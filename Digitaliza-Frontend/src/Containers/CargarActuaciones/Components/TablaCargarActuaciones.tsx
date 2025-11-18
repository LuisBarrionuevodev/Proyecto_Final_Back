import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
  type MRT_Row,
  type MRT_TableOptions,
} from "material-react-table";
import { useState } from "react";
import { Box, Typography } from "@mui/material";
import axios from "axios"; // 👈 NUEVO

import { createActuacion } from "../../../api/actuacionesApi";
import { TABLE_CREAR_ACTUACIONES } from "../../../constants/tableConfig";
import { TableButtonCreate } from "../../CargarActuaciones/Components/TableButtonCreate";
import { TableGeneralStyles, TableTitleStyles } from "../../../styles/TablasStyle";
import type { IActuacion } from "../../../types/actuaciones";
import { validateActuacion } from "../../../utils/validations";

const buildInspectores = (values: Record<string, any>): string[] => {
  const base = (values.inspectores as string[]) || [];
  return [values.inspector1, values.inspector2, values.inspector3, ...base]
    .map((v) => (v || "").toString().trim())
    .filter(Boolean);
};

const normalizeFecha = (value: string) => {
  if (!value) return value;
  if (value.includes("/")) {
    const [dd, mm, yy] = value.split("/");
    if (yy?.length === 2) {
      return `20${yy}-${mm}-${dd}`;
    }
    return `${yy}-${mm}-${dd}`;
  }
  return value;
};

