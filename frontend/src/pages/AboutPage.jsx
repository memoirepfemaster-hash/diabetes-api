// src/pages/AboutPage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './AboutPage.css';

const AboutPage = () => {
  return (
    <div className="about-page">

      {/* NAVBAR */}
      <nav className="about-navbar">
        <div className="about-navbar-container">
          <Link to="/" className="about-logo">
            <span className="logo-icon">💉</span>
            <span className="logo-text">DiabCare</span>
          </Link>

          <Link to="/" className="back-home-btn">
            ← Retour à l'accueil
          </Link>
        </div>
      </nav>

      {/* HERO */}
      <div className="about-hero">
        <h1 className="hero-gradient">Comprendre le diabète</h1>
      </div>

      {/* CONTENT */}
      <div className="about-main">
        <div className="about-section">
          
          <div className="section-icon">📖</div>

          <h2>Qu'est-ce que le diabète ?</h2>

          <div className="section-divider"></div>

          <div className="definition-text">

            <p>
              Le diabète est une maladie chronique où le corps a du mal à réguler le taux de sucre (glucose) dans le sang. 
              Normalement, après un repas, le glucose provenant de la digestion des aliments passe dans le sang. 
              En réponse, le pancréas sécrète une hormone appelée insuline, qui agit comme une clé permettant au glucose 
              d'entrer dans les cellules (muscles, foie, tissu adipeux) pour être utilisé comme source d'énergie ou stocké 
              pour plus tard. Dans le diabète, ce système de régulation est défaillant : soit le pancréas ne produit pas 
              assez d'insuline, soit les cellules de l'organisme deviennent résistantes à son action (ou les deux à la fois). 
              En conséquence, le glucose reste bloqué dans le sang, ce qui entraîne une hyperglycémie chronique.
            </p>

            <p>
              Cette hyperglycémie persistante est toxique pour l'organisme à long terme. Elle endommage progressivement 
              les vaisseaux sanguins. Si la maladie n'est pas bien contrôlée, elle peut entraîner de graves complications : 
              au niveau des yeux (rétinopathie), des reins (néphropathie), des nerfs (neuropathie), ainsi qu’un risque élevé 
              de maladies cardiovasculaires comme l'infarctus ou l’AVC.
            </p>

            <p>
              En résumé, le diabète est un trouble chronique de la régulation du sucre sanguin. Un contrôle rigoureux de la 
              glycémie et une surveillance médicale régulière sont essentiels pour prévenir ces complications.
            </p>

          </div>

        </div>
      </div>
      {/* ================= VIDEO SECTION ================= */}
<div className="about-video-section">
  <div className="section-icon">🎥</div>
  <h2>Regardez la vidéo explicative du DT2</h2>
  <div className="section-divider"></div>
  
  <div className="video-container">
    <video 
      controls 
      autoPlay={false}
      className="about-video"
      poster="/src/assets/vid.jpg"  // اختياري: صورة مصغرة للفيديو
    >
      <source src="/src/assets/video.mp4" type="video/mp4" />
      Votre navigateur ne supporte pas la lecture de vidéos.
    </video>
  </div>
</div>

      {/* FOOTER */}
      <footer className="about-footer">
        <p>© 2026 - DIABETES CARE</p>
      </footer>

    </div>
  );
};

export default AboutPage;