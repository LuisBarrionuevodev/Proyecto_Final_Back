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

const isValidInputDate = (value?: string) => {
  if (!value) return false;
  const patterns = [
    /^\d{2}\/\d{2}\/\d{2}$/,
    /^\d{2}\/\d{2}\/\d{4}$/,
    /^\d{4}-\d{2}-\d{2}$/,
  ];
  return patterns.some((p) => p.test(value));
};

export const validateActuacion = (
  a: Partial<IActuacion> & {
    inspector1?: string;
    inspector2?: string;
    inspector3?: string;
  },
) => {
  const errors: Record<string, string | undefined> = {};

  if (!isRequired(a.orden_trabajo_numero)) errors.orden_trabajo_numero = "OT requerida";
  if (!isValidInputDate(a.fecha_actuacion)) errors.fecha_actuacion = "Fecha inválida";
  if (!isRequired(a.rubro_nombre)) errors.rubro_nombre = "Rubro requerido";

  const inspectores = (a.inspectores?.length ? a.inspectores : [
    a.inspector1,
    a.inspector2,
    a.inspector3,
  ])
    .filter((v): v is string => Boolean(v && v.trim()))
    .map((v) => v.trim());

  if (!inspectores.length) {
    errors.inspectores = "Indica al menos un inspector";
    errors.inspector1 = errors.inspector1 || "Inspector requerido";
  }

  if (!isRequired(a.calle)) errors.calle = "Calle requerida";
  if (!isRequired(a.numero)) errors.numero = "Número requerido";
  if (!isRequired(a.tipo_actuacion)) errors.tipo_actuacion = "Tipo requerido";
  if (!isRequired(a.doc_tipo_codigo)) errors.doc_tipo_codigo = "Tipo doc requerido";
  if (!isRequired(a.doc_nro)) errors.doc_nro = "Documento requerido";
  if (!isRequired(a.contrib_apellido)) errors.contrib_apellido = "Apellido requerido";

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
