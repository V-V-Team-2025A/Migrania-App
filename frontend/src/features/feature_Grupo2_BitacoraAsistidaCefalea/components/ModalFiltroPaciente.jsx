import React, { useState } from 'react';
import styles from '../styles/modalFiltro.module.css';

export default function ModalFiltroPaciente({ onConfirm, onCancel }) {
    const [filtros, setFiltros] = useState({
        categoria: "",
        severidad: "",
        conAura: null
    });

    const categoriasDiagnosticas = [
        "Migraña sin aura",
        "Migraña con aura",
        "Cefalea de tipo tensional"
    ];

    const nivelasSeveridad = [
        "Leve",
        "Moderado",
        "Severo"
    ];

    const handleCategoriaChange = (e) => {
        setFiltros(prev => ({
            ...prev,
            categoria: e.target.value
        }));
    };

    const handleSeveridadChange = (e) => {
        setFiltros(prev => ({
            ...prev,
            severidad: e.target.value
        }));
    };

    const handleAuraChange = (e) => {
        const value = e.target.value;
        setFiltros(prev => ({
            ...prev,
            conAura: value === "" ? null : value === "true"
        }));
    };

    const handleConfirm = () => {
        onConfirm(filtros);
    };

    const handleLimpiar = () => {
        setFiltros({
            categoria: "",
            severidad: "",
            conAura: null
        });
    };

    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modalContent}>
                <div className={styles.modalHeader}>
                    <h3>Filtrar Episodios</h3>
                </div>
                
                <div className={styles.modalBody}>
                    <div className={styles.filterGroup}>
                        <label htmlFor="categoria">Categoría Diagnosticada:</label>
                        <select
                            id="categoria"
                            value={filtros.categoria}
                            onChange={handleCategoriaChange}
                            className={styles.selectFilter}
                        >
                            <option value="">Todas las categorías</option>
                            {categoriasDiagnosticas.map(categoria => (
                                <option key={categoria} value={categoria}>
                                    {categoria}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className={styles.filterGroup}>
                        <label htmlFor="severidad">Severidad:</label>
                        <select
                            id="severidad"
                            value={filtros.severidad}
                            onChange={handleSeveridadChange}
                            className={styles.selectFilter}
                        >
                            <option value="">Todas las severidades</option>
                            {nivelasSeveridad.map(severidad => (
                                <option key={severidad} value={severidad}>
                                    {severidad}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className={styles.filterGroup}>
                        <label htmlFor="aura">Presencia de Aura:</label>
                        <select
                            id="aura"
                            value={filtros.conAura === null ? "" : filtros.conAura.toString()}
                            onChange={handleAuraChange}
                            className={styles.selectFilter}
                        >
                            <option value="">Todos</option>
                            <option value="true">Con aura</option>
                            <option value="false">Sin aura</option>
                        </select>
                    </div>
                </div>

                <div className={styles.modalFooter}>
                    <button 
                        className={styles.clearButton}
                        onClick={handleLimpiar}
                    >
                        Limpiar
                    </button>
                    <button 
                        className={styles.cancelButton}
                        onClick={onCancel}
                    >
                        Cancelar
                    </button>
                    <button 
                        className={styles.confirmButton}
                        onClick={handleConfirm}
                    >
                        Aplicar Filtros
                    </button>
                </div>
            </div>
        </div>
    );
}
