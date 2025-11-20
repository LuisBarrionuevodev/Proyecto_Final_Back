import { Box, Grid, Typography } from "@mui/material";
import DashboardCards from "./DashboardCards";
import DashboardChart from "./DashboardChart";

const Panel = () => {

  return (
    <Box p={3} ml={{xs: 10, sm: 12, md: 30}}>
      <Typography variant="h4" fontWeight={800} mb={3}>
        Panel de Control
      </Typography>

      {/* Tarjetas principales */}
      <Grid container spacing={3} mb={3}>
        <Grid size = {{ xs:12, sm:6 ,md:3 }}>
          <DashboardCards title="Actuaciones" value={120} />
        </Grid>
        <Grid size = {{ xs:12, sm:6 ,md:3 }}>
          <DashboardCards title="Relevamientos" value={85} />
        </Grid>
        <Grid size = {{ xs:12, sm:6 ,md:3 }}>
          <DashboardCards title="Pendientes" value={14} />
        </Grid>
        <Grid size = {{ xs:12, sm:6 ,md:3 }}>
          <DashboardCards title="Completados" value={191} />
        </Grid>
      </Grid>

      {/* Gráfico */}
      <Grid container spacing={3}>
        <Grid size= {{xs:12, md:8}}>
          <DashboardChart />
        </Grid>
      </Grid>
    </Box>
  );
}

export default Panel;