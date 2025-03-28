import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

ruta = 'D:\\ADRIÁN\\Estudios\\Universidad UEX\\zzzTFG\\Datos\\*.xlsx'

dfs = []
nombres_archivos = []

for archivo in glob.glob(ruta):
    df = pd.read_excel(archivo)
    dfs.append(df)

    nombre_archivo_completo = os.path.basename(archivo)
    nombre_archivo, _ = os.path.splitext(nombre_archivo_completo)
    nombre_archivo = nombre_archivo.split('_')[0]
    nombres_archivos.append(nombre_archivo)

luces = ['Red', 'D65', 'Green', 'Blue']
resultados_fallos = {}

for luz in luces:
    suma = 0

    for i in range(len(dfs)):
        df = dfs[i]
        nombre_persona = nombres_archivos[i]
        df = df.drop(df.columns[[2] + list(range(4, df.shape[1]))], axis=1)
        df = df[df['Lighting'] == luz]
        df = df.reset_index(drop=True)
        acierto = 'S05N (Instance)'
        df['Resultado'] = df['Choose Option'].apply(lambda x: 1 if x == acierto else 0)

        for t in range(20, 121, 20):
            if ((df['Time'] == t) & (df['Resultado'] == 0)).any():
                if t == 120:
                    suma += 1
            if ((df['Time'] == t) & (df['Resultado'] == 1)).any():
                break

    
    resultados_fallos[luz] = suma

for luz, num_fallos in resultados_fallos.items():
    if luz == 'Red':
        nombre_luz = 'roja'
    elif luz == 'Blue':
        nombre_luz = 'azul'
    elif luz == 'Green':
        nombre_luz = 'verde'
    else:
        nombre_luz = 'D65'
    print(f'El número de personas que no ha acertado ninguna en luz {nombre_luz} es: {num_fallos}')

total_personas = len(dfs)
porcentaje_fallos = {luz: (fallos / total_personas) * 100 for luz, fallos in resultados_fallos.items()}

plt.figure(figsize=(8, 6))
plt.bar(['Rojo', 'D65', 'Verde', 'Azul'], porcentaje_fallos.values(), color=['red', 'gray', 'green', 'blue'])
plt.xlabel('Condición de luz')
plt.ylabel('Porcentaje de fallos (%)')
plt.ylim(0, 100)
plt.title('Personas sin ningún acierto para cada iluminante')
plt.show()
