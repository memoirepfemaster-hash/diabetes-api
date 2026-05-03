// src/pages/HomePage.jsx
// src/pages/HomePage.jsx
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Link, useNavigate } from "react-router-dom";
import './HomePage.css';
// استيراد Recharts
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';

// بيانات الرسم البياني
const chartData = [
  { day: "Lun", sugar: 120 },
  { day: "Mar", sugar: 135 },
  { day: "Mer", sugar: 110 },
  { day: "Jeu", sugar: 140 },
  { day: "Ven", sugar: 125 },
  { day: "Sam", sugar: 150 },
  { day: "Dim", sugar: 130 }
];

// بيانات المضاعفات
const complications = [
  {
    icon: "👁️",
    title: "Rétinopathie",
    desc: "Atteinte des vaisseaux de la rétine pouvant entraîner une perte de vision.",
    symptoms: ["Vision floue", "Taches noires", "Perte de vision"]
  },
  {
    icon: "❤️",
    title: "Maladies cardiaques",
    desc: "Risque élevé de crise cardiaque et d'accident vasculaire cérébral.",
    symptoms: ["Douleur thoracique", "Essoufflement", "Fatigue"]
  },
  {
    icon: "🧬",
    title: "Néphropathie",
    desc: "Détérioration progressive des reins liée à une glycémie élevée.",
    symptoms: ["Fatigue", "Œdème", "Urines fréquentes"]
  },
  {
    icon: "⚡",
    title: "Neuropathie",
    desc: "Atteinte des nerfs causant douleurs et engourdissements.",
    symptoms: ["Picotements", "Brûlures", "Perte de sensibilité"]
  },
  {
    icon: "🦶",
    title: "Pied diabétique",
    desc: "Plaies difficiles à cicatriser pouvant entraîner des infections.",
    symptoms: ["Plaies", "Infection", "Douleur"]
  },
  {
    icon: "🧠",
    title: "Complications cérébrales",
    desc: "Augmentation du risque d'AVC et troubles cognitifs.",
    symptoms: ["Maux de tête", "Perte mémoire", "Faiblesse"]
  }
];

