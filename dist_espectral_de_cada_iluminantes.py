import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

ruta = 'D:\\ADRIÁN\\Estudios\\Universidad UEX\\zzzTFG\\Iluminantes\\*.xlsx'

dfs = []
nombres_archivos = []

for archivo in glob.glob(ruta):
    df = pd.read_excel(archivo, dtype=float, decimal=',', header=None)
    dfs.append(df)

    nombre_archivo_completo = os.path.basename(archivo).split('.')[0]
    nombres_archivos.append(nombre_archivo_completo)

for i, df in enumerate(dfs):

    if nombres_archivos[i] == 'Red':
        nombre_luz = 'rojo'
        color_grafico='red'
    elif nombres_archivos[i] == 'Blue':
        nombre_luz = 'azul'
        color_grafico='blue'
    elif nombres_archivos[i] == 'Green':
        nombre_luz = 'verde'
        color_grafico='green'
    else:
        nombre_luz = 'D65'
        color_grafico='black'
    
    print(f"df de {nombre_luz}")
    print(df)

    x = np.linspace(380, 780, len(df))

    plt.plot(x, df.iloc[:, 0], color=color_grafico)
    plt.xlim(380,780)
    plt.xlabel("Longitud de onda (nm)")
    plt.ylim(0, 0.02)
    plt.ylabel("Distribución de energía espectral (W/m²/nm)")
    plt.title(f"Iluminante {nombre_luz}")
    plt.show()
