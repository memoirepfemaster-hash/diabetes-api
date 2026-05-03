// src/App.jsx
// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import HomePage from './pages/HomePage';
import PredictionPage from './pages/PredictionPage';
import LoginPage from './pages/LoginPage';
import PrivateRoute from './components/PrivateRoute';
import './App.css';
import RegisterPage from './pages/RegisterPage';
import AboutPage from './pages/AboutPage'; 

function App() {
  const token = localStorage.getItem('token');

  return (
    <Router>
      <div className="App">

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/register" element={<RegisterPage />} />
           <Route path="/about" element={<AboutPage />} />
          <Route
            path="/predict"
            element={
              <PrivateRoute>
                <PredictionPage />
              </PrivateRoute>
            }
          />

          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;