import React from 'react';
import { LightbulbFilamentIcon, InfoIcon, X } from '@phosphor-icons/react';
import styles from './ReminderPopup.module.css';

const ReminderPopup = ({ 
  isOpen, 
  onClose,
  type,
  message
}) => {
  if (!isOpen) return null;

  // Configuración según el tipo
  const getConfig = () => {
    switch (type) {
      case "recomendacion":
        return {
          title: "Recuerda seguir las recomendaciones",
          icon: <InfoIcon size={64} color="var(--secondary-light)" weight="fill" />
        };
      case "medicina":
      default:
        return {
          title: "Es hora de prepararte para tu medicación",
          icon: <LightbulbFilamentIcon size={64} color="var(--secondary-light)" weight="fill" />
        };
    }
  };

  const config = getConfig();

  return (
    <div className={styles.overlay}>
      <div className={styles.popup}>
        <button 
          className={styles.closeBtn}
          onClick={onClose}
          title="Cerrar"
        >
          <X size={24} color="var(--color-text)" weight="bold" />
        </button>
        
        <div>
          {config.icon}
        </div>
        
        <div className={styles.content}>
          <h3 className={styles.title}>{config.title}</h3>
          <p className={styles.message}>{message}</p>
        </div>
      </div>
    </div>
  );
};

export default ReminderPopup;