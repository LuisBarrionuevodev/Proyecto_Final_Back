import { useEffect, useState } from "react";
import { getActuacionesListado } from "../api/actuacionesApi";
import type { IActuacionListado } from "../types/actuaciones";

export const useGestionActuaciones = () => {
  const [actuaciones, setActuaciones] = useState<IActuacionListado[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getActuacionesListado();
        setActuaciones(data);
      } catch (error) {
        console.error("Error al cargar actuaciones:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { actuaciones, setActuaciones, loading };
};
