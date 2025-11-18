export type TipoActuacion =
  | "INSPECCION"
  | "REINSPECCION"
  | "RATIFICACION"
  | "VERIFICAR E INFORMAR";

export interface IActuacion {
  id?: number;
  orden_trabajo_numero: string;
  fecha_actuacion: string; // UI DD/MM/YY → backend YYYY-MM-DD
  rubro_nombre: string;
  inspectores: string[];
  calle: string;
  numero: string;
  tipo_actuacion: TipoActuacion;
  contraproducencia?: string;
  doc_tipo_codigo: string;
  doc_nro: string;
  contrib_apellido: string;
  contrib_nombre?: string;
  acta_inspeccion_num?: string;
  acta_notificacion_num?: string;
  notificacion_motivo_1?: string;
  notificacion_motivo_2?: string;
  notificacion_motivo_3?: string;
  acta_comprobacion_num?: string;
  comprobacion_motivo?: string;
  acta_clausura_num?: string;
  clausura_motivo?: string;
  acta_decomiso_num?: string;
  decomiso_kilos_total?: number;
  expediente_numero?: string;
  expediente_anio?: number;
  oficio_numero?: string;
  oficio_anio?: number;
  oficio_causa?: number;
  notificacion_previa_num?: string;
  comprobacion_previa_num?: string;
}

export interface IActuacionListado {
  id: number;
  orden_trabajo_numero: string | null;
  fecha_actuacion: string;
  rubro_nombre: string | null;
  inspectores: string[];
  calle: string | null;
  numero: string | null;
  tipo_actuacion: TipoActuacion;
  contraproducencia?: string | null;
  doc_tipo_codigo: string | null;
  doc_nro: string | null;
  contrib_apellido: string | null;
  contrib_nombre?: string | null;
  acta_inspeccion_num?: string | null;
  acta_notificacion_num?: string | null;
  notificacion_motivo_1?: string | null;
  notificacion_motivo_2?: string | null;
  notificacion_motivo_3?: string | null;
  acta_comprobacion_num?: string | null;
  comprobacion_motivo?: string | null;
  acta_clausura_num?: string | null;
  clausura_motivo?: string | null;
  acta_decomiso_num?: string | null;
  decomiso_kilos_total?: number | null;
  expediente_numero?: string | null;
  expediente_anio?: number | null;
  oficio_numero?: string | null;
  oficio_anio?: number | null;
  oficio_causa?: number | null;
  notificacion_previa_num?: string | null;
  comprobacion_previa_num?: string | null;
  establecimiento_domicilio_id?: number | null;
  created_at: string | null;
  updated_at: string | null;
}
