import { BrowserRouter as Router, Routes, Route, Navigate, } from "react-router-dom";
import Login from "./Containers/Login";
import Inicio from "./Containers/Inicio";
import Actuaciones from "./Containers/Actuaciones";
import CargarRelevamientos from "./Containers/CargarRelevamientos";
import CargarActuaciones from "./Containers/CargarActuaciones";
import Dashboard from "./Containers/Dashboard";

function App() {


  return (

    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={ <Login/> } />
        <Route path="/inicio" element={ <Inicio/> } />
        <Route path="/actuaciones" element={ <Actuaciones/> } />
        <Route path="/cargarRelevamiento" element={ <CargarRelevamientos/> } />
        <Route path="/cargarActuacion" element={ <CargarActuaciones/> } />
        <Route path="/dashboard" element={ <Dashboard/> } />
      </Routes>
    </Router>

  )
}

export default App
