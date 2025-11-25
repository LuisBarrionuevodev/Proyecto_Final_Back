import { mkConfig, generateCsv, download } from "export-to-csv";

export const csvConfig = mkConfig({
  fieldSeparator: ",",
  decimalSeparator: ".",
  useKeysAsHeaders: true,
});

// Normaliza cualquier valor a algo que export-to-csv soporte
const normalizeValue = (
  value: unknown,
): string | number | boolean | null => {
  if (value === null || value === undefined) return "";

  const t = typeof value;

  if (t === "string" || t === "number" || t === "boolean") {
    return value as string | number | boolean;
  }

  // Arrays → string legible
  if (Array.isArray(value)) {
    return value
      .map((v) =>
        typeof v === "string" || typeof v === "number"
          ? String(v)
          : JSON.stringify(v),
      )
      .join(" | ");
  }

  // Objetos → JSON (por si acaso)
  return JSON.stringify(value);
};

export const exportVisibleRows = (rows: any[], table: any) => {
  const visibleColumns = table
    .getAllLeafColumns()
    .filter((col: { getIsVisible: () => any }) => col.getIsVisible())
    .map((col: { id: any }) => col.id);

  const rowData = rows.map((row) => {
    const filtered: Record<string, string | number | boolean | null> = {};

    visibleColumns.forEach((colId: string | number) => {
      const rawValue = (row.original as any)[colId];
      filtered[colId as string] = normalizeValue(rawValue);
    });

    return filtered;
  });

  const csv = generateCsv(csvConfig)(rowData);
  download(csvConfig)(csv);
};

export const exportAllData = (data: any[]) => {
  const rowData = data.map((row) => {
    const flat: Record<string, string | number | boolean | null> = {};

    Object.entries(row).forEach(([key, value]) => {
      flat[key] = normalizeValue(value);
    });

    return flat;
  });

  const csv = generateCsv(csvConfig)(rowData);
  download(csvConfig)(csv);
};
