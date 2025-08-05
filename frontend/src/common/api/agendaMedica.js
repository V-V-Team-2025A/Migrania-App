export async function obtenerCitasMensuales(year, month) {
  // Mock temporal
  return {
    citas: [
      {
        fecha: `${year}-${String(month).padStart(2, "0")}-01`,
        doctor: "Dr. Juan Guarnizo",
        hora: "09:00 A.M.",
      },
      {
        fecha: `${year}-${String(month).padStart(2, "0")}-11`,
        doctor: "Dr. Juan Guarnizo",
        hora: "09:00 A.M.",
      },
    ],
  };
}

export async function obtenerCitasSemanales(year, month, day) {
  // Mock temporal :
  return {
    citas: [
      {
        fecha: `${year}-${String(month).padStart(2, "0")}-${String(
          day
        ).padStart(2, "0")}`,
        doctor: "Dr. Juan Guarnizo",
        hora: "09:00 A.M.",
      },
      {
        fecha: `${year}-${String(month).padStart(2, "0")}-${String(
          day + 2
        ).padStart(2, "0")}`,
        doctor: "Dr. Juan Guarnizo",
        hora: "11:00 A.M.",
      },
    ],
  };
}

export async function obtenerCitasSemanalesPaciente(year, month, day) {
  // Ajustar
  const res = await fetch(
    `/api/paciente/citas/semana?year=${year}&month=${month}&day=${day}`
  );
  if (!res.ok) throw new Error("Error al obtener citas semanales del paciente");
  return await res.json();
}

export async function obtenerCitasMensualesPaciente(year, month) {
  // Ajustad
  const res = await fetch(
    `/api/paciente/citas/mes?year=${year}&month=${month}`
  );
  if (!res.ok) throw new Error("Error al obtener citas mensuales del paciente");
  return await res.json();
}
