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

        const inspectores = Array.isArray(values.inspectores)
          ? values.inspectores
          : `${values.inspectores ?? ""}`
              .split(",")
              .map((v) => v.trim())
              .filter(Boolean);

        const payload: Partial<IActuacionListado> = {
          fecha_actuacion: values.fecha_actuacion,
          tipo_actuacion: values.tipo_actuacion,
          orden_trabajo_numero: values.orden_trabajo_numero ?? null,
          contraproducencia: values.contraproducencia,
          inspectores,
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
      { accessorKey: "rubro_nombre", header: "Rubro", enableEditing: false },
      {
        accessorKey: "inspectores",
        header: "Inspectores",
        Cell: ({ cell }) => (cell.getValue<string[]>() || []).join(", "),
        muiTableBodyCellEditTextFieldProps: ({ cell, row }) => ({
          defaultValue: (cell.getValue<string[]>() || []).join(", "),
          onChange: (event) => {
            row._valuesCache.inspectores = event.target.value
              .split(",")
              .map((v: string) => v.trim())
              .filter(Boolean);
          },
        }),
      },
      { accessorKey: "calle", header: "Calle", enableEditing: false },
      { accessorKey: "numero", header: "Número", enableEditing: false },
      { accessorKey: "contraproducencia", header: "Contraproducencia" },
      { accessorKey: "doc_tipo_codigo", header: "Doc. Tipo", enableEditing: false },
      { accessorKey: "doc_nro", header: "Doc. Nro", enableEditing: false },
      { accessorKey: "contrib_apellido", header: "Apellido", enableEditing: false },
      { accessorKey: "contrib_nombre", header: "Nombre", enableEditing: false },
      { accessorKey: "acta_inspeccion_num", header: "Acta inspección", enableEditing: false },
      { accessorKey: "acta_notificacion_num", header: "Acta notificación", enableEditing: false },
      { accessorKey: "notificacion_motivo_1", header: "Notif. Motivo 1", enableEditing: false },
      { accessorKey: "notificacion_motivo_2", header: "Notif. Motivo 2", enableEditing: false },
      { accessorKey: "notificacion_motivo_3", header: "Notif. Motivo 3", enableEditing: false },
      { accessorKey: "acta_comprobacion_num", header: "Acta comprobación", enableEditing: false },
      { accessorKey: "comprobacion_motivo", header: "Comprobación motivo", enableEditing: false },
      { accessorKey: "acta_clausura_num", header: "Acta clausura", enableEditing: false },
      { accessorKey: "clausura_motivo", header: "Clausura motivo", enableEditing: false },
      { accessorKey: "acta_decomiso_num", header: "Acta decomiso", enableEditing: false },
      { accessorKey: "decomiso_kilos_total", header: "Kg decomiso", enableEditing: false },
      { accessorKey: "expediente_numero", header: "Expediente número", enableEditing: false },
      { accessorKey: "expediente_anio", header: "Expediente año", enableEditing: false },
      { accessorKey: "oficio_numero", header: "Oficio número", enableEditing: false },
      { accessorKey: "oficio_anio", header: "Oficio año", enableEditing: false },
      { accessorKey: "oficio_causa", header: "Oficio causa", enableEditing: false },
      { accessorKey: "notificacion_previa_num", header: "Notif. previa", enableEditing: false },
      { accessorKey: "comprobacion_previa_num", header: "Comprob. previa", enableEditing: false },
      {
        accessorKey: "establecimiento_domicilio_id",
        header: "Estab./Domicilio ID",
        enableEditing: false,
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
    initialState: {
      columnVisibility: { id: false },
    },

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
