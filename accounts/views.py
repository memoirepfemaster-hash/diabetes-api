# accounts/views.py
# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg
from .models import PatientData
from .serializers import PatientDataSerializer, DiabetesPredictionSerializer

import joblib
import numpy as np
import os

# ============================================================
# MODELS PATH
# ============================================================

MODEL_PATH = os.path.join('accounts', 'ml_models', 'diabetes_model.pkl')
SCALER_PATH = os.path.join('accounts', 'ml_models', 'scaler.pkl')
METRICS_PATH = os.path.join('accounts', 'ml_models', 'metrics.pkl')

model = None
scaler = None
best_threshold = 0.075

# ============================================================
# LOAD MODELS
# ============================================================

def load_models():
    global model, scaler, best_threshold

    if model is None:
        try:
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH)

            if os.path.exists(METRICS_PATH):
                metrics = joblib.load(METRICS_PATH)
                best_threshold = metrics.get('best_threshold', 0.075)

            print("✅ Model loaded successfully")

        except Exception as e:
            print("❌ Error loading model:", e)
            model = None
            scaler = None

    return model, scaler, best_threshold


# ============================================================
# ENCODING FUNCTIONS
# ============================================================

def encode_gender(gender):
    return {'Female': 0, 'Male': 1, 'Other': 2}.get(gender, 0)


def encode_smoking(smoking_history):
    mapping = {
        'never': 0,
        'former': 1,
        'current': 2,
        'ever': 3,
        'not current': 4
    }
    return mapping.get(smoking_history, 0)


def encode_activite(value):
    return {'FAIBLE': 0, 'MODERE': 1, 'ELEVE': 2}.get(value, 1)


# ============================================================
# PATIENTS (USER-BASED)
# ============================================================

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientData.objects.filter(user=self.request.user)


# ============================================================
# PREDICTION API (ACCÈS PUBLIC)
# ============================================================

class PredictDiabetesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        model, scaler, best_threshold = load_models()

        serializer = DiabetesPredictionSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            if model is None or scaler is None:
                return Response({
                    "error": "Model not available"
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            features = np.array([[
                data['age'],
                1 if data['hypertension'] else 0,
                1 if data['heart_disease'] else 0,
                data['bmi'],
                data['HbA1c_level'],
                data['blood_glucose_level'],
                encode_gender(data['gender']),
                encode_smoking(data['smoking_history']),
                encode_activite(data.get('activite_physique', 'MODERE'))
            ]])

            features_scaled = scaler.transform(features)
            probability = model.predict_proba(features_scaled)[0][1]

            # Déterminer le niveau de risque et la recommandation
            if probability >= best_threshold:
                risk_category = "Élevé"
                risk_level = "high"
                recommendation = "Consultation urgente. Bilan diabétique complet nécessaire."
                
                # Conseils de prévention pour risque ÉLEVÉ
                prevention_tips = [
                    "📅 Consultez votre médecin rapidement",
                    "🥗 Adoptez une alimentation équilibrée (faible en sucres rapides)",
                    "🏃 Pratiquez une activité physique régulière (30 min/jour)",
                    "🩸 Faites un bilan sanguin complet (HbA1c, glycémie)",
                    "⚖️ Perdez 5-10% de votre poids si vous êtes en surpoids"
                ]
                
            elif probability >= 0.3:
                risk_category = "Modéré"
                risk_level = "medium"
                recommendation = "Consultez votre médecin. Contrôle glycémique recommandé."
                
                # Conseils de prévention pour risque MODÉRÉ
                prevention_tips = [
                    "🩺 Contrôlez votre glycémie régulièrement",
                    "🥦 Réduisez les sucres rapides et les boissons sucrées",
                    "🚶 Marchez 30 minutes par jour",
                    "⚖️ Surveillez votre poids et votre IMC",
                    "🩸 Faites un contrôle HbA1c tous les 6 mois"
                ]
                
            else:
                risk_category = "Faible"
                risk_level = "low"
                recommendation = "Maintenez un mode de vie sain. Contrôle dans 1 an."
                
                # Conseils de prévention pour risque FAIBLE
                prevention_tips = [
                    "✅ Maintenez votre mode de vie sain",
                    "🥬 Continuez une alimentation équilibrée",
                    "🏋️ Restez actif physiquement",
                    "🩺 Contrôle annuel recommandé",
                    "🍎 Mangez 5 fruits et légumes par jour"
                ]

            return Response({
                "probability": round(probability, 3),
                "risk_category": risk_category,
                "recommendation": recommendation,
                "risk_level": risk_level,
                "threshold_used": round(best_threshold, 3),
                "message": "Cet outil est une aide à la décision. Ne remplace pas un avis médical.",
                "prevention_tips": prevention_tips
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================
# STATISTICS
# ============================================================

class StatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = PatientData.objects.filter(user=request.user).count()
        diabetiques = PatientData.objects.filter(user=request.user, diabetes=True).count()

        stats = PatientData.objects.filter(user=request.user).aggregate(
            age_moyen=Avg('age'),
            bmi_moyen=Avg('bmi'),
            hba1c_moyen=Avg('HbA1c_level'),
            glycemie_moyenne=Avg('blood_glucose_level')
        )

        return Response({
            "total_patients": total,
            "diabetiques": diabetiques,
            "non_diabetiques": total - diabetiques,
            "moyennes": {
                "age": stats['age_moyen'] or 0,
                "bmi": stats['bmi_moyen'] or 0,
                "hba1c": stats['hba1c_moyen'] or 0,
                "glycemie": stats['glycemie_moyenne'] or 0
            }
        })