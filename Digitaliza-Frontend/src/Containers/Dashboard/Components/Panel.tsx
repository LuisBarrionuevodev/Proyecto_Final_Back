import { useEffect, useState } from "react";
import { getDashboardResumen } from "../../../api/dashboardapi";
import { Box, Grid, Typography } from "@mui/material";
import DashboardCards from "./DashboardCards";
import DashboardChart from "./DashboardChart";

const Panel = () => {
  const [data, setData] = useState({
    actuaciones: 0,
    relevamientos: 0,
    pendientes: 0,
    completadas: 0,
  });

  useEffect(() => {
    const cargar = async () => {
      const res = await getDashboardResumen();
      setData(res);
    };
    cargar();
  }, []);

  return (
    <Box p={3} ml={{ xs: 10, sm: 12, md: 30 }}>
      <Typography variant="h4" fontWeight={800} mb={3}>
        Panel de Control
      </Typography>

      <Grid container spacing={3} mb={3}>
        <Grid xs={12} sm={6} md={3}>
          <DashboardCards title="Actuaciones" value={data.actuaciones} />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <DashboardCards title="Relevamientos" value={data.relevamientos} />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <DashboardCards title="Pendientes" value={data.pendientes} />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <DashboardCards title="Completados" value={data.completadas} />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid xs={12} md={8}>
          <DashboardChart />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Panel;
