import React from "react";
import "../styles/ConfirmacionCancelar.css";

function ConfirmacionCancelar({ onClose }) {
    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h3>¿Está seguro de cancelar la cita en curso?</h3>
                <div className="modal-buttons">
                    <button className="button-confirm-cancelar">Sí</button>
                    <button className="button-cancel-confirmacion" onClick={onClose}>No</button>
                </div>
            </div>
        </div>
    );
}

export default ConfirmacionCancelar;
