# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import csv
import fileinput
import glob
import os
import zipfile


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    # Función para leer registros
    def load_files(input_directory):
        """Lee todas las líneas de los archivos en un directorio y retorna un generador."""
        files = glob.glob(os.path.join(input_directory, "*"))
        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    yield (line.strip(), os.path.basename(input_directory))

    # Función para exportar los datos a un archivo CSV
    def export_to_csv(data, output_directory, filename):
        """Exporta los datos a un archivo CSV en el directorio de salida."""
        # Crear el directorio de salida si no existe
        os.makedirs(output_directory, exist_ok=True)

        # Ruta completa del archivo de salida
        file_path = os.path.join(output_directory, filename)

        # Escribir los datos en un archivo CSV
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["phrase", "target"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow({"phrase": row[0], "target": row[1]})

    # Función para procesar los archivos
    def run_job(zip_file, output_directory):
        """Descomprime el archivo ZIP y procesa los archivos para generar CSVs."""

        def unzip_files(zip_file):
            """Descomprime los archivos ZIP en un directorio."""
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall("files/input")  # Directorio donde se descomprime el ZIP

        def process_files(input_directory, output_directory):
            """Procesa los archivos descomprimidos y genera los CSVs."""
            for folder in ["train", "test"]:  # Procesar las carpetas train y test
                data = []
                folder_path = os.path.join(input_directory, folder)
                for sentiment_folder in glob.glob(os.path.join(folder_path, "*")):
                    # Leer los archivos dentro de cada subcarpeta (positive, negative, neutral)
                    data.extend(load_files(sentiment_folder))

                # Nombre del archivo CSV basado en la carpeta (train o test)
                filename = f"{folder}_dataset.csv"
                export_to_csv(data, output_directory, filename)

        unzip_files(zip_file)  # Descomprimir el ZIP
        process_files("files/input", output_directory)  # Procesar archivos

    # Ejecutar el trabajo principal
    run_job("files/input.zip", "files/output")

    return "Proceso finalizado"


# Ejecutar la función principal
if __name__ == "__main__":
    print(pregunta_01())