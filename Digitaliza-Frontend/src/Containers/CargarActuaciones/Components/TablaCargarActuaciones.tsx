import {
    MaterialReactTable,
    useMaterialReactTable,
    type MRT_ColumnDef,
    type MRT_Row,
    type MRT_TableOptions,
} from "material-react-table";
import { validateActuacion } from "../../../utils/validations";
import { useState } from "react";
import { createActuacion } from "../../../api/actuacionesApi";
import type { IActuacion } from "../../../types/actuaciones";
import { Box, Typography } from "@mui/material";
import { TableGeneralStyles, TableTitleStyles } from "../../../styles/TablasStyle";
import { TABLE_CREAR_ACTUACIONES } from "../../../constants/tableConfig";
import { TableButtonCreate } from "../../CargarActuaciones/Components/TableButtonCreate";

const TablaCargarActuaciones = () => {
    const [validationErrors, setValidationErrors] = useState<Record<string, string | undefined>>({});
    const [data, setData] = useState<IActuacion[]>([]);


    const validateRow = (row: MRT_Row<IActuacion>) => {
        setValidationErrors(validateActuacion(row._valuesCache));
    };

    const handleCreateNewRow: MRT_TableOptions<IActuacion>["onCreatingRowSave"] =
        async ({ values, table }) => {
            const errors = validateActuacion(values);

            if (Object.values(errors).some((e) => e)) {
                setValidationErrors(errors);
                return;
            }

            try {
                const nuevaActuacion = await createActuacion(values as IActuacion);

                // cerrar la fila actual
                table.setCreatingRow(null);
                setValidationErrors({});
                setData(prev => [...prev, nuevaActuacion]);
                // abrir automáticamente otra fila editable
                setTimeout(() => {
                    table.setCreatingRow(true);
                }, 50);

            } catch (error) {
                console.error("Error al crear relevamiento:", error);
            }
        };

    const columns: MRT_ColumnDef<IActuacion>[] = [
        {
            accessorKey: "id",
            header: "ID",
            enableEditing: false,
        },
        {
            accessorKey: "rubro",
            header: "Rubro",
            muiEditTextFieldProps: ({ cell, row }) => ({
                autoFocus: cell.column.id === "rubro",
                error: !!validationErrors[cell.column.id],
                helperText: validationErrors[cell.column.id],
                onChange: (e) => {
                    // Guradamos cache
                    row._valuesCache[cell.column.id] = e.target.value;
                },
                onBlur: () => {
                    // valida SOLO al salir del input
                    validateRow(row);
                },
            })
        },
        {
            accessorKey: "distrito",
            header: "Distrito",
            muiEditTextFieldProps: ({ cell, row }) => ({
                error: !!validationErrors[cell.column.id],
                helperText: validationErrors[cell.column.id],
                onChange: (e) => {
                    const value = cell.column.id === "distrito"
                        ? Number(e.target.value)
                        : e.target.value;
                    row._valuesCache[cell.column.id] = value;
                },
                onBlur: () => {
                    validateRow(row);
                },
            }),
        },
        {
            accessorKey: "inspector1",
            header: "Inspector-1",
            muiEditTextFieldProps: ({ cell, row }) => ({
                error: !!validationErrors[cell.column.id],
                helperText: validationErrors[cell.column.id],
                onChange: (e) => {
                    row._valuesCache[cell.column.id] = e.target.value;
                },
                onBlur: () => {
                    validateRow(row);
                },
            }),
        },
        {
            accessorKey: "inspector2",
            header: "Inspector-2",
            muiEditTextFieldProps: ({ cell, row }) => ({
                error: !!validationErrors[cell.column.id],
                helperText: validationErrors[cell.column.id],
                onChange: (e) => {
                    row._valuesCache[cell.column.id] = e.target.value;
                },
                onBlur: () => {
                    validateRow(row);
                },
            }),
        },
        {
            accessorKey: "inspector3",
            header: "Inspector-3",
            muiEditTextFieldProps: ({ cell, row }) => ({
                error: !!validationErrors[cell.column.id],
                helperText: validationErrors[cell.column.id],
                onChange: (e) => {
                    row._valuesCache[cell.column.id] = e.target.value;
                },

                onBlur: () => {
                    validateRow(row);
                },
            }),
        },
        {
            accessorKey: "direccion",
            header: "Dirección",
            muiEditTextFieldProps: ({ cell, row }) => ({
                error: !!validationErrors[cell.column.id],
                helperText: validationErrors[cell.column.id],
                onChange: (e) => {
                    row._valuesCache[cell.column.id] = e.target.value;
                },

                onBlur: () => {
                    validateRow(row);
                },
            }),
        },
        {
            accessorKey: "clausuras",
            header: "Clausuras",
            muiEditTextFieldProps: ({ row, cell, table }) => ({
                error: !!validationErrors[cell.column.id],
                helperText: validationErrors[cell.column.id],
                onChange: (e) => {
                    const value = cell.column.id === "clausuras"
                        ? Number(e.target.value)
                        : e.target.value;
                    row._valuesCache[cell.column.id] = value;
                },

                onBlur: () => {
                    validateRow(row);
                },
                // ENTER ENVIA AUTOMATICAMENTE
                onKeyDown: (e) => {
                    if (e.key === "Enter") {
                        table.options.onCreatingRowSave?.({
                            values: row.getAllCells().reduce((acc, c) => {
                                acc[c.column.id] = row._valuesCache[c.column.id];
                                return acc;
                            }, {} as any),
                            table,
                        } as any);
                    }
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
            <Box sx={{...TableGeneralStyles, }}>
                <Typography sx={TableTitleStyles}>Creación de actuación</Typography>
                <MaterialReactTable table={table} />
            </Box>
        </Box>
    );
};

export default TablaCargarActuaciones;