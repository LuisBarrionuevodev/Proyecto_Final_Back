import { Box, Typography, IconButton, Tooltip } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
  type MRT_TableOptions,
} from "material-react-table";
import { useCallback, useMemo } from "react";
import { BASE_TABLE_CONFIG } from "../../../constants/tableConfig";
import type { IActuacionListado } from "../../../types/actuaciones";
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

  const handleDeleteRow = useCallback(
    async (id: number) => {
      if (!window.confirm("¿Estás seguro de eliminar este registro?")) return;

      try {
        await deleteActuacion(id);
        setActuaciones((prev) => prev.filter((item) => item.id !== id));
      } catch (error) {
        console.error("Error al eliminar:", error);
        alert("No se pudo eliminar el registro.");
      }
    },
    [setActuaciones],
  );

  const handleSaveRow: MRT_TableOptions<IActuacionListado>["onEditingRowSave"] =
    useCallback(
      async ({ values, exitEditingMode }) => {
        const id = Number(values.id);
        if (Number.isNaN(id)) {
          alert("ID de actuación inválido");
          return;
        }

        const payload: Partial<IActuacionListado> = {
          fecha_actuacion: values.fecha_actuacion,
          tipo_actuacion: values.tipo_actuacion,
          orden_trabajo_numero: values.orden_trabajo_numero,
          establecimiento_domicilio_id:
            values.establecimiento_domicilio_id === null
              ? null
              : Number(values.establecimiento_domicilio_id),
        };

        try {
          const updated = await updateActuacion(id, payload);
          setActuaciones((prev) =>
            prev.map((item) => (item.id === id ? updated : item)),
          );
          exitEditingMode();
        } catch (error) {
          console.error("Error al actualizar:", error);
          alert("No se pudo actualizar el registro.");
        }
      },
      [setActuaciones],
    );

  const columns = useMemo<MRT_ColumnDef<IActuacionListado>[]>(
    () => [
      { accessorKey: "id", header: "ID", enableEditing: false },
      {
        accessorKey: "fecha_actuacion",
        header: "Fecha actuación",
        muiTableBodyCellEditTextFieldProps: {
          type: "date",
        },
      },
      { accessorKey: "tipo_actuacion", header: "Tipo" },
      { accessorKey: "orden_trabajo_numero", header: "OT" },
      {
        accessorKey: "establecimiento_domicilio_id",
        header: "Estab./Domicilio ID",
      },
      { accessorKey: "created_at", header: "Creado", enableEditing: false },
      { accessorKey: "updated_at", header: "Actualizado", enableEditing: false },
    ],
    [],
  );

  const table = useMaterialReactTable({
    ...BASE_TABLE_CONFIG,
    editDisplayMode: "row",
    columns,
    data: actuaciones,
    enableColumnOrdering: true,
    enableColumnFilters: true,
    enableGlobalFilter: true,
    enableHiding: true,
    enableRowActions: true,
    onEditingRowSave: handleSaveRow,
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
      <TablaExportButtons data={actuaciones} table={table} />
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
