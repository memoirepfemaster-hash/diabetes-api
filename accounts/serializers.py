# accounts/serializers.py
from rest_framework import serializers
from .models import PatientData

class PatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientData
        fields = ['id', 'gender', 'age', 'hypertension', 'heart_disease', 
                  'smoking_history', 'bmi', 'activite_physique',
                  'HbA1c_level', 'blood_glucose_level', 'diabetes', 'created_at']
        read_only_fields = ['id', 'created_at']


class DiabetesPredictionSerializer(serializers.Serializer):
    """Serializer pour la prédiction (entrée utilisateur)"""
    
    # Démographie
    gender = serializers.ChoiceField(choices=['Female', 'Male', 'Other'])
    age = serializers.IntegerField(min_value=18, max_value=120)  # ← MODIFIÉ: 18 au lieu de 0
    
    # Antécédents médicaux
    hypertension = serializers.BooleanField(default=False)
    heart_disease = serializers.BooleanField(default=False)
    smoking_history = serializers.ChoiceField(
        choices=['never', 'former', 'current', 'ever', 'not current'],
        default='never'
    )
    
    # Activité physique
    activite_physique = serializers.ChoiceField(
        choices=['FAIBLE', 'MODERE', 'ELEVE'],
        default='MODERE'
    )
    
    # Mesures cliniques
    bmi = serializers.FloatField(min_value=10, max_value=60)
    HbA1c_level = serializers.FloatField(min_value=3, max_value=15)
    blood_glucose_level = serializers.IntegerField(min_value=50, max_value=400)
    
    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("L'âge doit être au moins 18 ans")
        return value
    
    def validate_bmi(self, value):
        if value < 10 or value > 60:
            raise serializers.ValidationError("Le BMI doit être entre 10 et 60")
        return value
    
    def validate_HbA1c_level(self, value):
        if value < 3 or value > 15:
            raise serializers.ValidationError("L'HbA1c doit être entre 3% et 15%")
        return value
    
    def validate_blood_glucose_level(self, value):
        if value < 50 or value > 400:
            raise serializers.ValidationError("La glycémie doit être entre 50 et 400 mg/dL")
        return value