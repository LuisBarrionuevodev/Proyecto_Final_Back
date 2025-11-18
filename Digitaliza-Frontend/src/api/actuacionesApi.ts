import { apiClient } from "./apiClient";
import type { IActuacion } from "../types/actuaciones";

// Respuesta típica de GET /api/v1/actuaciones (coincide con IActuacion):
// [
//   {
//     "id": 1,
//     "orden_trabajo_numero": "000123",
//     "fecha_actuacion": "2024-06-01",
//     "rubro_nombre": "ALIMENTOS",
//     "inspectores": ["INSPECTOR UNO", "INSPECTOR DOS"],
//     "calle": "SARMIENTO",
//     "numero": "1234",
//     "tipo_actuacion": "INSPECCION",
//     "contraproducencia": "SIN OBSERVACIONES",
//     "doc_tipo_codigo": "DNI",
//     "doc_nro": "12345678",
//     "contrib_apellido": "PEREZ",
//     "contrib_nombre": "JUAN",
//     "acta_inspeccion_num": "000111",
//     "acta_notificacion_num": "000222",
//     "notificacion_motivo_1": "FALTA DE HIGIENE",
//     "notificacion_motivo_2": "VENTILACION DEFECTUOSA",
//     "notificacion_motivo_3": "OTRO MOTIVO",
//     "acta_comprobacion_num": "000333",
//     "comprobacion_motivo": "INCUMPLIMIENTO PLAZO",
//     "acta_clausura_num": "000444",
//     "clausura_motivo": "RIESGO SANITARIO",
//     "acta_decomiso_num": "000555",
//     "decomiso_kilos_total": 12.5,
//     "expediente_numero": "EXP-2024-001",
//     "expediente_anio": 24,
//     "oficio_numero": "OF-77",
//     "oficio_anio": 24,
//     "oficio_causa": 987,
//     "notificacion_previa_num": "000666",
//     "comprobacion_previa_num": "000777"
//   }
// ]

export const getActuaciones = async (): Promise<IActuacion[]> => {
  const { data } = await apiClient.get("/actuaciones");
  return data;
};

export const createActuacion = async (body: IActuacion): Promise<IActuacion> => {
  const { data } = await apiClient.post("/actuaciones", body);
  return data;
};

export const updateActuacion = async (
  id: number,
  body: IActuacion,
): Promise<IActuacion> => {
  const { data } = await apiClient.put(`/actuaciones/${id}`, body);
  return data;
};

export const deleteActuacion = async (id: number): Promise<void> => {
  await apiClient.delete(`/actuaciones/${id}`);
};
