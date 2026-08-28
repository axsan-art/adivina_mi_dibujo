import numpy as np

# Compatibilidad con TensorFlow.js y NumPy
np.object = object
np.bool = bool

import tensorflowjs as tfjs

print("TensorFlow.js cargado correctamente.")

tfjs.converters.save_keras_model(
    "adivina_mi_dibujo.keras",
    "modelo_tfjs"
)

print("Modelo convertido correctamente.")