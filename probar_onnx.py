import onnxruntime as ort

sesion = ort.InferenceSession("modelo.onnx")

print("Modelo ONNX cargado correctamente.")

entrada = sesion.get_inputs()[0]
salida = sesion.get_outputs()[0]

print("Entrada:", entrada.name)
print("Forma:", entrada.shape)

print("Salida:", salida.name)
print("Forma:", salida.shape)