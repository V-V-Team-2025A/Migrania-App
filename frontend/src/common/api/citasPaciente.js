export async function getCitasPaciente() {
  // Mock temporal
  return {
    proximas: [
      {
        id: 1,
        doctor: "Dr. Juan Guarnizo",
        fecha: "2025-07-23",
        hora: "09:00 A.M.",
      },
      {
        id: 2,
        doctor: "Dr. Juan Guarnizo",
        fecha: "2025-08-19",
        hora: "11:00 A.M.",
      },
    ],
    historial: [
      {
        id: 3,
        doctor: "Dr. Juan Guarnizo",
        fecha: "2025-07-01",
        hora: "01:00 P.M.",
        estado: "Asistido",
      },
      {
        id: 4,
        doctor: "Dr. Raúl Álvarez",
        fecha: "2025-06-13",
        hora: "04:00 P.M.",
        estado: "Cancelado",
      },
    ],
  };
}

export async function crearCitaPaciente(data) {
  // Mock temporal
  return { ok: true };
}
