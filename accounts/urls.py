# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('predict/', views.PredictDiabetesView.as_view(), name='predict'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
]
