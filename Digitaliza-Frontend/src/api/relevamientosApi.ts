import { apiClient } from "./apiClient";
import type { IRelevamiento } from "../types/relevamientos";

export const getRelevamientos = async (): Promise<IRelevamiento[]> => {
  const { data } = await apiClient.get("/ped");
  return data;
};

export const createRelevamiento = async (body: IRelevamiento): Promise<IRelevamiento> => {
  const { data } = await apiClient.post("/relevamientos", body);
  return data;
};

export const updateRelevamiento = async (id: Number, body: IRelevamiento): Promise<IRelevamiento> => {
  const { data } = await apiClient.put(`/relevamientos/${id}`, body);
  return data;
};

export const deleteRelevamiento = async (id: string): Promise<void> => {
  await apiClient.delete(`/relevamientos/${id}`);
};