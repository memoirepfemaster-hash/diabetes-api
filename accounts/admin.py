# accounts/admin.py
from django.contrib import admin
from .models import PatientData

@admin.register(PatientData)
class PatientDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'gender', 'age', 'bmi', 'activite_physique', 
                    'HbA1c_level', 'blood_glucose_level', 'diabetes', 'created_at']
    
    list_filter = ['gender', 'hypertension', 'heart_disease', 'activite_physique', 'diabetes']
    
    search_fields = ['age', 'bmi']
    
    list_editable = ['diabetes']
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Démographie', {
            'fields': ('gender', 'age')
        }),
        ('Mesures cliniques', {
            'fields': ('bmi', 'HbA1c_level', 'blood_glucose_level')
        }),
        ('Antécédents', {
            'fields': ('hypertension', 'heart_disease', 'smoking_history', 'activite_physique')
        }),
        ('Diagnostic', {
            'fields': ('diabetes',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )