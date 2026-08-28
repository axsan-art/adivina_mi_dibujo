import { useRef, useState } from "react";
import axios from "axios";

function App() {
  const canvasRef = useRef(null);
  const temporizadorRef = useRef(null);
  const intervaloRef = useRef(null);

  const [dibujando, setDibujando] = useState(false);
  const [predicciones, setPredicciones] = useState([]);
  const [programaActivo, setProgramaActivo] = useState(false);

  const comenzarDibujo = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    ctx.beginPath();
    ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);

    setDibujando(true);
    setProgramaActivo(true);
    

    if (temporizadorRef.current) {
      clearTimeout(temporizadorRef.current);
    }

    intervaloRef.current = setInterval(() => {
      adivinar();
    }, 1500);
  };

  const dibujar = (e) => {
    if (!dibujando) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    ctx.lineWidth = 8;
    ctx.lineCap = "round";
    ctx.strokeStyle = "black";

    ctx.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    ctx.stroke();
  };

  const terminarDibujo = () => {

    if (!dibujando) return;

    setDibujando(false);

    if (intervaloRef.current) {
      clearInterval(intervaloRef.current);
    }

    temporizadorRef.current = setTimeout(() => {
      adivinar();
    }, 1500);
  };

  const limpiarCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    setPredicciones([]);
    setProgramaActivo(false);

    if (temporizadorRef.current) {
      clearTimeout(temporizadorRef.current);
    }

    if (intervaloRef.current) {
      clearInterval(intervaloRef.current);
    }
  };

  const adivinar = async () => {
    const canvas = canvasRef.current;

    canvas.toBlob(async (blob) => {
      const formulario = new FormData();

      formulario.append("imagen", blob, "dibujo.png");

      try {
        const respuesta = await axios.post(
          "http://127.0.0.1:8000/predecir",
          formulario
        );

        setPredicciones(respuesta.data.predicciones);
      } catch (error) {
        console.error("Error al enviar el dibujo:", error);
      }
    }, "image/png");
  };

  return (
    <div>
      <h1>Adivina mi dibujo</h1>

      {programaActivo && (
        <p>
          🟢 Programa activo - analizando tu dibujo...
        </p>
      )}

      <canvas
        ref={canvasRef}
        width={400}
        height={400}
        style={{
          border: "2px solid black",
          backgroundColor: "white"
        }}
        onMouseDown={comenzarDibujo}
        onMouseMove={dibujar}
        onMouseUp={terminarDibujo}
        onMouseLeave={terminarDibujo}
      />

      <br />

      <button onClick={limpiarCanvas}>
        Limpiar
      </button>

      <button onClick={adivinar}>
        Adivinar
      </button>

      <div>
        <h2>Predicciones</h2>

        {predicciones.map((prediccion, indice) => (
          <p key={indice}>
            {indice + 1}. {prediccion.clase} -{" "}
            {(prediccion.confianza * 100).toFixed(2)}%
          </p>
        ))}
      </div>
    </div>
  );
}

export default App;