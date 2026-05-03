# diabetes_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.urls import path, include

# Page d'accueil
def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Diabète Prédiction API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .card {
                background: white;
                color: #333;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { color: #667eea; }
            a { color: #667eea; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .api-link {
                background: #f0f0f0;
                padding: 10px;
                margin: 10px 0;
                border-radius: 8px;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🩺 API de Prédiction du Diabète de Type 2</h1>
            <p>Bienvenue sur l'API de prédiction du diabète utilisant l'intelligence artificielle.</p>
            
            <h2>📡 Endpoints disponibles:</h2>
            <div class="api-link">POST /accounts/predict/ - Prédire le risque de diabète</div>
            <div class="api-link">GET /accounts/patients/ - Liste des patients</div>
            <div class="api-link">GET /accounts/statistics/ - Statistiques</div>
            <div class="api-link">GET /admin - Administration</div>
            
            <h2>🔐 Authentification:</h2>
            <div class="api-link"><a href="/users/register/">Inscription</a></div>
            <div class="api-link"><a href="/users/login/">Connexion</a></div>
            
            <h2>🚀 Frontend React:</h2>
            <p>Pour utiliser l'interface React, lancez: <code>cd frontend && npm start</code></p>
            <p>Puis ouvrez: <a href="http://localhost:3000">http://localhost:3000</a></p>
            
            <hr>
            <p style="text-align: center; color: #666;">
                ⚠️ Cet outil est une aide à la décision. Ne remplace pas un avis médical.
            </p>
        </div>
    </body>
    </html>
    """)

def home(request):
    return HttpResponse("API Running")

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ auth
    path('users/', include('users.urls')),

    # 🔥 IMPORTANT: add this
    path('api/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
]



