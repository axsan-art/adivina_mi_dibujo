from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import onnxruntime as ort
import numpy as np
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo ONNX
sesion = ort.InferenceSession("modelo.onnx")

# Nombres de las 5 clases
clases = [
    "manzana",
    "auto",
    "casa",
    "estrella",
    "arbol"
]


@app.get("/")
def inicio():
    return {"mensaje": "API Adivina mi dibujo funcionando"}


@app.post("/predecir")
async def predecir(imagen: UploadFile = File(...)):

    # Leer la imagen
    contenido = await imagen.read()

    with open("dibujo_recibido.png", "wb") as archivo:
        archivo.write(contenido)

    # Abrir y preparar la imagen
    img = Image.open(io.BytesIO(contenido))

    # Crear fondo blanco
    fondo = Image.new("RGBA", img.size, "white")

    # Colocar el dibujo sobre el fondo blanco
    fondo.alpha_composite(img)

    # Convertir a escala de grises
    img = fondo.convert("L")

    # Reducir a 28x28
    img = img.resize((28, 28))

    # Convertir a números
    datos = np.array(img).astype(np.float32)

    # Invertir colores
    datos = 255.0 - datos

    # Normalizar
    datos = datos / 255.0

    # Agregar dimensiones: (1, 28, 28, 1)
    datos = datos.reshape(1, 28, 28, 1)

    # Obtener nombre de entrada del modelo
    nombre_entrada = sesion.get_inputs()[0].name

    # Realizar predicción
    resultado = sesion.run(None, {nombre_entrada: datos})

    probabilidades = resultado[0][0]

    # Obtener las 3 mejores predicciones
    indices = np.argsort(probabilidades)[::-1][:3]

    predicciones = []

    for indice in indices:
        predicciones.append({
            "clase": clases[indice],
            "confianza": float(probabilidades[indice])
        })

    return {
        "predicciones": predicciones
    }