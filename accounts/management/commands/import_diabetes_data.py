import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from accounts.models import PatientData

class Command(BaseCommand):
    help = 'Importe le dataset avec ajout de activité physique et âge ≥ 18 ans'

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Début de l'importation des données...")
        
        # 1. Charger les données
        df = pd.read_csv('accounts/bdd/diabetes_prediction_dataset.csv')
        self.stdout.write(f"📊 {len(df)} lignes chargées")
        
        # 2. Ajouter ACTIVITÉ PHYSIQUE (distribution réaliste)
        np.random.seed(42)
        n = len(df)
        
        activite_choices = ['FAIBLE', 'MODERE', 'ELEVE']
        activite_probs = [0.35, 0.45, 0.20]
        
        df['activite_physique'] = np.random.choice(activite_choices, size=n, p=activite_probs)
        
        self.stdout.write(f"\n✅ Activité physique ajoutée:")
        self.stdout.write(f"   - FAIBLE: {(df['activite_physique'] == 'FAIBLE').sum()} ({(df['activite_physique'] == 'FAIBLE').sum()/n*100:.1f}%)")
        self.stdout.write(f"   - MODERE: {(df['activite_physique'] == 'MODERE').sum()} ({(df['activite_physique'] == 'MODERE').sum()/n*100:.1f}%)")
        self.stdout.write(f"   - ELEVE: {(df['activite_physique'] == 'ELEVE').sum()} ({(df['activite_physique'] == 'ELEVE').sum()/n*100:.1f}%)")
        
        # 3. Supprimer les doublons
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        self.stdout.write(f"\n🧹 Doublons supprimés: {before - after}")
        
        # 4. Supprimer les valeurs aberrantes
        # 4.1 Âge ≥ 18 ans (critère d'inclusion)
        before_age = len(df)
        df = df[df['age'] >= 18]
        self.stdout.write(f"   - Âge < 18 ans supprimés: {before_age - len(df)}")
        
        # 4.2 BMI valide (10-60)
        before_bmi = len(df)
        df = df[(df['bmi'] >= 10) & (df['bmi'] <= 60)]
        self.stdout.write(f"   - BMI invalide supprimés: {before_bmi - len(df)}")
        
        # 4.3 HbA1c valide (3-15)
        before_hba1c = len(df)
        df = df[(df['HbA1c_level'] >= 3) & (df['HbA1c_level'] <= 15)]
        self.stdout.write(f"   - HbA1c invalide supprimés: {before_hba1c - len(df)}")
        
        # 4.4 Glycémie valide (50-400)
        before_glucose = len(df)
        df = df[(df['blood_glucose_level'] >= 50) & (df['blood_glucose_level'] <= 400)]
        self.stdout.write(f"   - Glycémie invalide supprimés: {before_glucose - len(df)}")
        
        self.stdout.write(f"\n📊 Après nettoyage: {len(df)} lignes")
        
        # 5. Statistiques de la population
        self.stdout.write("\n📊 Statistiques de la population:")
        self.stdout.write(f"   - Âge moyen: {df['age'].mean():.1f} ans")
        self.stdout.write(f"   - Âge min: {df['age'].min()} ans")
        self.stdout.write(f"   - Âge max: {df['age'].max()} ans")
        self.stdout.write(f"   - BMI moyen: {df['bmi'].mean():.1f} kg/m²")
        self.stdout.write(f"   - HbA1c moyen: {df['HbA1c_level'].mean():.1f}%")
        self.stdout.write(f"   - Glycémie moyenne: {df['blood_glucose_level'].mean():.0f} mg/dL")
        
        # Répartition par genre
        self.stdout.write(f"\n   - Répartition par genre:")
        for gender in df['gender'].unique():
            count = len(df[df['gender'] == gender])
            self.stdout.write(f"      * {gender}: {count} ({count/len(df)*100:.1f}%)")
        
        # Pourcentage de diabétiques
        diabetics = df['diabetes'].sum()
        self.stdout.write(f"\n   - Diabétiques: {diabetics} ({diabetics/len(df)*100:.1f}%)")
        self.stdout.write(f"   - Non-diabétiques: {len(df)-diabetics} ({(len(df)-diabetics)/len(df)*100:.1f}%)")
        
        # 6. Supprimer les anciennes données
        old_count = PatientData.objects.count()
        PatientData.objects.all().delete()
        self.stdout.write(f"\n🗑️ {old_count} anciens enregistrements supprimés")
        
        # 7. Importer les données
        self.stdout.write("\n💾 Importation dans la base de données...")
        patients = []
        for _, row in df.iterrows():
            patient = PatientData(
                gender=row['gender'],
                age=int(row['age']),
                hypertension=bool(row['hypertension']),
                heart_disease=bool(row['heart_disease']),
                smoking_history=row['smoking_history'],
                bmi=round(row['bmi'], 1),
                activite_physique=row['activite_physique'],
                HbA1c_level=round(row['HbA1c_level'], 1),
                blood_glucose_level=int(row['blood_glucose_level']),
                diabetes=bool(row['diabetes'])
            )
            patients.append(patient)
        
        PatientData.objects.bulk_create(patients)
        
        self.stdout.write(self.style.SUCCESS(
            f"\n{'='*50}\n"
            f"✅ IMPORTATION TERMINÉE!\n"
            f"{'='*50}\n"
            f"📊 Total patients: {len(patients)}\n"
            f"🔴 Diabétiques: {diabetics} ({diabetics/len(df)*100:.1f}%)\n"
            f"🟢 Non-diabétiques: {len(df)-diabetics} ({(len(df)-diabetics)/len(df)*100:.1f}%)\n"
            f"\n📏 Âge minimum: {df['age'].min()} ans (≥ 18 ans)\n"
            f"🏃 Répartition activité physique:\n"
            f"   - FAIBLE: {(df['activite_physique'] == 'FAIBLE').sum()}\n"
            f"   - MODERE: {(df['activite_physique'] == 'MODERE').sum()}\n"
            f"   - ELEVE: {(df['activite_physique'] == 'ELEVE').sum()}\n"
            f"{'='*50}"
        ))