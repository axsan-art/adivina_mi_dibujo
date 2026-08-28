import zipfile
import json
import shutil
import os

archivo_original = "adivina_mi_dibujo.keras"
archivo_limpio = "modelo_limpio.keras"

# Crear una copia temporal
with zipfile.ZipFile(archivo_original, "r") as zip_original:

    with zipfile.ZipFile(archivo_limpio, "w") as zip_limpio:

        for archivo in zip_original.namelist():

            datos = zip_original.read(archivo)

            # Modificar solamente config.json
            if archivo == "config.json":

                config = json.loads(datos.decode("utf-8"))

                def limpiar(obj):
                    if isinstance(obj, dict):

                        # Eliminar quantization_config
                        obj.pop("quantization_config", None)

                        for valor in obj.values():
                            limpiar(valor)

                    elif isinstance(obj, list):

                        for valor in obj:
                            limpiar(valor)

                limpiar(config)

                datos = json.dumps(config).encode("utf-8")

            zip_limpio.writestr(archivo, datos)

print("Modelo limpio creado correctamente.")
print("Archivo:", archivo_limpio)
print("Existe:", os.path.exists(archivo_limpio))