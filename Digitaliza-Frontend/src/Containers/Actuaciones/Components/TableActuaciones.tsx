import { Box, Typography, IconButton, Tooltip } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { MaterialReactTable, useMaterialReactTable, type MRT_ColumnDef, } from "material-react-table";
import { useCallback, useEffect, useMemo, useState } from "react";
import { BASE_TABLE_CONFIG } from "../../../constants/tableConfig";
import type { IActuacion } from "../../../types/actuaciones";
import {
  TableGeneralStyles,
  TableLoadingStyles,
  TableTitleStyles,
} from "../../../styles/TablasStyle";
import { useGestionActuaciones } from "../../../hooks/useGestionActuaciones";
import { deleteActuacion, updateActuacion } from "../../../api/actuacionesApi";
import { TablaExportButtons } from "./TableButtons";

const TablaActuaciones = () => {

  const { actuaciones, setActuaciones, loading } = useGestionActuaciones();
  const [data, setData] = useState<IActuacion[]>([]);
  const [validationErrors] = useState<Record<number, Record<string, string>>>({});

  useEffect(() => {
    setData(actuaciones ?? []);
  }, [actuaciones]);

  const handleDeleteRow = useCallback(async (id: number) => {
    if (!window.confirm("¿Estás seguro de eliminar este registro?")) return;
    const prev = data;
    setData(prev => prev.filter(item => item.id !== id));
    setActuaciones(prev => prev.filter(item => item.id !== id)); // si querés sync local
    try {
      await deleteActuacion(id);
    } catch (error) {
      console.error("Error al eliminar:", error);
      alert("No se pudo eliminar el registro. Se restaurará la lista.");
      setData(prev);
      setActuaciones(prev);
    }
  }, [data, setActuaciones]);

  const handleEditCell = useCallback(
    async (id: number, key: keyof IActuacion, value: any) => {
      let updatedRow: IActuacion | undefined;
      setData((prev) => {
        const idx = prev.findIndex((r) => r.id === id);
        if (idx === -1) return prev;
        updatedRow = { ...prev[idx], [key]: value }; // guardamos fila actualizada
        const newData = [...prev];
        newData[idx] = updatedRow!;
        return newData;
      });

      if (!updatedRow) return;

      const payload: IActuacion = {
        id: updatedRow.id!,
        rubro: updatedRow.rubro,
        distrito: Number(updatedRow.distrito ?? 0),
        inspector1: updatedRow.inspector1?.trim() || "",
        inspector2: updatedRow.inspector2?.trim() || "",
        inspector3: updatedRow.inspector3?.trim() || "",
        direccion: updatedRow.direccion?.trim() || "",
        clausuras: Number(updatedRow.clausuras ?? 0),
      };

      //  Validación 
      if (!payload.rubro || !payload.direccion || payload.distrito <= 0 || payload.clausuras < 0) {
        alert("Algunos campos no son válidos. Corrigelos antes de guardar.");
        return;
      }

      // Llamada Axios
      try {
        await updateActuacion(id, payload);
      } catch (error) {
        console.error("Error al actualizar:", error);
        alert("No se pudo actualizar el registro.");
      }
    },
    []
  );


  const columns = useMemo<MRT_ColumnDef<IActuacion>[]>(() => [
    {
      accessorKey: "id",
      header: "ID",
      enableHiding: true,
      enableEditing: false,
      enableClickToCopy: true,
    },
    {
      accessorKey: "rubro",
      header: "Rubro",
      muiEditTextFieldProps: ({ row }) => ({
        error: !!validationErrors[row.original.id]?.rubro,
        helperText: validationErrors[row.original.id]?.rubro,
        onBlur: (e) => handleEditCell(row.original.id, "rubro", e.target.value),
      })
    },
    {
      accessorKey: "distrito",
      header: "Distrito",
      muiEditTextFieldProps: ({ row }) => ({
        type: "number",
        error: !!validationErrors[row.original.id]?.distrito,
        helperText: validationErrors[row.original.id]?.distrito,
        onBlur: (e) => handleEditCell(row.original.id, "distrito", Number(e.target.value)),
      }),
    },
    {
      accessorKey: "inspector1",
      header: "Inspector-1",
      muiEditTextFieldProps: ({ row }) => ({
        error: !!validationErrors[row.original.id]?.inspector1,
        helperText: validationErrors[row.original.id]?.inspector1,
        onBlur: (e) => handleEditCell(row.original.id, "inspector1", e.target.value),
      }),
    },
    {
      accessorKey: "inspector2",
      header: "Inspector-2",
      muiEditTextFieldProps: ({ row }) => ({
        error: !!validationErrors[row.original.id]?.inspector2,
        helperText: validationErrors[row.original.id]?.inspector2,
        onBlur: (e) => handleEditCell(row.original.id, "inspector2", e.target.value),
      }),
    },
    {
      accessorKey: "inspector3",
      header: "Inspector-3",
      muiEditTextFieldProps: ({ row }) => ({
        error: !!validationErrors[row.original.id]?.inspector3,
        helperText: validationErrors[row.original.id]?.inspector3,
        onBlur: (e) => handleEditCell(row.original.id, "inspector3", e.target.value),
      }),
    },
    {
      accessorKey: "direccion",
      header: "Dirección",
      muiEditTextFieldProps: ({ row }) => ({
        error: !!validationErrors[row.original.id]?.direccion,
        helperText: validationErrors[row.original.id]?.direccion,
        onBlur: (e) => handleEditCell(row.original.id, "direccion", e.target.value),
      }),
    },
    {
      accessorKey: "clausuras",
      header: "Clausuras",
      muiEditTextFieldProps: ({ row }) => ({
        type: "number",
        error: !!validationErrors[row.original.id]?.clausuras,
        helperText: validationErrors[row.original.id]?.clausuras,
        onBlur: (e) => handleEditCell(row.original.id, "clausuras", Number(e.target.value)),
      }),
    },
  ], [validationErrors])

  const table = useMaterialReactTable({
    ...BASE_TABLE_CONFIG,
    columns,
    data,
    enableRowActions: true,
    initialState: {
      columnVisibility: { id: false },
    },
    renderRowActions: ({ row }) => (
      <Box sx={{ display: "flex", gap: "0.5rem" }}>
        <Tooltip title="Eliminar">
          <IconButton color="error" onClick={() => handleDeleteRow(Number(row.original.id))}>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box>
    ),
    renderTopToolbarCustomActions: ({ table }) => (
      <TablaExportButtons data={data} table={table} />
    ),
  });

  if (loading) return <Typography sx={TableLoadingStyles}>Cargando actuaciones...</Typography>;

  return (
    <Box sx={{ width: "100%" }}>
      <Box
        sx={{
          ...TableGeneralStyles,
          "& .MuiBox-root.css-wsew38": {
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            gap: 2,
          },
        }}
      >
        <Typography sx={TableTitleStyles}>Gestión de Actuaciones</Typography>
        <MaterialReactTable table={table} />
      </Box>
    </Box>
  );
};

export default TablaActuaciones;