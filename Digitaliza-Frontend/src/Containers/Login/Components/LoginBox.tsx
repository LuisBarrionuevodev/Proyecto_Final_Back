import { Box, Button, TextField, Typography } from "@mui/material";
import { ButtonStyle, InputStyles, LoginBoxGlobalStyle, LoginBoxInputStyles, LoginBoxStyle, LoginLogoStyle } from "../../../styles/LoginStyles";
import Logo from "../assets-login/Logo.svg"
import type { JSX } from "react";
import { useNavigate } from "react-router-dom";



const LoginBox = () : JSX.Element => {

    const navigate = useNavigate()

    const handleOnClick = () => {
        navigate("/inicio")
    }

    return (
        <Box sx={LoginBoxGlobalStyle}>
            <Box sx={LoginBoxStyle}>
                <Box sx={LoginLogoStyle}>
                    <img src={Logo} alt="" style={{ width: "100px" }} />
                </Box>
                <Box sx={LoginLogoStyle}>

                    <Typography sx={{ fontFamily: "Tactic Sans", fontWeight: 500, fontSize: "35px" }}>
                        Iniciar Sesión
                    </Typography>

                </Box>
                <Box sx={LoginBoxInputStyles}>

                    <TextField sx={InputStyles}
                        placeholder="Usuario">

                    </TextField>
                    <TextField sx={InputStyles}
                        placeholder="Contraseña">

                    </TextField>

                    <Button sx={ButtonStyle} onClick={handleOnClick}>
                        Ingresar
                    </Button>

                </Box>
            </Box>
        </Box>
    )

}

export default LoginBox;