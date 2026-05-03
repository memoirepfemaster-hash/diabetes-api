# accounts/models.py
from django.db import models
from django.conf import settings

class PatientData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    age = models.IntegerField()

    hypertension = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    smoking_history = models.CharField(max_length=20, blank=True, null=True)

    bmi = models.FloatField()
    HbA1c_level = models.FloatField()
    blood_glucose_level = models.IntegerField()

    activite_physique = models.CharField(max_length=10, choices=[
        ('FAIBLE','Faible'),
        ('MODERE','Modéré'),
        ('ELEVE','Élevé')
    ], null=True, blank=True)

    diabetes = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient {self.id}"