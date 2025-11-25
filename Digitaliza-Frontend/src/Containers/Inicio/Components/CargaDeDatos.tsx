import { Box, Button, Grid, Typography } from "@mui/material";
import LogoSuma from "../assets-inicio/LogoSuma.svg"
import type { JSX } from "react";
import { BoxInicio, BoxInputInicio, BoxTitulo, ButtonStylesInicio, LogoSumaStyle, TitleStyle } from "../../../styles/InicioStyles";

const CargaDeDatos = (): JSX.Element => {

    return (
        <Box sx={BoxInicio}>
            <Box sx={BoxTitulo}>
                <Typography sx={TitleStyle}>
                    Gestion de expedientes
                </Typography>
            </Box>

            <Grid container 
            direction={{ xs: "column", md: "row" }} 
            rowSpacing={2} 
            sx={BoxInputInicio}>
                <Grid>
                    <a href="/cargarActuacion">
                    <Button sx={ButtonStylesInicio}>

                        <Box component={"img"} 
                        src={LogoSuma} 
                        sx={LogoSumaStyle} />

                        Cargar Actuacion

                    </Button>
                    </a>
                </Grid>

                <Grid>
                    <a href="/cargarRelevamiento">
                    <Button sx={ButtonStylesInicio}>

                        <Box component={"img"} 
                        src={LogoSuma} 
                        sx={LogoSumaStyle} />

                        Cargar Relevamiento
                    </Button>
                    </a>
                </Grid>
            </Grid>
        </Box>
    )

}

export default CargaDeDatos;