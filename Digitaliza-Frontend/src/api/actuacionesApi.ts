import apiClient from "./apiClient";
import type { IActuacion, IActuacionListado } from "../types/actuaciones";

export const getActuacionesListado = async (): Promise<IActuacionListado[]> => {
  const { data } = await apiClient.get<IActuacionListado[]>("/actuaciones");
  return data;
};

export const deleteActuacion = async (id: number): Promise<void> => {
  await apiClient.delete(`/actuaciones/${id}`);
};

export const updateActuacion = async (
  id: number,
  payload: Partial<IActuacionListado>,
): Promise<IActuacionListado> => {
  const { data } = await apiClient.put<IActuacionListado>(
    `/actuaciones/${id}`,
    payload,
  );
  return data;
};

export const createActuacion = async (actuacion: IActuacion): Promise<IActuacion> => {
  const { data } = await apiClient.post<IActuacion | IActuacion[]>(
    "/actuaciones",
    actuacion,
  );
  return Array.isArray(data) ? data[0] : data;
};
