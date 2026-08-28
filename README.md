# Adivina mi dibujo

Aplicación web que permite dibujar en un canvas y utilizar un modelo de inteligencia artificial para intentar reconocer el dibujo.

El modelo reconoce 5 categorías:

* Manzana
* Auto
* Casa
* Estrella
* Árbol

## Tecnologías

* React + Vite
* Python
* FastAPI
* ONNX Runtime
* Pillow
* NumPy
* Axios
* TensorFlow/Keras

## Estructura

```text
adivina_mi_dibujo/
├── backend/
├── frontend/
├── modelo.onnx
├── convertir_modelo.py
├── limpiar_modelo.py
├── probar_modelo.py
└── probar_onnx.py
```

## Instalación

### Backend

Desde la carpeta principal, crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows:

```bash
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install fastapi uvicorn python-multipart pillow onnxruntime numpy
```

Ejecutar el backend:

```bash
uvicorn backend.main:app --reload
```

El backend quedará disponible en:

```text
http://127.0.0.1:8000
```

### Frontend

Abrir otra terminal en la carpeta principal y entrar a `frontend`:

```bash
cd frontend
```

Instalar las dependencias:

```bash
npm install
```

Ejecutar:

```bash
npm run dev
```

La aplicación estará disponible normalmente en:

```text
http://localhost:5173
```

## Uso

1. Abrir la aplicación en el navegador.
2. Dibujar una de las cinco categorías.
3. Las predicciones aparecen automáticamente mientras se dibuja.
4. También se puede utilizar el botón **Adivinar** para realizar una predicción inmediata.
5. El botón **Limpiar** permite comenzar un nuevo dibujo.

## Funcionamiento

El dibujo realizado en React se convierte en una imagen y se envía al backend mediante Axios. FastAPI recibe la imagen, la prepara y la envía al modelo `modelo.onnx` mediante ONNX Runtime.

Para finalizar, el modelo devuelve las tres clases con mayor probabilidad.

## Nota

Las predicciones pueden variar, especialmente cuando el dibujo está incompleto o se realiza con formas diferentes a las utilizadas durante el entrenamiento. El modelo está limitado a las cinco categorías indicadas anteriormente.
