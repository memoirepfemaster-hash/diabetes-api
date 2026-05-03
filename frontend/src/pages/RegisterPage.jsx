// src/pages/RegisterPage.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './RegisterPage.css';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);
  
  const navigate = useNavigate();

  // التحقق من وجود توكن بالفعل
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/');
    }
  }, [navigate]);

  // حساب قوة كلمة المرور
  const checkPasswordStrength = (pwd) => {
    let strength = 0;
    if (pwd.length >= 6) strength++;
    if (pwd.length >= 10) strength++;
    if (/[A-Z]/.test(pwd)) strength++;
    if (/[0-9]/.test(pwd)) strength++;
    if (/[^A-Za-z0-9]/.test(pwd)) strength++;
    setPasswordStrength(strength);
  };

  const handlePasswordChange = (e) => {
    const pwd = e.target.value;
    setPassword(pwd);
    checkPasswordStrength(pwd);
  };

  const getStrengthText = () => {
    if (passwordStrength <= 2) return 'Faible';
    if (passwordStrength <= 4) return 'Moyen';
    return 'Fort';
  };

  const getStrengthColor = () => {
    if (passwordStrength <= 2) return '#ff6b6b';
    if (passwordStrength <= 4) return '#ffd93d';
    return '#4fd1c5';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!username || !email || !password || !confirmPassword) {
      setError('Veuillez remplir tous les champs');
      return;
    }

    if (password !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }

    if (password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }

    try {
      setLoading(true);

      const response = await fetch('http://127.0.0.1:8000/users/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        navigate('/login');
      } else {
        setError(data.error || "Erreur lors de l'inscription");
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-background"></div>
      
      <div className="register-card">
        <div className="register-header">
          <h1 className="register-title">
            <span className="title-gradient">Créer un compte</span>
          </h1>
          <p className="register-subtitle">Rejoignez DiabCare pour commencer</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nom d'utilisateur</label>
            <div className="input-icon">
              <span className="input-icon-symbol">👤</span>
              <input
                type="text"
                className="register-input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="ex: john_doe"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Email</label>
            <div className="input-icon">
              <span className="input-icon-symbol">📧</span>
              <input
                type="email"
                className="register-input"
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
                className="register-input"
                value={password}
                onChange={handlePasswordChange}
                placeholder="••••••••"
              />
              <span
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? '🙈' : '👁️'}
              </span>
            </div>
            {password && (
              <div className="password-strength">
                <div className="strength-bar">
                  <div 
                    className="strength-fill" 
                    style={{ 
                      width: `${(passwordStrength / 5) * 100}%`,
                      backgroundColor: getStrengthColor()
                    }}
                  ></div>
                </div>
                <span className="strength-text" style={{ color: getStrengthColor() }}>
                  Force: {getStrengthText()}
                </span>
              </div>
            )}
          </div>

          <div className="form-group">
            <label>Confirmer le mot de passe</label>
            <div className="input-icon">
              <span className="input-icon-symbol">✓</span>
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                className="register-input"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
              />
              <span
                className="password-toggle"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? '🙈' : '👁️'}
              </span>
            </div>
          </div>

          {error && (
            <div className="register-error">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <button type="submit" className="register-button" disabled={loading}>
            {loading ? (
              <>
                <span className="loading-spinner"></span>
                Inscription en cours...
              </>
            ) : (
              <>
                <span>✨</span>
                S'inscrire
                <span>→</span>
              </>
            )}
          </button>
        </form>

        <div className="register-divider">
          <span>ou</span>
        </div>

        <div className="register-footer">
          <p>
            Déjà un compte ? <Link to="/login">Se connecter</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;