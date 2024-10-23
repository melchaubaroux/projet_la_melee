'use client'

import React from 'react';
import { CgOverflow } from 'react-icons/cg';

// Composant Box qui encadre son contenu
const Box = ({ children, title }) => {
  return (
    <div style={boxStyle}>
      {title && <h2 style={titleStyle}>{title}</h2>}
      <div style={contentStyle}>
        {children}
      </div>
    </div>
  );
};


// Styles pour le Box
const boxStyle = {
  border: '2px solid #ccc',  // Bordure grise
  borderRadius: '8px',       // Coins arrondis
  padding: '10px',           // Espacement intérieur
  marginBottom: '10px',      // Espacement extérieur
  boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',  // Ombre légère
  backgroundColor: '#f9f9f9' ,// Couleur de fond légère
  overflowY: 'auto',
  width: '400px', // Largeur fixe
  height: '300px', // Hauteur fixe

};

const titleStyle = {
  marginBottom: '10px',
  fontSize: '18px',
  color: '#333',
};

const contentStyle = {
  padding: '10px',
  backgroundColor: '#fff',
  borderRadius: '5px',
  border: '1px solid #ddd',
  overflow: 'auto',
  flex : 'auto',
};

export default Box;

