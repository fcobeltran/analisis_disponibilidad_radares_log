# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:53:55 2024

@author: CPU
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from tkinter import Tk, filedialog, messagebox, Toplevel, Label, Canvas, Frame, Scrollbar, RIGHT, Y, Listbox, END
from PIL import Image, ImageTk

def extract_availability_data(file_path):
    with open(file_path, 'r') as file:
        log_lines = file.readlines()

    psv_creation_pattern = re.compile(r"New Psv Created")
    date_pattern = re.compile(r"(\d{2}-\w{3}-\d{2})")

    daily_psv_count = defaultdict(int)

    for line in log_lines:
        if psv_creation_pattern.search(line):
            date_match = date_pattern.search(line)
            if date_match:
                date = date_match.group(1)
                daily_psv_count[date] += 1

    return daily_psv_count

def adjust_availability_data(daily_psv_count):
    dates = list(daily_psv_count.keys())
    
    # Ignorar el primer y último día si los registros son menores de lo esperado
    if len(dates) > 1:
        if daily_psv_count[dates[0]] < 720:
            del daily_psv_count[dates[0]]
        if daily_psv_count[dates[-1]] < 720:
            del daily_psv_count[dates[-1]]

    return daily_psv_count

def calculate_and_plot_availability(combined_df, radar_name):
    expected_data_points = 720
    
    # Calcular disponibilidad diaria y asegurar que no exceda 100%
    combined_df['Availability (%)'] = (combined_df['Count'] / expected_data_points) * 100
    combined_df['Availability (%)'] = combined_df['Availability (%)'].clip(upper=100)
    
    # Asegurarse de que los valores de disponibilidad son numéricos
    combined_df['Availability (%)'] = pd.to_numeric(combined_df['Availability (%)'], errors='coerce')
    
    # Calcular disponibilidad promedio total
    average_availability = combined_df["Availability (%)"].mean()
    
    # Crear el gráfico de disponibilidad
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(combined_df["Date"], combined_df["Availability (%)"], color='skyblue')
    
    # Calcular y agregar la línea de tendencia
    x_values = np.arange(len(combined_df))
    z = np.polyfit(x_values, combined_df["Availability (%)"], 1)
    p = np.poly1d(z)
    ax.plot(combined_df["Date"], p(x_values), "r--", label='Tendencia')

    ax.set_xlabel('Fecha')
    ax.set_ylabel('Disponibilidad (%)')
    ax.set_title(f'Disponibilidad del Radar por Día ({radar_name})')
    ax.set_xticklabels(combined_df["Date"], rotation=45, ha='right')
    ax.set_ylim([0, 110])  # Asegura que el gráfico no suba más allá de 100%
    ax.legend()
    plt.tight_layout()

    return combined_df, average_availability, fig

def save_figure(fig, radar_name):
    # Abrir cuadro de diálogo para guardar la imagen
    output_image_path = filedialog.asksaveasfilename(
        title="Guardar imagen del gráfico",
        defaultextension=".png",
        filetypes=(("Archivo PNG", "*.png"), ("Todos los archivos", "*.*"))
    )
    if output_image_path:
        fig.savefig(output_image_path)
        print(f'Imagen del gráfico guardada en {output_image_path}')
    else:
        print("La imagen no se guardó.")

def display_results(fig, average_availability, radar_name, combined_df):
    # Crear ventana emergente
    result_window = Toplevel()
    result_window.title(f"Informe de Disponibilidad - {radar_name}")
    
    # Ajustar el tamaño de la ventana emergente
    result_window.geometry("1400x800")
    
    # Mostrar disponibilidad promedio en la ventana emergente
    Label(result_window, text=f"Disponibilidad promedio total del radar {radar_name}: {average_availability:.2f}%", font=("Arial", 14)).pack(pady=10)
    
    # Crear un marco para el gráfico y la tabla
    frame = Frame(result_window)
    frame.pack(side="left", fill="both", expand=True)
    
    # Mostrar el gráfico en la ventana emergente
    canvas = Canvas(frame)
    canvas.pack(fill="both", expand=True)

    # Convertir la figura de Matplotlib a una imagen que Tkinter pueda mostrar
    fig.canvas.draw()
    img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    img_tk = ImageTk.PhotoImage(img)

    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.img_tk = img_tk  # Necesario para mantener la referencia

    # Guardar la imagen del gráfico
    save_figure(fig, radar_name)

    # Crear un marco para la tabla de disponibilidad
    table_frame = Frame(result_window)
    table_frame.pack(side="right", fill="y")

    # Crear una barra de desplazamiento
    scrollbar = Scrollbar(table_frame, orient="vertical")
    scrollbar.pack(side=RIGHT, fill=Y)

    # Crear una lista para mostrar la tabla
    listbox = Listbox(table_frame, yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)

    # Rellenar la lista con los datos de disponibilidad
    for index, row in combined_df.iterrows():
        listbox.insert(END, f"{row['Date']}: {row['Availability (%)']:.2f}%")

    # Configurar la barra de desplazamiento
    scrollbar.config(command=listbox.yview)

    # Iniciar el loop de la ventana emergente y asegurarse de cerrar la aplicación correctamente
    result_window.protocol("WM_DELETE_WINDOW", result_window.destroy)
    result_window.mainloop()

def main():
    # Crear una ventana de selección de archivos
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    # Abrir un cuadro de diálogo para seleccionar múltiples archivos
    file_paths = filedialog.askopenfilenames(
        title="Selecciona los archivos de registro",
        filetypes=(("Archivos de Log", "*.log"), ("Todos los archivos", "*.*"))
    )

    if file_paths:
        combined_df = pd.DataFrame(columns=["Date", "Count"])
        radar_name = None
        
        for file_path in file_paths:
            # Extraer el nombre del radar del nombre del archivo
            file_name = os.path.basename(file_path)
            parts = file_name.split('_')
            radar_name = parts[0] if not radar_name else radar_name
            daily_psv_count = extract_availability_data(file_path)
            adjusted_psv_count = adjust_availability_data(daily_psv_count)
            
            # Convertir el diccionario a un DataFrame temporal
            temp_df = pd.DataFrame(list(adjusted_psv_count.items()), columns=["Date", "Count"])
            
            # Agregar los datos al DataFrame combinado
            combined_df = pd.concat([combined_df, temp_df], ignore_index=True)
        
        # Calcular la disponibilidad y crear el gráfico
        combined_df, avg_availability, fig = calculate_and_plot_availability(combined_df, radar_name)

        # Mostrar los resultados en la ventana emergente
        display_results(fig, avg_availability, radar_name, combined_df)

        # Guardar todos los datos en un archivo Excel si se procesaron múltiples archivos
        output_path = filedialog.asksaveasfilename(
            title="Guardar informe combinado",
            defaultextension=".xlsx",
            filetypes=(("Archivo Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
        )
        if output_path:
            combined_df.to_excel(output_path, index=False)
            print(f'Informe combinado guardado en {output_path}')
        else:
            print("El informe combinado no se guardó.")
    else:
        print("No se seleccionó ningún archivo.")

    root.quit()  # Asegurarse de que la ejecución se cierre correctamente

if __name__ == "__main__":
    main()
