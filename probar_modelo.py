import tensorflow as tf

modelo = tf.keras.models.load_model("modelo_limpio.keras")

print("Modelo cargado correctamente.")
modelo.summary()