const HomePage = () => {
  const [token, setToken] = useState(null);
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [currentImage, setCurrentImage] = useState(0);
  const [imageError, setImageError] = useState(false);
  
  const navigate = useNavigate();
  const imageIntervalRef = useRef(null);

  // Refs للأقسام المختلفة
  const aboutRef = useRef(null);      // قسم "ما هو مرض السكري"
  const typesRef = useRef(null);      // قسم "أنواع السكري"
  const complicationsRef = useRef(null); // قسم "مضاعفات السكري"
  const tipsRef = useRef(null);       // قسم "النصائح"
  const dashboardRef = useRef(null);  // قسم "الرسم البياني"

  // صور الهيدر
  const images = [
    "https://images.unsplash.com/photo-1579684385127-1ef15d508118",
    "https://cdn4.premiumread.com/?url=https://akhbaar24.com/akhbar24/uploads/images/2025/12/15/9501859.jpeg&w=1164&q=95&f=webp&t=1",
    "https://24.ae/images/templates/2023/2024220195325947DT.png"
  ];

  // دالة التمرير السلس إلى القسم
  const scrollToSection = useCallback((ref) => {
    if (ref && ref.current) {
      const navbarHeight = 80;
      const elementPosition = ref.current.offsetTop - navbarHeight;
      
      window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
      });
    }
    setMenuOpen(false);
  }, []);

  // قراءة التوكن
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    setToken(storedToken);
  }, []);

  // تأثير التمرير
  useEffect(() => {
  const handleScroll = () => {
    setScrolled(window.scrollY > 50);
  };
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
  // تغيير الصور
  useEffect(() => {
    imageIntervalRef.current = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 3000);

    return () => {
      if (imageIntervalRef.current) {
        clearInterval(imageIntervalRef.current);
      }
    };
  }, [images.length]);

  // تأثير ظهور البطاقات
  useEffect(() => {
    const cards = document.querySelectorAll(".tip-card");
    
    if (cards.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    cards.forEach((card) => observer.observe(card));

    return () => observer.disconnect();
  }, []);

  const handleLogout = useCallback(() => {
    localStorage.removeItem('token');
    setToken(null);
    navigate('/');
    window.location.reload();
  }, [navigate]);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <div className="homepage">

      {/* ================= HEADER ================= */}
      <header
        className="header"
        style={{ 
          backgroundImage: !imageError ? `url(${images[currentImage]})` : 'none',
          backgroundColor: imageError ? '#0a0f2c' : 'transparent'
        }}
      >
        <div className="header-overlay"></div>
        {/* ================= NAVBAR ================= */}
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
          <div className="logo">
            <span className="logo-icon">💉</span>
            <span className="logo-text">DiabCare</span>
          </div>

          <div className={`nav-links ${menuOpen ? 'active' : ''}`}>
            {/* Accueil - haut de page */}
            <button 
              onClick={() => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
                setMenuOpen(false);
              }} 
              className="nav-item"
            >
              Accueil
            </button>

            {/* Diabète - section À propos */}
            <button 
              onClick={() => scrollToSection(aboutRef)} 
              className="nav-item"
            >
              Diabète
            </button>

            {/* Types - section Types de diabète */}
            <button 
              onClick={() => scrollToSection(typesRef)} 
              className="nav-item"
            >
              Types
            </button>

            {/* Complications - section Complications */}
            <button 
              onClick={() => scrollToSection(complicationsRef)} 
              className="nav-item"
            >
              Complications
            </button>

            {/* Conseils - section Conseils santé */}
            <button 
              onClick={() => scrollToSection(tipsRef)} 
              className="nav-item"
            >
              Conseils
            </button>

            {/* Evolution - section Dashboard */}
            <button 
              onClick={() => scrollToSection(dashboardRef)} 
              className="nav-item"
            >
              Evolution
            </button>

            {/* Prédiction - page séparée */}
            <Link to="/predict" className="nav-item" onClick={() => setMenuOpen(false)}>
              Prédiction
            </Link>

            {!token ? (
              <Link to="/login" className="btn-login" onClick={() => setMenuOpen(false)}>
                Connexion
              </Link>
            ) : (
              <button className="btn-logout" onClick={handleLogout}>
                Déconnexion
              </button>
            )}
          </div>

          <div className="menu-icon" onClick={toggleMenu}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </nav>

        {/* ================= HEADER CONTENT ================= */}
        <div className="header-content">
          <p className="welcome-small">Bienvenue sur</p>
          <h1>
            Système de Prédiction<br />
            <span className="subtitle-line">du Diabète de Type 2</span>
          </h1>
          <p className="description">
            Entrez vos données de santé et obtenez une prédiction intelligente sur le risque de diabète.
          </p>
          <Link to="/predict">
            <button className="btn-risk">Prédire maintenant</button>
          </Link>
        </div>
      </header>

      {/* ================= SECTION : Qu'est-ce que le diabète ? ================= */}
      <div ref={aboutRef} className="about-wrapper">
        <div className="about-container">
          <div className="about-left">
            <span className="about-tag">À PROPOS DU DIABÈTE</span>
            <h1>Qu'est-ce que <br /><span>le diabète ?</span></h1>
            <p>
              Le diabète est une maladie chronique où le corps a du mal
              à réguler le taux de sucre dans le sang. Cela peut entraîner
              des complications si elle n'est pas bien contrôlée.
            </p>
            <div className="about-buttons">
              <Link to="/about">
  <button className="btn-main">En savoir plus →</button>
</Link>
            </div>
          </div>

          <div className="about-right">
          <img src="/src/assets/image.PNG" alt="Diabetes information"/>
          </div>
        </div>

        <div className="stats">
          <div className="stat">
            <h3>+537M</h3>
            <p>Personnes vivent avec le diabète dans le monde.</p>
          </div>
          <div className="stat">
            <h3>En hausse</h3>
            <p>Le diabète est en constante augmentation depuis des années.</p>
          </div>
          <div className="stat">
            <h3>Prévention</h3>
            <p>Un mode de vie sain peut réduire les risques de complications.</p>
          </div>
          <div className="stat">
            <h3>Soutien</h3>
            <p>Un accompagnement régulier améliore la qualité de vie.</p>
          </div>
        </div>
      </div>

      {/* ================= SECTION : Types de diabète ================= */}
      <section ref={typesRef} className="types-section">
        <div className="types-header">
          <span className="types-tag">INFORMATIONS MÉDICALES</span>
          <h2>Types de diabète</h2>
          <p>Comprenez les différents types de diabète pour mieux prévenir et gérer cette maladie</p>
        </div>

        <div className="types-grid">
          <div className="type-card">
            <div className="type-icon">💉</div>
            <h3>Diabète de type 1</h3>
            <p>Maladie auto-immune où le corps ne produit pas d'insuline.</p>
            <div className="features">
              <h4>Caractéristiques</h4>
              <ul>
                <li>Débute dans l'enfance</li>
                <li>Dépendance à l'insuline</li>
                <li>Non lié au mode de vie</li>
                <li>Surveillance quotidienne</li>
              </ul>
            </div>
          </div>

          <div className="type-card">
            <div className="type-icon">💧</div>
            <h3>Diabète de type 2</h3>
            <p>Le corps n'utilise pas correctement l'insuline.</p>
            <div className="features">
              <h4>Caractéristiques</h4>
              <ul>
                <li>Apparaît à l'âge adulte</li>
                <li>Lié au mode de vie</li>
                <li>Contrôlable</li>
                <li>Le plus fréquent</li>
              </ul>
            </div>
          </div>

          <div className="type-card">
            <div className="type-icon">🤰</div>
            <h3>Diabète gestationnel</h3>
            <p>Se développe pendant la grossesse.</p>
            <div className="features">
              <h4>Caractéristiques</h4>
              <ul>
                <li>Pendant la grossesse</li>
                <li>Temporaire</li>
                <li>Surveillance stricte</li>
                <li>Risque futur</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="types-footer">
          <p>Un diagnostic précoce et une bonne prise en charge sont essentiels pour prévenir les complications.</p>
        </div>
      </section>

      {/* ================= SECTION : Complications ================= */}
      <section ref={complicationsRef} className="complications-section">
        <div className="comp-header">
          <span className="comp-tag">INFORMATIONS MÉDICALES</span>
          <h2>Complications du diabète</h2>
          <p>Le diabète non contrôlé peut entraîner plusieurs complications graves affectant différents organes.</p>
        </div>

        <div className="comp-grid">
          {complications.map((item, index) => (
            <div className="comp-card" key={index}>
              <div className="comp-icon">{item.icon}</div>
              <h3>{item.title}</h3>
              <p>{item.desc}</p>
              <div className="divider"></div>
              <span className="symp-title">Symptômes</span>
              <ul>
                {item.symptoms.map((symptom, i) => (
                  <li key={i}>{symptom}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="comp-footer">
          <div className="footer-icon">🛡️</div>
          <div>
            <h3>Prévention et gestion</h3>
            <p>Une alimentation équilibrée, l'activité physique et un suivi médical régulier permettent de réduire significativement les risques.</p>
          </div>
        </div>
      </section>

      {/* ================= SECTION : Conseils Santé ================= */}
      <section ref={tipsRef} className="tips-section">
        <div className="tips-header">
          <span className="tips-tag">CONSEILS SANTÉ</span>
          <h2>Astuces santé</h2>
          <p>Adoptez de bonnes habitudes pour prévenir et gérer le diabète.</p>
        </div>

        <div className="tips-grid">
          <div className="tip-card">
            <div className="tip-icon nutrition">🥗</div>
            <h3>Nutrition</h3>
            <div className="divider"></div>
            <ul>
              <li>Réduire le sucre</li>
              <li>Manger équilibré</li>
              <li>Favoriser les fibres</li>
            </ul>
          </div>

          <div className="tip-card">
            <div className="tip-icon sport">🏃</div>
            <h3>Sport</h3>
            <div className="divider"></div>
            <ul>
              <li>30 min par jour</li>
              <li>Cardio ou marche</li>
              <li>Régularité importante</li>
            </ul>
          </div>

          <div className="tip-card featured">
            <span className="badge">🔥Recommandée</span>
            <div className="tip-icon lifestyle">🧘</div>
            <h3>Mode de vie</h3>
            <div className="divider"></div>
            <ul>
              <li>Bien dormir</li>
              <li>Gérer le stress</li>
              <li>Suivi médical régulier</li>
            </ul>
          </div>
        </div>
      </section>

      {/* ================= SECTION : Dashboard / Evolution ================= */}
      <section ref={dashboardRef} className="dashboard-section">
        <div className="dashboard-container">
          <div className="dash-header">
            <span className="dash-tag">Tableau de bord</span>
            <h2>Aperçu de votre santé</h2>
          </div>

          <div className="dash-stats">
            <div className="stat-card">
              <h3>120</h3>
              <p>Glucose (mg/dL)</p>
            </div>
            <div className="stat-card">
              <h3>Normal</h3>
              <p>Statut</p>
            </div>
            <div className="stat-card">
              <h3>7</h3>
              <p>Dossiers</p>
            </div>
          </div>

          <div className="dash-card dash-chart">
            <h3>Évolution du Glucose</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="day" stroke="#aaa" />
                <YAxis stroke="#aaa" />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: "#0a0f2c",
                    border: "none",
                    borderRadius: "10px",
                    color: "#fff"
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="sugar"
                  stroke="#7c5cff"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="dash-grid">
            <div className="dash-card">
              <h3>History</h3>
              <ul>
                <li>120 mg/dL - Today</li>
                <li>135 mg/dL - Yesterday</li>
                <li>110 mg/dL - 2 days ago</li>
              </ul>
            </div>
            <div className="dash-card">
              <h3>Personal Tips</h3>
              <ul>
                <li>Drink more water 💧</li>
                <li>Reduce sugar 🍬</li>
                <li>Exercise 🏃</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer className="footer">
        <div className="footer-warning-section">
          <span className="warning-icon">⚠️</span>
          <p>Cet outil est une aide à la décision. Ne remplace pas un avis médical.</p>
        </div>
        <div className="footer-copyright">
          <p>© 2026 - DIABETES CARE - Prédiction du Diabète de Type 2</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;