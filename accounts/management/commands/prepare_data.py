# accounts/management/commands/prepare_data.py
import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Nettoie et prépare les données une seule fois'

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Nettoyage et préparation des données...")
        
        # 1. Charger les données brutes
        df = pd.read_csv('accounts/bdd/diabetes_prediction_dataset.csv')
        self.stdout.write(f"📊 {len(df)} lignes brutes chargées")
        
        # 2. Supprimer les doublons
        before = len(df)
        df = df.drop_duplicates()
        self.stdout.write(f"🗑️ Doublons supprimés: {before - len(df)}")
        
        # 3. Supprimer les valeurs aberrantes
        df = df[(df['bmi'] >= 10) & (df['bmi'] <= 60)]
        df = df[(df['HbA1c_level'] >= 3) & (df['HbA1c_level'] <= 15)]
        df = df[(df['blood_glucose_level'] >= 50) & (df['blood_glucose_level'] <= 400)]
        self.stdout.write(f"📊 Après nettoyage: {len(df)} lignes")
        
        # 4. Ajouter activité physique (distribution réaliste)
        np.random.seed(42)
        n = len(df)
        activite_choices = ['FAIBLE', 'MODERE', 'ELEVE']
        activite_probs = [0.35, 0.45, 0.20]
        df['activite_physique'] = np.random.choice(activite_choices, size=n, p=activite_probs)
        
        # 5. Sauvegarder les données nettoyées
        df.to_csv('accounts/bdd/diabetes_clean.csv', index=False)
        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Données nettoyées sauvegardées!\n"
            f"   - Fichier: accounts/bdd/diabetes_clean.csv\n"
            f"   - {len(df)} patients prêts à l'emploi"
        ))