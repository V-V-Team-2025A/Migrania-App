import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Eye, EyeSlash } from '@phosphor-icons/react';
import styles from '../styles/Registro.module.css';

export default function Registro() {
    const [nombre, setNombre] = useState('');
    const [apellido, setApellido] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log("Intentando registrarse con:", { nombre, apellido, email, password });
    };

    return (
        <div className={styles["registro"]}>
            <div className={styles["registro__tarjeta"]}>
                <h1 className={styles.registro__titulo}>Regístrate</h1>

                <form onSubmit={handleSubmit} className={styles["registro__formulario"]}>
                    <div className={styles["registro__grupo-input"]}>
                        <label htmlFor="nombre">Nombre</label>
                        <input
                            type="text"
                            id="nombre"
                            value={nombre}
                            onChange={(e) => setNombre(e.target.value)}
                            placeholder="nombre"
                            required
                        />
                    </div>

                    <div className={styles["registro__grupo-input"]}>
                        <label htmlFor="apellido">Apellido</label>
                        <input
                            type="text"
                            id="apellido"
                            value={apellido}
                            onChange={(e) => setApellido(e.target.value)}
                            placeholder="apellido"
                            required
                        />
                    </div>

                    <div className={styles["registro__grupo-input"]}>
                        <label htmlFor="email">Dirección de correo electrónico</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Por ejemplo: john@company.com"
                            required
                        />
                    </div>

                    <div className={styles["registro__grupo-input"]}>
                        <label htmlFor="password">Contraseña</label>
                        <div className={styles["registro__contenedor-password"]}>
                            <input
                                type={showPassword ? 'text' : 'password'}
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Más de 12 caracteres"
                                required
                            />
                            <span
                                className={styles["registro__icono-password"]}
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? <EyeSlash size={22} /> : <Eye size={22} />}
                            </span>
                        </div>
                    </div>

                    <button type="submit" className={styles["registro__boton"]}>
                        Registrarse
                    </button>
                </form>
            </div>
        </div>
    );
}