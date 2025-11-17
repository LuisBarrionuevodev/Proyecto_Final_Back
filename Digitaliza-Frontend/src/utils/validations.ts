import type { IActuacion } from "../types/actuaciones";
import type { IRelevamiento } from "../types/relevamientos";

const isRequired = (value: unknown) =>
  typeof value === "string"
    ? value.trim().length > 0
    : value !== undefined && value !== null;

const isNumber = (value: unknown) =>
  value !== null && value !== undefined && value !== "" && !isNaN(Number(value));

// Fecha YYYY-MM-DD
const isValidDate = (value: string) =>
  /^\d{4}-\d{2}-\d{2}$/.test(value);

const isValidRealDate = (value: string) => {
  const d = new Date(value);
  return !isNaN(d.getTime()) && value === d.toISOString().split('T')[0];
};




// Validaciones Actuaciones

export const validateActuacion = (a: Partial<IActuacion>) => {
  const errors: Record<string, string | undefined> = {};

  if (!isRequired(a.rubro)) errors.rubro = "Rubro requerido";
  if (a.rubro && a.rubro.length > 20) errors.rubro = "Rubro demasiado largo";
  if (!isNumber(a.distrito)) errors.distrito = "Distrito inválido";
  if (a.distrito && (Number(a.distrito) < 1 || Number(a.distrito) > 10)) errors.distrito = "Distrito fuera de rango (1-10)";
  if (!isRequired(a.inspector1)) errors.inspector1 = "Inspector requerido";
  if (a.inspector1 && a.inspector1.length > 20) errors.inspector1 = "Nombre demasiado largo";
  if (!isRequired(a.inspector2)) errors.inspector2 = "Inspector requerido";
  if (!isRequired(a.inspector3)) errors.inspector3 = "Inspector requerido";
  if (!isRequired(a.direccion)) errors.direccion = "Dirección requerida";
  if (!isNumber(a.clausuras)) errors.clausuras = "Clausuras inválidas";

  return errors;
};


// Validaciones Relevamientos

export const validateRelevamiento = (r: IRelevamiento) => {
  const errors: Record<string, string | undefined> = {};

  if (!isValidDate(r.fecha))
    errors.fecha = "Formato de fecha incorrecto (YYYY-MM-DD)";

  if (!isValidRealDate(r.fecha))
    errors.fecha = "Fecha inválida";

  if (!isRequired(r.inspector))
    errors.inspector = "Ingresa un inspector";

  if (!isRequired(r.direccion))
    errors.direccion = "Dirección requerida";

  if (!isRequired(r.rubro))
    errors.rubro = "Rubro requerido";

  return errors;
};
