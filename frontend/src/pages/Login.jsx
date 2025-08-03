import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeSlash } from '@phosphor-icons/react';
import { jwtDecode } from 'jwt-decode';
import styles from '../common/styles/Login.module.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/jwt/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        throw new Error('Las credenciales proporcionadas son incorrectas.');
      }

      const data = await response.json();

      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);

      const decodedToken = jwtDecode(data.access);

      console.log('Token decodificado:', decodedToken);

      const userType = decodedToken.tipo_usuario;

      if (userType === 'paciente') {
        navigate('/dashboard-paciente');
      } else if (userType === 'medico') {
        navigate('/dashboard-medico');
      } else if (userType === 'enfermera') {
        navigate('/dashboard-enfermera');
      } else {

        console.error('Tipo de usuario no reconocido:', userType);
        navigate('/');
      }

    } catch (error) {
      console.error("Error al iniciar sesión:", error.message);
    }
  };

  const handleNavigateToRegister = () => {
    navigate('/');
  };

  return (
    <div className={styles["login"]}>
      <div className={styles["login__tarjeta"]}>
        <h1 className={styles.login__titulo}>Bienvenido de nuevo</h1>

        <form onSubmit={handleSubmit} className={styles["login__formulario"]}>
          <div className={styles["login__grupo-input"]}>
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

          <div className={styles["login__grupo-input"]}>
            <label htmlFor="password">Contraseña</label>
            <div className={styles["login__contenedor-password"]}>
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Más de 12 caracteres"
                required
              />
              <span
                className={styles["login__icono-password"]}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeSlash size={22} /> : <Eye size={22} />}
              </span>
            </div>
          </div>

          <button type="submit" className={styles["login__boton"]}>
            Iniciar sesión
          </button>
          {error && <p className={styles.login__mensaje_error}>{error}</p>}
        </form>
        <button
          type="button"
          onClick={handleNavigateToRegister}
          className={styles.login__boton}
        >
          Registrarse
        </button>
      </div>
    </div>
  );
}