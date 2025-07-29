import React, { useState } from 'react';
import NotificationButton from '../features/feature_Grupo3_Recordatorios/components/notificationPanel/NotificationButton';
import ModalNotifications from '../features/feature_Grupo3_Recordatorios/components/notificationPanel/ModalNotifications';
import AlertPopup from '../features/feature_Grupo3_Recordatorios/components/notification/AlertPopup';
import ReminderPopup from '../features/feature_Grupo3_Recordatorios/components/notification/ReminderPopup';

function Login() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAlertOpen, setIsAlertOpen] = useState(false);
  const [isReminderOpen, setIsReminderOpen] = useState(false);
  const [notificationCount] = useState(3);
  const [medicationMessage] = useState("Toma 1 píldora de 400mg de Ibuprofeno");
  const [reminderType, setReminderType] = useState("medicina");
  const [reminderMessage, setReminderMessage] = useState("Toma Ibuprofeno a las 13:00 horas");

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleShowAlert = () => {
    setIsAlertOpen(true);
  };

  const handleShowMedicineReminder = () => {
    setReminderType("medicina");
    setReminderMessage("Toma Ibuprofeno a las 13:00 horas");
    setIsReminderOpen(true);
  };

  const handleShowRecommendationReminder = () => {
    setReminderType("recomendacion");
    setReminderMessage("Evita exponerte a sonidos fuertes");
    setIsReminderOpen(true);
  };

  const handleConfirmMedication = () => {
    console.log('Medicación confirmada');
    setIsAlertOpen(false);
  };

  const handleCancelMedication = () => {
    console.log('Medicación no tomada');
    setIsAlertOpen(false);
  };

  const handleCloseReminder = () => {
    setIsReminderOpen(false);
  };

  return (
    <>
      <div style={{ position: 'relative', minHeight: '100vh' }}>
        <h1>Login</h1>
        <button className="btn-primary">Login</button>
        
        <button onClick={handleShowAlert} className="btn-primary" style={{ marginLeft: '10px' }}>
          Mostrar Alerta
        </button>

        <button onClick={handleShowMedicineReminder} className="btn-primary" style={{ marginLeft: '10px' }}>
          Recordatorio Medicina
        </button>

        <button onClick={handleShowRecommendationReminder} className="btn-primary" style={{ marginLeft: '10px' }}>
          Recordatorio Recomendación
        </button>
        
        <NotificationButton 
          onClick={handleOpenModal} 
          hasNotifications={notificationCount > 0}
          notificationCount={notificationCount}
        />
      </div>

      <ModalNotifications 
        isOpen={isModalOpen} 
        onClose={handleCloseModal} 
      />

      <AlertPopup
        isOpen={isAlertOpen}
        onConfirm={handleConfirmMedication}
        onCancel={handleCancelMedication}
        message={medicationMessage}
      />

      <ReminderPopup
        isOpen={isReminderOpen}
        onClose={handleCloseReminder}
        type={reminderType}
        message={reminderMessage}
      />
    </>
  );
}

export default Login;
