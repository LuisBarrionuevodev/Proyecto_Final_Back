export interface IActuacion {
    id: number;
    rubro: string;
    distrito: number;
    inspector1: string;
    inspector2: string;
    inspector3: string;
    direccion: string;
    clausuras: number;
    [key: string]: string | number;
}