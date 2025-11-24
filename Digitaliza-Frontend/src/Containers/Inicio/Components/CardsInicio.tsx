import { CardStyle, StyleBoxTextCard, StyleTextCard } from "../../../styles/InicioStyles"
import type { JSX } from "react";
import { Typography, Grid, Box } from '@mui/material';
import GestionarActuaciones from "../assets-inicio/GestionarActuaciones.svg"
import VerDashboardLogo from "../assets-inicio/VerDashboardLogo.svg"
import VerMapaLogo from "../assets-inicio/VerMapaLogo.svg"
import VerInformeLogo from "../assets-inicio/VerInformeLogo.svg"

const CardsInicio = (): JSX.Element => {

    return (
        <Grid container marginTop={"15px"} padding={5} spacing={8} >
            <Grid size={{ xs: 12, sm: 6, md: 6, lg: 3 }}>
                <a href="/actuaciones">

                    <Grid sx={CardStyle}>
                        <Box component="img" src={GestionarActuaciones} alt="IMG-ACTUACIONES" />
                    </Grid>
                    
                    <Grid sx={StyleBoxTextCard}>
                        <Typography sx={StyleTextCard}>
                            Gestionar Actuaciones
                        </Typography>
                    </Grid>

                </a>
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 6, lg: 3 }}>
                <a href="/dashboard">

                    <Grid sx={CardStyle}>
                        <Box component="img" src={VerDashboardLogo} alt="IMG-DASHBOARD" />
                    </Grid>

                    <Grid sx={StyleBoxTextCard}>
                        <Typography sx={StyleTextCard}>
                            Ver Dashboard
                        </Typography>
                    </Grid>

                </a>
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 6, lg: 3 }}>
                <a href="/mapa">

                    <Grid sx={CardStyle}>
                        <Box component="img" src={VerMapaLogo} alt="IMG-MAPA" />
                    </Grid>

                    <Grid sx={StyleBoxTextCard}>
                        <Typography sx={StyleTextCard}>
                            Ver Mapa
                        </Typography>
                    </Grid>

                </a>
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 6, lg: 3 }}>
                <a href="/informe">

                    <Grid sx={CardStyle}>
                        <Box component="img" src={VerInformeLogo} alt="IMG-INFORME" />
                    </Grid>

                    <Grid sx={StyleBoxTextCard}>
                        <Typography sx={StyleTextCard}>
                            Ver Informe Mensual
                        </Typography>
                    </Grid>

                </a>
            </Grid>

        </Grid>
    );

};

export default CardsInicio;