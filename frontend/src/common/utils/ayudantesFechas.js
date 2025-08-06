/**
 * Devuelve el lunes de la semana de una fecha dada.
 * @param {Date} fecha
 * @returns {Date}
 */
export function obtenerLunes(fecha) {
  const d = new Date(fecha);
  const dia = d.getDay() || 7;
  if (dia !== 1) d.setHours(-24 * (dia - 1));
  return d;
}

/**
 * Devuelve un arreglo con las fechas de la semana (lunes a domingo) de una fecha dada.
 * @param {Date} fecha
 * @returns {Date[]}
 */
export function obtenerFechasSemana(fecha) {
  const lunes = obtenerLunes(fecha);
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(lunes);
    d.setDate(lunes.getDate() + i);
    return d;
  });
}

/**
 * Genera la matriz de días para un mes, incluyendo días del mes anterior y siguiente para completar las filas.
 * @param {number} anio
 * @param {number} mes (0 = enero, 11 = diciembre)
 * @param {Array} citas
 * @returns {Array}
 */
export function generarMatrizMes(anio, mes, citas = []) {
  const primerDia = new Date(anio, mes, 1);
  const ultimoDia = new Date(anio, mes + 1, 0);
  const ultimoDiaMesAnterior = new Date(anio, mes, 0);

  let matriz = [];
  let semana = [];
  let diaSemana = primerDia.getDay() === 0 ? 6 : primerDia.getDay() - 1;

  // Días del mes anterior
  for (let i = 0; i < diaSemana; i++) {
    semana.push({
      numero: ultimoDiaMesAnterior.getDate() - diaSemana + i + 1,
      tipo: "anterior",
      citas: [],
    });
  }

  // Días del mes actual
  for (let d = 1; d <= ultimoDia.getDate(); d++) {
    const fechaStr = `${anio}-${String(mes + 1).padStart(2, "0")}-${String(
      d
    ).padStart(2, "0")}`;
    const citasDia = citas.filter((c) => c.fecha === fechaStr);
    semana.push({ numero: d, tipo: "actual", citas: citasDia });
    if (semana.length === 7) {
      matriz.push(semana);
      semana = [];
    }
  }

  // Días del mes siguiente
  let siguienteDia = 1;
  while (semana.length < 7) {
    semana.push({ numero: siguienteDia++, tipo: "siguiente", citas: [] });
  }
  matriz.push(semana);

  // Completar hasta 6 filas
  while (matriz.length < 6) {
    let semanaVacia = [];
    for (let i = 0; i < 7; i++) {
      semanaVacia.push({ numero: "", tipo: "vacio", citas: [] });
    }
    matriz.push(semanaVacia);
  }

  return matriz;
}
