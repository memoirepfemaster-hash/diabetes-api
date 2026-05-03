// src/pages/LoginPage.jsx
// src/pages/LoginPage.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  // التحقق من وجود توكن بالفعل
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/');
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Veuillez remplir tous les champs');
      return;
    }

    try {
      setLoading(true);

      const response = await fetch('http://127.0.0.1:8000/users/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email,
          password: password
        }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        navigate('/');
        window.location.reload();
      } else {
        setError(data.error || 'Email ou mot de passe incorrect');
      }

    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-background"></div>
      
      <div className="login-card">
        <div className="login-header">
          <h1 className="login-title">
            <span className="title-gradient">Bienvenue</span>
          </h1>
          <p className="login-subtitle">Connectez-vous pour accéder à votre espace</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nom d'utilisateur ou Email</label>
            <div className="input-icon">
              <span className="input-icon-symbol">👤</span>
              <input
                type="text"
                className="login-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="exemple@email.com"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Mot de passe</label>
            <div className="input-icon">
              <span className="input-icon-symbol">🔒</span>
              <input
                type={showPassword ? 'text' : 'password'}
                className="login-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
              <span
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? '🙈' : '👁️'}
              </span>
            </div>
          </div>

          {error && (
            <div className="login-error">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? (
              <span className="loading-spinner"></span>
            ) : (
              'Se connecter'
            )}
            {!loading && <span className="button-arrow">→</span>}
          </button>
        </form>

        <div className="login-divider">
          <span>ou</span>
        </div>

        <div className="login-footer">
          <p>
            Pas encore de compte ? <Link to="/register">Créer un compte</Link>
          </p>
          <Link to="/forgot-password" className="forgot-link">
            Mot de passe oublié ?
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;