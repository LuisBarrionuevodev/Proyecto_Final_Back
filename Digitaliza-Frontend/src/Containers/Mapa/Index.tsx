// src/components/BromatoMap.tsx
// por ejemplo: src/pages/PanelGeografico.tsx
import NavLeft from "../../Componets/NavLeft";
import BromatoMap from "./Components/BromatoApp";

const PanelGeografico = () => {
  return (
   <>
    <NavLeft />
    <div style={{ padding: 16, marginLeft: 300 }}>
      <h2>Mapa de inspecciones - Bromatología</h2>
      <BromatoMap />
    </div>
     </>
  );
};

export default PanelGeografico;

