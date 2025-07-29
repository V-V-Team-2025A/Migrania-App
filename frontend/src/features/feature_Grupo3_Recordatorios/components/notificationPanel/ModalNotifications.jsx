import React, { useState } from 'react';
import { AlarmIcon, LightbulbFilamentIcon, SirenIcon } from '@phosphor-icons/react';
import Notificacion from './Notification';
import ConfigurationButtons from './ConfigurationButtons';
import styles from './ModalNotifications.module.css';

const ModalNotifications = ({ isOpen, onClose }) => {
  const [estadoNotificaciones, setEstadoNotificaciones] = useState('sonido');

  const notificaciones = [
    {
      id: 1,
      tipo: 'medicacion',
      titulo: 'Es hora de prepararte para tu medicación',
      mensaje: 'Toma Ibuprofeno a las 13:00 horas',
      tiempo: '2m',
      icono: <AlarmIcon size={32} color="#bad8ecff" weight="fill" />
    },
    {
      id: 2,
      tipo: 'recordatorio',
      titulo: 'Recuerda:',
      mensaje: 'Evita exponerte a sonidos fuertes',
      tiempo: '8m',
      icono: <LightbulbFilamentIcon size={32} color="#f5e400ff" weight="fill" />
    },
    {
      id: 3,
      tipo: 'alerta',
      titulo: 'No has confirmado la toma',
      mensaje: 'Te has olvidado la primera alerta a las 13:00h',
      tiempo: '12m',
      icono: <SirenIcon size={32} color="#AA4D53" weight="fill" />
    }
  ];

  const handleSonido = () => setEstadoNotificaciones('sonido');
  const handleSilenciar = () => setEstadoNotificaciones('silencio');
  const handleSuspender = () => setEstadoNotificaciones('suspender');

  const handleBorrarTodo = () => {
    console.log('Borrando todas las notificaciones');
  };

  if (!isOpen) return null;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2 className={styles.titulo}>Notificaciones</h2>
        </div>

        <ConfigurationButtons 
          onSonido={handleSonido}
          onSilenciar={handleSilenciar}
          onSuspender={handleSuspender}
          estadoActual={estadoNotificaciones}
        />

        <div className={styles.notificacionesList}>
          {notificaciones.map(notificacion => (
            <Notificacion 
              key={notificacion.id}
              tipo={notificacion.tipo}
              titulo={notificacion.titulo}
              mensaje={notificacion.mensaje}
              tiempo={notificacion.tiempo}
              icono={notificacion.icono}
            />
          ))}
        </div>

        <button className={styles.borrarTodoBtn} onClick={handleBorrarTodo}>
          Borrar todo
        </button>
      </div>
    </div>
  );
};

export default ModalNotifications;