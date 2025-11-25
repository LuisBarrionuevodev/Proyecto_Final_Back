export interface IRelevamiento {
  id?: number;         // backend lo genera
  fecha: string;       // YYYY-MM-DD
  inspector: string;   // apellido/nombre del inspector
  direccion: string;   // texto libre
  rubro: string;       // rubro informado
}
