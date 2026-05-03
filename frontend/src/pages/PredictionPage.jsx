// src/pages/PredictionPage.jsx
// src/pages/PredictionPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './PredictionPage.css';

const PredictionPage = () => {
  const [formData, setFormData] = useState({
    gender: 'Female',
    age: '',
    hypertension: false,
    heart_disease: false,
    smoking_history: 'never',
    activite_physique: 'MODERE',
    bmi: '',
    HbA1c_level: '',
    blood_glucose_level: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Validation frontend supplémentaire
    const bmi = parseFloat(formData.bmi);
    const hba1c = parseFloat(formData.HbA1c_level);
    const glucose = parseInt(formData.blood_glucose_level);

    if (bmi < 10 || bmi > 60) {
      setError('L\'IMC doit être compris entre 10 et 60 kg/m²');
      setLoading(false);
      return;
    }

    if (hba1c < 3 || hba1c > 15) {
      setError('L\'HbA1c doit être compris entre 3% et 15%');
      setLoading(false);
      return;
    }

    if (glucose < 50 || glucose > 400) {
      setError('La glycémie doit être comprise entre 50 et 400 mg/dL');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/accounts/predict/', {
        gender: formData.gender,
        age: parseInt(formData.age),
        hypertension: formData.hypertension,
        heart_disease: formData.heart_disease,
        smoking_history: formData.smoking_history,
        activite_physique: formData.activite_physique,
        bmi: bmi,
        HbA1c_level: hba1c,
        blood_glucose_level: glucose
      });
      setResult(response.data);
    } catch (err) {
      console.error('Erreur:', err);
      if (err.response) {
        if (err.response.status === 401) {
          setError('Non autorisé. Veuillez vous connecter.');
        } else if (err.response.status === 400) {
          setError('Données invalides. Vérifiez vos informations.');
        } else {
          setError(`Erreur serveur: ${err.response.status}`);
        }
      } else if (err.request) {
        setError('Impossible de contacter le serveur. Vérifiez que Django est démarré.');
      } else {
        setError('Erreur de connexion. Réessayez plus tard.');
      }
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel) => {
    switch(riskLevel) {
      case 'high': return '#ff6b6b';
      case 'medium': return '#ffd93d';
      case 'low': return '#4fd1c5';
      default: return '#7c5cff';
    }
  };

  const getRiskText = (riskLevel) => {
    switch(riskLevel) {
      case 'high': return '⚠️ Risque ÉLEVÉ';
      case 'medium': return '📊 Risque MODÉRÉ';
      case 'low': return '✅ Risque FAIBLE';
      default: return 'Risque inconnu';
    }
  };

  return (
    <div className="prediction-page">
      {/* Hero Section */}
<div className="prediction-hero">
  <div className="prediction-hero-overlay"></div>
  <div className="prediction-hero-content">
    <h1>
      <span>Prédiction du Diabète</span>
      <span className="hero-subtitle"> de Type 2</span>
    </h1>
    <p>Outil d'aide à la décision basé sur l'intelligence artificielle</p>
  </div>
</div>

      {/* Main Container */}
      <div className="prediction-main">
        <div className="prediction-grid">
          
          {/* Formulaire */}
        <div className="prediction-form-card glass-card">
  <div className="card-header">
    <div className="card-header-title">
      <span className="header-icon">📝</span>
      <h3>Données du patient</h3>
    </div>
    <p className="card-header-sub">Remplissez les informations suivantes</p>
  </div>
            
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Genre</label>
                <div className="gender-buttons">
                  <button 
                    type="button"
                    className={`gender-btn ${formData.gender === 'Female' ? 'active' : ''}`}
                    onClick={() => setFormData({...formData, gender: 'Female'})}
                  >
                    <span>👩</span> Femme
                  </button>
                  <button 
                    type="button"
                    className={`gender-btn ${formData.gender === 'Male' ? 'active' : ''}`}
                    onClick={() => setFormData({...formData, gender: 'Male'})}
                  >
                    <span>👨</span> Homme
                  </button>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Âge (ans)</label>
                  <input 
                    type="number" 
                    className="form-input" 
                    name="age" 
                    value={formData.age} 
                    onChange={handleChange} 
                    required 
                    min="18" 
                    max="120"
                    placeholder="Ex: 45"
                  />
                </div>

                <div className="form-group">
                  <label>IMC (kg/m²)</label>
                  <input 
                    type="number" 
                    step="0.1" 
                    className="form-input" 
                    name="bmi" 
                    value={formData.bmi} 
                    onChange={handleChange} 
                    required 
                    min="10" 
                    max="60"
                    placeholder="Ex: 24.5"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>HbA1c (%)</label>
                  <input 
                    type="number" 
                    step="0.1" 
                    className="form-input" 
                    name="HbA1c_level" 
                    value={formData.HbA1c_level} 
                    onChange={handleChange} 
                    required 
                    min="3" 
                    max="15"
                    placeholder="Ex: 5.7"
                  />
                </div>

                <div className="form-group">
                  <label>Glycémie (mg/dL)</label>
                  <input 
                    type="number" 
                    className="form-input" 
                    name="blood_glucose_level" 
                    value={formData.blood_glucose_level} 
                    onChange={handleChange} 
                    required 
                    min="50" 
                    max="400"
                    placeholder="Ex: 120"
                  />
                </div>
              </div>

              <div className="checkbox-group">
                <label className="checkbox-label">
                  <input 
                    type="checkbox" 
                    name="hypertension" 
                    checked={formData.hypertension} 
                    onChange={handleChange} 
                  />
                  <span>Hypertension artérielle</span>
                </label>

                <label className="checkbox-label">
                  <input 
                    type="checkbox" 
                    name="heart_disease" 
                    checked={formData.heart_disease} 
                    onChange={handleChange} 
                  />
                  <span>Maladie cardiaque</span>
                </label>
              </div>

              <div className="form-group">
                <label>Tabagisme</label>
                <select className="form-select" name="smoking_history" value={formData.smoking_history} onChange={handleChange}>
                  <option value="never">Jamais fumé</option>
                  <option value="former">Ancien fumeur</option>
                  <option value="current">Fumeur actuel</option>
                </select>
              </div>

              <div className="form-group">
                <label>Activité physique</label>
                <select className="form-select" name="activite_physique" value={formData.activite_physique} onChange={handleChange}>
                  <option value="FAIBLE">🏠 Faible</option>
                  <option value="MODERE">🚶 Modérée</option>
                  <option value="ELEVE">🏃 Élevée</option>
                </select>
              </div>

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Prédiction en cours...
                  </>
                ) : (
                  <>
                    <span>🔮</span>
                    Prédire le risque
                    <span>→</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Résultats */}
          <div className="prediction-result-card glass-card">
  <div className="card-header">
  <div className="card-header-title">
    <span className="header-icon">📊</span>
    <h3>Résultat de l'analyse</h3>
  </div>
  <p className="card-header-sub">Basé sur les données fournies</p>
</div>
            {error && (
              <div className="error-message">
                <span>❌</span>
                <p>{error}</p>
              </div>
            )}

            {!result && !error && (
              <div className="empty-state">
                <div className="empty-icon">🔍</div>
                <p>Remplissez le formulaire et cliquez sur "Prédire le risque" pour voir le résultat</p>
              </div>
            )}

            {result && (
              <div className="result-content">
                <div className={`risk-badge ${result.risk_level}`}>
                  {getRiskText(result.risk_level)}
                </div>

                <div className="probability-section">
                  <h4>Probabilité de diabète</h4>
                  <div className="probability-value" style={{ color: getRiskColor(result.risk_level) }}>
                    {(result.probability * 100).toFixed(1)}%
                  </div>
                  <div className="progress-bar-container">
                    <div 
                      className="progress-bar-fill" 
                      style={{ width: `${result.probability * 100}%`, backgroundColor: getRiskColor(result.risk_level) }}
                    ></div>
                  </div>
                </div>

                <div className="info-card recommendation">
                  <div className="info-icon">💊</div>
                  <div className="info-content">
                    <h4>Recommandation</h4>
                    <p>{result.recommendation}</p>
                  </div>
                </div>

                <div className="info-card warning">
                  <div className="info-icon">⚠️</div>
                  <div className="info-content">
                    <h4>Avertissement</h4>
                    <p>{result.message}</p>
                  </div>
                </div>

                {/* ⭐ CONSEILS DE PRÉVENTION ⭐ */}
                {result.prevention_tips && (
                  <div className="info-card prevention">
                    <div className="info-content">
                      <h4>Conseils de prévention</h4>
                      <ul>
                        {result.prevention_tips.map((tip, index) => (
                          <li key={index}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer Note */}
      <div className="prediction-footer">
        <p>🔬 Cet outil utilise un modèle d'intelligence artificielle pour estimer le risque de diabète de type 2</p>
      </div>
    </div>
  );
};

export default PredictionPage;