const TablaCargarActuaciones = () => {
  const [validationErrors, setValidationErrors] =
    useState<Record<string, string | undefined>>({});
  const [data, setData] = useState<IActuacion[]>([]);

  const validateRow = (row: MRT_Row<IActuacion>) => {
    setValidationErrors(validateActuacion(row._valuesCache));
  };

  /*
    Ejemplo de payload que se envía al backend desde esta tabla (se envía un solo
    objeto y el backend lo envuelve como {"items": [obj]}):
    {
      "orden_trabajo_numero": "000123",
      "fecha_actuacion": "2024-06-01",
      "rubro_nombre": "ALIMENTOS",
      "inspectores": ["INSPECTOR UNO", "INSPECTOR DOS"],
      "calle": "SARMIENTO",
      "numero": "1234",
      "tipo_actuacion": "INSPECCION",
      "contraproducencia": "SIN OBSERVACIONES",
      "doc_tipo_codigo": "DNI",
      "doc_nro": "12345678",
      "contrib_apellido": "PEREZ",
      "contrib_nombre": "JUAN",
      "acta_inspeccion_num": "000111",
      "acta_notificacion_num": "000222",
      "notificacion_motivo_1": "FALTA DE HIGIENE",
      "notificacion_motivo_2": "VENTILACION DEFECTUOSA",
      "notificacion_motivo_3": "OTRO MOTIVO",
      "acta_comprobacion_num": "000333",
      "comprobacion_motivo": "INCUMPLIMIENTO PLAZO",
      "acta_clausura_num": "000444",
      "clausura_motivo": "RIESGO SANITARIO",
      "acta_decomiso_num": "000555",
      "decomiso_kilos_total": 12.5,
      "expediente_numero": "EXP-2024-001",
      "expediente_anio": 24,
      "oficio_numero": "OF-77",
      "oficio_anio": 24,
      "oficio_causa": 987,
      "notificacion_previa_num": "000666",
      "comprobacion_previa_num": "000777"
    }
  */
  const handleCreateNewRow: MRT_TableOptions<IActuacion>["onCreatingRowSave"] =
    async ({ values, table }) => {
      const payload: IActuacion = {
        orden_trabajo_numero: values.orden_trabajo_numero,
        fecha_actuacion: normalizeFecha(values.fecha_actuacion),
        rubro_nombre: values.rubro_nombre,
        inspectores: buildInspectores(values),
        calle: values.calle,
        numero: `${values.numero ?? ""}`,
        tipo_actuacion: values.tipo_actuacion,
        contraproducencia: values.contraproducencia,
        doc_tipo_codigo: values.doc_tipo_codigo,
        doc_nro: values.doc_nro,
        contrib_apellido: values.contrib_apellido,
        contrib_nombre: values.contrib_nombre,
        acta_inspeccion_num: values.acta_inspeccion_num,
        acta_notificacion_num: values.acta_notificacion_num,
        notificacion_motivo_1: values.notificacion_motivo_1,
        notificacion_motivo_2: values.notificacion_motivo_2,
        notificacion_motivo_3: values.notificacion_motivo_3,
        acta_comprobacion_num: values.acta_comprobacion_num,
        comprobacion_motivo: values.comprobacion_motivo,
        acta_clausura_num: values.acta_clausura_num,
        clausura_motivo: values.clausura_motivo,
        acta_decomiso_num: values.acta_decomiso_num,
        decomiso_kilos_total: values.decomiso_kilos_total
          ? Number(values.decomiso_kilos_total)
          : undefined,
        expediente_numero: values.expediente_numero,
        expediente_anio: values.expediente_anio
          ? Number(values.expediente_anio)
          : undefined,
        oficio_numero: values.oficio_numero,
        oficio_anio: values.oficio_anio ? Number(values.oficio_anio) : undefined,
        oficio_causa: values.oficio_causa ? Number(values.oficio_causa) : undefined,
        notificacion_previa_num: values.notificacion_previa_num,
        comprobacion_previa_num: values.comprobacion_previa_num,
      };

      const errors = validateActuacion({ ...values, inspectores: payload.inspectores });

      if (Object.values(errors).some((e) => e)) {
        setValidationErrors(errors);
        return;
      }

      try {
        const nuevaActuacion = await createActuacion(payload as IActuacion);

        table.setCreatingRow(null);
        setValidationErrors({});
        setData((prev) => [...prev, nuevaActuacion]);
        setTimeout(() => {
          table.setCreatingRow(true);
        }, 50);
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.error(
            "Error al crear actuación (backend):",
            error.response?.status,
            error.response?.data
          );
        } else {
          console.error("Error al crear actuación (desconocido):", error);
        }
      }
    };

  const columns: MRT_ColumnDef<IActuacion>[] = [
    {
      accessorKey: "orden_trabajo_numero",
      header: "OT",
      muiEditTextFieldProps: ({ cell, row }) => ({
        autoFocus: cell.column.id === "orden_trabajo_numero",
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "fecha_actuacion",
      header: "Fecha (DD/MM/YY)",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "rubro_nombre",
      header: "Rubro",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "inspector1",
      header: "Inspector 1",
      accessorFn: (row) => row.inspectores?.[0] || "",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id] || validationErrors.inspectores,
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "inspector2",
      header: "Inspector 2",
      accessorFn: (row) => row.inspectores?.[1] || "",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "inspector3",
      header: "Inspector 3",
      accessorFn: (row) => row.inspectores?.[2] || "",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "calle",
      header: "Calle",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "numero",
      header: "Número",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "tipo_actuacion",
      header: "Tipo de actuación",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "contraproducencia",
      header: "Contraproducencia",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.contraproducencia = e.target.value;
        },
      }),
    },
    {
      accessorKey: "doc_tipo_codigo",
      header: "Tipo doc",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "doc_nro",
      header: "Documento",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "contrib_apellido",
      header: "Apellido contribuyente",
      muiEditTextFieldProps: ({ cell, row }) => ({
        error: !!validationErrors[cell.column.id],
        helperText: validationErrors[cell.column.id],
        onChange: (e) => {
          row._valuesCache[cell.column.id] = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "contrib_nombre",
      header: "Nombre contribuyente",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.contrib_nombre = e.target.value;
        },
      }),
    },
    {
      accessorKey: "acta_inspeccion_num",
      header: "Acta inspección",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.acta_inspeccion_num = e.target.value;
        },
      }),
    },
    {
      accessorKey: "acta_notificacion_num",
      header: "Acta notificación",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.acta_notificacion_num = e.target.value;
        },
      }),
    },
    {
      accessorKey: "notificacion_motivo_1",
      header: "Motivo notificación 1",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.notificacion_motivo_1 = e.target.value;
        },
      }),
    },
    {
      accessorKey: "notificacion_motivo_2",
      header: "Motivo notificación 2",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.notificacion_motivo_2 = e.target.value;
        },
      }),
    },
    {
      accessorKey: "notificacion_motivo_3",
      header: "Motivo notificación 3",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.notificacion_motivo_3 = e.target.value;
        },
      }),
    },
    {
      accessorKey: "acta_comprobacion_num",
      header: "Acta comprobación",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.acta_comprobacion_num = e.target.value;
        },
      }),
    },
    {
      accessorKey: "comprobacion_motivo",
      header: "Motivo comprobación",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.comprobacion_motivo = e.target.value;
        },
      }),
    },
    {
      accessorKey: "acta_clausura_num",
      header: "Acta clausura",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.acta_clausura_num = e.target.value;
        },
      }),
    },
    {
      accessorKey: "clausura_motivo",
      header: "Motivo clausura",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.clausura_motivo = e.target.value;
        },
      }),
    },
    {
      accessorKey: "acta_decomiso_num",
      header: "Acta decomiso",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.acta_decomiso_num = e.target.value;
        },
      }),
    },
    {
      accessorKey: "decomiso_kilos_total",
      header: "Kg decomiso",
      muiEditTextFieldProps: ({ row }) => ({
        type: "number",
        onChange: (e) => {
          row._valuesCache.decomiso_kilos_total = e.target.value;
        },
        onBlur: () => validateRow(row),
      }),
    },
    {
      accessorKey: "expediente_numero",
      header: "Expediente número",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.expediente_numero = e.target.value;
        },
      }),
    },
    {
      accessorKey: "expediente_anio",
      header: "Expediente año",
      muiEditTextFieldProps: ({ row }) => ({
        type: "number",
        onChange: (e) => {
          row._valuesCache.expediente_anio = e.target.value;
        },
      }),
    },
    {
      accessorKey: "oficio_numero",
      header: "Oficio número",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.oficio_numero = e.target.value;
        },
      }),
    },
    {
      accessorKey: "oficio_anio",
      header: "Oficio año",
      muiEditTextFieldProps: ({ row }) => ({
        type: "number",
        onChange: (e) => {
          row._valuesCache.oficio_anio = e.target.value;
        },
      }),
    },
    {
      accessorKey: "oficio_causa",
      header: "Oficio causa",
      muiEditTextFieldProps: ({ row }) => ({
        type: "number",
        onChange: (e) => {
          row._valuesCache.oficio_causa = e.target.value;
        },
      }),
    },
    {
      accessorKey: "notificacion_previa_num",
      header: "Notif. previa",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.notificacion_previa_num = e.target.value;
        },
      }),
    },
    {
      accessorKey: "comprobacion_previa_num",
      header: "Comprob. previa",
      muiEditTextFieldProps: ({ row }) => ({
        onChange: (e) => {
          row._valuesCache.comprobacion_previa_num = e.target.value;
        },
      }),
    },
  ];

  const table = useMaterialReactTable({
    ...TABLE_CREAR_ACTUACIONES,
    columns,
    data: data,
    initialState: {
      columnVisibility: { id: false },
    },
    editDisplayMode: "row",
    enableEditing: true,
    onCreatingRowSave: handleCreateNewRow,
    renderTopToolbarCustomActions: ({ table }) => (
      <TableButtonCreate table={table} />
    ),
  });

  return (
    <Box sx={{ width: "100%" }}>
      <Box sx={{ ...TableGeneralStyles }}>
        <Typography sx={TableTitleStyles}>Creación de actuación</Typography>
        <MaterialReactTable table={table} />
      </Box>
    </Box>
  );
};

export default TablaCargarActuaciones;
