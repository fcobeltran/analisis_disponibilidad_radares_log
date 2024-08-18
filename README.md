# analisis_disponibilidad_radares_log
Analiza la disponibilidad de radares a partir de logs, generando gráficos con líneas de tendencia y permitiendo guardar resultados como imágenes o en Excel//Analyzes radar availability from logs, generating charts with trend lines and allowing results to be saved as images or Excel files

# Proyecto de Análisis de Disponibilidad de Radar / Radar Availability Analysis Project

## Descripción en Español

Este proyecto analiza la disponibilidad de radares utilizando archivos de log generados por el sistema de monitoreo de los radares. El script permite procesar múltiples archivos de log, combinar los datos, generar gráficos de disponibilidad diaria con líneas de tendencia, y calcular la disponibilidad promedio total. El resultado se presenta en una interfaz gráfica de usuario (GUI) que permite guardar los resultados en archivos de imagen y Excel.

### Características
- Procesa múltiples archivos de log de radar.
- Calcula la disponibilidad diaria y la disponibilidad promedio total.
- Genera gráficos con barras de disponibilidad diaria, líneas de tendencia y una tabla de disponibilidad por día.
- Interfaz gráfica de usuario (GUI) para facilitar la visualización y el guardado de resultados.

## Project Description in English

This project analyzes radar availability using log files generated by the radar monitoring system. The script processes multiple log files, combines the data, generates daily availability charts with trend lines, and calculates the overall average availability. The results are presented in a graphical user interface (GUI) that allows saving the results as image and Excel files.

### Features
- Processes multiple radar log files.
- Calculates daily availability and overall average availability.
- Generates charts with daily availability bars, trend lines, and a daily availability table.
- User-friendly GUI for easy visualization and saving of results.

## Instalación / Installation

### Requisitos / Requirements
- Python 3.7+
- Matplotlib
- Numpy
- Pandas
- Tkinter (generalmente incluido con Python)
- PIL (Python Imaging Library)

### Instrucciones / Instructions

1. **Clonar el repositorio / Clone the repository:**
    ```bash
    git clone https://github.com/fcobeltran/analisis_disponibilidad_radares_log.git
    cd analisis_disponibilidad_radares_log
    ```

2. **Instalar las dependencias / Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecutar el script / Run the script:**
    ```bash
    python nombre_del_script.py
    ```

## Uso / Usage

1. Al ejecutar el script, aparecerá una ventana emergente donde podrás seleccionar los archivos de log a procesar.
2. El sistema procesará los archivos, calculará la disponibilidad diaria y generará un gráfico con la línea de tendencia y una tabla con los valores de disponibilidad diaria.
3. Podrás guardar los resultados como imagen y como archivo Excel.

### Ejemplo de Uso / Usage Example

```bash
python radar_availability_analysis.py
