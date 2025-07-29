import React from 'react';
import { AlarmIcon } from '@phosphor-icons/react';
import styles from './AlertPopup.module.css';

const AlertPopup = ({ 
  isOpen, 
  onConfirm, 
  onCancel, 
  title = "¿Tomaste la medicación?",
  message,
  confirmText = "SÍ",
  cancelText = "NO"
}) => {
  if (!isOpen) return null;

  return (
    <div className={styles.overlay}>
      <div className={styles.popup}>
        <div className={styles.iconContainer}>
          <AlarmIcon size={64} color="var(--secondary-light)" weight="fill" />
        </div>
        
        <div className={styles.content}>
          <h3 className={styles.title}>{title}</h3>
          <p className={styles.message}>{message}</p>
        </div>
        
        <div className={styles.buttonContainer}>
          <button 
            className={styles.confirmBtn}
            onClick={onConfirm}
          >
            {confirmText}
          </button>
          
          <button 
            className={styles.cancelBtn}
            onClick={onCancel}
          >
            {cancelText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AlertPopup;