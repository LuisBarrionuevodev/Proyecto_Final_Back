import { apiClient } from "./apiClient";
import type { IRelevamiento } from "../types/relevamientos";

// GET: lista de relevamientos
export const getRelevamientos = async (): Promise<IRelevamiento[]> => {
  const { data } = await apiClient.get<IRelevamiento[]>("/relevamientos");
  return data;
};

// POST: creación de relevamiento (sin id en el body)
export const createRelevamiento = async (
  body: Omit<IRelevamiento, "id">,
): Promise<IRelevamiento> => {
  const { data } = await apiClient.post<IRelevamiento>("/relevamientos", body);
  return data;
};

// PUT: actualización parcial
export const updateRelevamiento = async (
  id: number,
  body: Partial<Omit<IRelevamiento, "id">>,
): Promise<IRelevamiento> => {
  const { data } = await apiClient.put<IRelevamiento>(
    `/relevamientos/${id}`,
    body,
  );
  return data;
};

// DELETE
export const deleteRelevamiento = async (id: number): Promise<void> => {
  await apiClient.delete(`/relevamientos/${id}`);
};
