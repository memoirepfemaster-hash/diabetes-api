# accounts/management/commands/train_model.py
import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from accounts.models import PatientData
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix, average_precision_score, brier_score_loss, roc_curve
import joblib
import os
from xgboost import XGBClassifier

class Command(BaseCommand):
    help = 'Entraîne les modèles sur le nouveau dataset avec activite_physique'

    def encode_gender(self, value):
        """Encoder le genre"""
        mapping = {'Female': 0, 'Male': 1, 'Other': 2}
        return mapping.get(value, 0)
    
    def encode_smoking(self, value):
        """Encoder l'historique de tabagisme"""
        mapping = {
            'never': 0,
            'former': 1,
            'current': 2,
            'ever': 3,
            'not current': 4
        }
        return mapping.get(value, 0)
    
    def encode_activite(self, value):
        """Encoder l'activité physique"""
        mapping = {'FAIBLE': 0, 'MODERE': 1, 'ELEVE': 2}
        return mapping.get(value, 1)

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 60)
        self.stdout.write("🚀 DÉBUT DE L'ENTRAÎNEMENT DES MODÈLES")
        self.stdout.write("=" * 60)
        
        # 📊 1. Charger les données depuis Django
        self.stdout.write("\n📊 1. Chargement des données depuis Django...")
        patients = PatientData.objects.all()
        
        if patients.count() == 0:
            self.stdout.write(self.style.ERROR("❌ Aucune donnée trouvée! Exécutez d'abord import_diabetes_data"))
            return
        
        # Convertir en DataFrame
        data = []
        for p in patients:
            data.append({
                'age': p.age,
                'hypertension': 1 if p.hypertension else 0,
                'heart_disease': 1 if p.heart_disease else 0,
                'bmi': p.bmi,
                'HbA1c_level': p.HbA1c_level,
                'blood_glucose_level': p.blood_glucose_level,
                'gender': self.encode_gender(p.gender),
                'smoking_history': self.encode_smoking(p.smoking_history),
                'activite_physique': self.encode_activite(p.activite_physique) if p.activite_physique else 1,
                'diabetes': 1 if p.diabetes else 0
            })
        
        df = pd.DataFrame(data)
        
        self.stdout.write(self.style.SUCCESS(f"   ✅ {len(df)} patients chargés"))
        
        # Afficher la répartition des classes
        diab_count = df['diabetes'].sum()
        non_diab_count = len(df) - diab_count
        self.stdout.write(f"   📊 Répartition: {diab_count} diabétiques ({diab_count/len(df)*100:.1f}%), {non_diab_count} non-diabétiques ({non_diab_count/len(df)*100:.1f}%)")
        
        # 2. Préparer X et y
        X = df.drop('diabetes', axis=1)
        y = df['diabetes']
        
        # 3. Division des données
        self.stdout.write("\n📊 2. Division des données...")
        
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
        
        self.stdout.write(f"   - Train: {len(X_train)} patients")
        self.stdout.write(f"   - Validation: {len(X_val)} patients")
        self.stdout.write(f"   - Test: {len(X_test)} patients")
        
        # 4. Normalisation
        self.stdout.write("\n📊 3. Normalisation des données...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        X_test_scaled = scaler.transform(X_test)
        self.stdout.write("   ✅ Normalisation terminée")
        
        # =========================================================
        # 5. Logistic Regression (Baseline)
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 4. Entraînement du BASELINE (Logistic Regression)")
        self.stdout.write("=" * 60)
        
        baseline_model = LogisticRegression(max_iter=1000, random_state=42)
        baseline_model.fit(X_train_scaled, y_train)
        
        y_test_baseline_proba = baseline_model.predict_proba(X_test_scaled)[:, 1]
        test_baseline_acc = accuracy_score(y_test, baseline_model.predict(X_test_scaled))
        test_baseline_auc = roc_auc_score(y_test, y_test_baseline_proba)
        
        self.stdout.write(f"   - Accuracy: {test_baseline_acc:.3f}")
        self.stdout.write(f"   - AUC-ROC: {test_baseline_auc:.3f}")
        
        # =========================================================
        # 6. Random Forest
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 5. Entraînement du modèle Random Forest")
        self.stdout.write("=" * 60)
        
        rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
        rf_model.fit(X_train_scaled, y_train)
        
        y_test_rf_proba = rf_model.predict_proba(X_test_scaled)[:, 1]
        test_rf_acc = accuracy_score(y_test, rf_model.predict(X_test_scaled))
        test_rf_auc = roc_auc_score(y_test, y_test_rf_proba)
        
        self.stdout.write(f"   - Accuracy: {test_rf_acc:.3f}")
        self.stdout.write(f"   - AUC-ROC: {test_rf_auc:.3f}")
        
        # =========================================================
        # 7. XGBoost
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 6. Entraînement du modèle XGBoost")
        self.stdout.write("=" * 60)
        
        xgb_model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='logloss')
        xgb_model.fit(X_train_scaled, y_train)
        
        y_test_xgb_proba = xgb_model.predict_proba(X_test_scaled)[:, 1]
        test_xgb_acc = accuracy_score(y_test, xgb_model.predict(X_test_scaled))
        test_xgb_auc = roc_auc_score(y_test, y_test_xgb_proba)
        
        self.stdout.write(f"   - Accuracy: {test_xgb_acc:.3f}")
        self.stdout.write(f"   - AUC-ROC: {test_xgb_auc:.3f}")
        
        # =========================================================
        # 8. Comparaison
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 7. COMPARAISON DES MODÈLES")
        self.stdout.write("=" * 60)
        
        self.stdout.write("\n   📈 Tableau comparatif:")
        self.stdout.write("   " + "-" * 55)
        self.stdout.write(f"   | {'Modèle':<25} | {'Accuracy':<10} | {'AUC-ROC':<10} |")
        self.stdout.write("   " + "-" * 55)
        self.stdout.write(f"   | {'Logistic Regression':<25} | {test_baseline_acc:<10.3f} | {test_baseline_auc:<10.3f} |")
        self.stdout.write(f"   | {'Random Forest':<25} | {test_rf_acc:<10.3f} | {test_rf_auc:<10.3f} |")
        self.stdout.write(f"   | {'XGBoost':<25} | {test_xgb_acc:<10.3f} | {test_xgb_auc:<10.3f} |")
        self.stdout.write("   " + "-" * 55)
        
        # Meilleur modèle
        best_auc = max(test_baseline_auc, test_rf_auc, test_xgb_auc)
        if best_auc == test_xgb_auc:
            best_model = xgb_model
            best_model_name = 'xgboost'
        elif best_auc == test_rf_auc:
            best_model = rf_model
            best_model_name = 'random_forest'
        else:
            best_model = baseline_model
            best_model_name = 'logistic_regression'
        
        self.stdout.write(self.style.SUCCESS(f"\n   🏆 Meilleur modèle: {best_model_name.upper()} avec AUC = {best_auc:.3f}"))
        
        # =========================================================
        # 9. Évaluation détaillée
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(f"📊 8. ÉVALUATION DU MODÈLE ({best_model_name.upper()})")
        self.stdout.write("=" * 60)
        
        y_pred = best_model.predict(X_test_scaled)
        y_proba = best_model.predict_proba(X_test_scaled)[:, 1]
        
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        f1 = 2 * (precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) > 0 else 0
        
        self.stdout.write(f"\n   📈 Métriques:")
        self.stdout.write(f"      - Accuracy: {accuracy:.3f}")
        self.stdout.write(f"      - Sensitivity: {sensitivity:.3f}")
        self.stdout.write(f"      - Specificity: {specificity:.3f}")
        self.stdout.write(f"      - Precision: {precision:.3f}")
        self.stdout.write(f"      - F1-Score: {f1:.3f}")
        
        auprc = average_precision_score(y_test, y_proba)
        self.stdout.write(f"\n   📈 AUC-PR: {auprc:.3f}")
        
        brier = brier_score_loss(y_test, y_proba)
        self.stdout.write(f"   📈 Brier Score: {brier:.3f}")
        
        fpr, tpr, thresholds = roc_curve(y_test, y_proba)
        youden_j = tpr - fpr
        best_idx = youden_j.argmax()
        best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
        
        self.stdout.write(f"\n   📈 Seuil optimal (Youden): {best_threshold:.3f}")
        self.stdout.write(f"      - Sensitivity: {tpr[best_idx]:.3f}")
        self.stdout.write(f"      - Specificity: {1 - fpr[best_idx]:.3f}")
        
        # =========================================================
        # 10. Importance des caractéristiques
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 9. IMPORTANCE DES CARACTÉRISTIQUES")
        self.stdout.write("=" * 60)
        
        feature_names = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 
                         'blood_glucose_level', 'gender', 'smoking_history', 'activite_physique']
        
        if best_model_name == 'logistic_regression':
            importance = abs(best_model.coef_[0])
        else:
            importance = best_model.feature_importances_
        
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        for _, row in feature_importance.iterrows():
            bar = "█" * int(row['importance'] * 50)
            self.stdout.write(f"   - {row['feature']:20s}: {row['importance']:.3f} {bar}")
                # =========================================================
        # 11. PERFORMANCE PAR SOUS-GROUPES (NOUVEAU)
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 11. PERFORMANCE PAR SOUS-GROUPES")
        self.stdout.write("=" * 60)
        
        # Créer un DataFrame avec les prédictions et les vraies valeurs
        results_df = X_test.copy()
        results_df['y_true'] = y_test.values
        results_df['y_proba'] = y_proba
        results_df['y_pred'] = y_pred
        
        # 1. Performance par sexe (gender)
        self.stdout.write("\n   📊 Performance par sexe:")
        for gender_val in [0, 1]:
            gender_mask = results_df['gender'] == gender_val
            if gender_mask.sum() > 0:
                gender_auc = roc_auc_score(
                    results_df.loc[gender_mask, 'y_true'], 
                    results_df.loc[gender_mask, 'y_proba']
                )
                gender_acc = accuracy_score(
                    results_df.loc[gender_mask, 'y_true'], 
                    results_df.loc[gender_mask, 'y_pred']
                )
                gender_name = "Homme" if gender_val == 1 else "Femme"
                self.stdout.write(f"      - {gender_name}: AUC = {gender_auc:.3f}, Accuracy = {gender_acc:.3f} ({gender_mask.sum()} patients)")
        
        # 2. Performance par âge
        self.stdout.write("\n   📊 Performance par tranche d'âge:")
        age_groups = [
    ('Jeune (18-40 ans)', (results_df['age'] >= 18) & (results_df['age'] < 40)),  # ← MODIFIÉ
    ('Adulte (40-60 ans)', (results_df['age'] >= 40) & (results_df['age'] <= 60)),
    ('Âgé (> 60 ans)', results_df['age'] > 60)
]
        
        for group_name, mask in age_groups:
            if mask.sum() > 0:
                group_auc = roc_auc_score(
                    results_df.loc[mask, 'y_true'], 
                    results_df.loc[mask, 'y_proba']
                )
                group_acc = accuracy_score(
                    results_df.loc[mask, 'y_true'], 
                    results_df.loc[mask, 'y_pred']
                )
                self.stdout.write(f"      - {group_name}: AUC = {group_auc:.3f}, Accuracy = {group_acc:.3f} ({mask.sum()} patients)")
        
        # 3. Performance par IMC (bmi)
        self.stdout.write("\n   📊 Performance par catégorie d'IMC:")
        bmi_groups = [
            ('Normal (18.5-25)', (results_df['bmi'] >= 18.5) & (results_df['bmi'] < 25)),
            ('Surpoids (25-30)', (results_df['bmi'] >= 25) & (results_df['bmi'] < 30)),
            ('Obésité (≥ 30)', results_df['bmi'] >= 30)
        ]
        
        for group_name, mask in bmi_groups:
            if mask.sum() > 0:
                group_auc = roc_auc_score(
                    results_df.loc[mask, 'y_true'], 
                    results_df.loc[mask, 'y_proba']
                )
                group_acc = accuracy_score(
                    results_df.loc[mask, 'y_true'], 
                    results_df.loc[mask, 'y_pred']
                )
                self.stdout.write(f"      - {group_name}: AUC = {group_auc:.3f}, Accuracy = {group_acc:.3f} ({mask.sum()} patients)")
        
        # 4. Performance par hypertension
        self.stdout.write("\n   📊 Performance par hypertension:")
        for hyp_val in [0, 1]:
            hyp_mask = results_df['hypertension'] == hyp_val
            if hyp_mask.sum() > 0:
                hyp_auc = roc_auc_score(
                    results_df.loc[hyp_mask, 'y_true'], 
                    results_df.loc[hyp_mask, 'y_proba']
                )
                hyp_name = "Avec hypertension" if hyp_val == 1 else "Sans hypertension"
                self.stdout.write(f"      - {hyp_name}: AUC = {hyp_auc:.3f} ({hyp_mask.sum()} patients)")
        
        # 5. Performance par activité physique
        self.stdout.write("\n   📊 Performance par niveau d'activité physique:")
        for act_val in [0, 1, 2]:
            act_mask = results_df['activite_physique'] == act_val
            if act_mask.sum() > 0:
                act_auc = roc_auc_score(
                    results_df.loc[act_mask, 'y_true'], 
                    results_df.loc[act_mask, 'y_proba']
                )
                act_names = {0: 'FAIBLE', 1: 'MODERE', 2: 'ELEVE'}
                act_name = act_names.get(act_val, 'Inconnu')
                self.stdout.write(f"      - {act_name}: AUC = {act_auc:.3f} ({act_mask.sum()} patients)")
        
        # 6. Détection des biais (biais)
        self.stdout.write("\n   📊 Détection des biais potentiels:")
        
        # Comparaison Hommes vs Femmes
        homme_mask = results_df['gender'] == 1
        femme_mask = results_df['gender'] == 0
        if homme_mask.sum() > 0 and femme_mask.sum() > 0:
            homme_auc = roc_auc_score(results_df.loc[homme_mask, 'y_true'], results_df.loc[homme_mask, 'y_proba'])
            femme_auc = roc_auc_score(results_df.loc[femme_mask, 'y_true'], results_df.loc[femme_mask, 'y_proba'])
            diff_auc = abs(homme_auc - femme_auc)
            if diff_auc > 0.05:
                self.stdout.write(self.style.WARNING(f"      ⚠️ Biais potentiel entre hommes et femmes: différence AUC = {diff_auc:.3f}"))
            else:
                self.stdout.write(f"      ✅ Pas de biais significatif entre hommes et femmes (diff = {diff_auc:.3f})")
        
        # Comparaison Jeunes vs Âgés
        jeune_mask = results_df['age'] < 40
        age_mask = results_df['age'] > 60
        if jeune_mask.sum() > 0 and age_mask.sum() > 0:
            jeune_auc = roc_auc_score(results_df.loc[jeune_mask, 'y_true'], results_df.loc[jeune_mask, 'y_proba'])
            age_auc = roc_auc_score(results_df.loc[age_mask, 'y_true'], results_df.loc[age_mask, 'y_proba'])
            diff_auc = abs(jeune_auc - age_auc)
            if diff_auc > 0.05:
                self.stdout.write(self.style.WARNING(f"      ⚠️ Biais potentiel entre jeunes et âgés: différence AUC = {diff_auc:.3f}"))
            else:
                self.stdout.write(f"      ✅ Pas de biais significatif entre jeunes et âgés (diff = {diff_auc:.3f})")
        # =========================================================
        # 12. Sauvegarde
        # =========================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 10. Sauvegarde des modèles")
        self.stdout.write("=" * 60)
        
        os.makedirs('accounts/ml_models', exist_ok=True)
        
        joblib.dump(best_model, 'accounts/ml_models/diabetes_model.pkl')
        joblib.dump(scaler, 'accounts/ml_models/scaler.pkl')
        
        metrics = {
            'best_model': best_model_name,
            'best_threshold': float(best_threshold),
            'accuracy': accuracy,
            'sensitivity': sensitivity,
            'specificity': specificity,
            'auc': best_auc,
            'brier_score': brier,
            'feature_importance': dict(zip(feature_names, importance))
        }
        joblib.dump(metrics, 'accounts/ml_models/metrics.pkl')
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ MODÈLE SAUVEGARDÉ! AUC = {best_auc:.3f}"))
               