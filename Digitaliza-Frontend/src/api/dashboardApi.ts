import { apiClient } from "./apiClient";

export const getDashboardResumen = async () => {
  const { data } = await apiClient.get("/dashboard/resumen");
  return data;
};
