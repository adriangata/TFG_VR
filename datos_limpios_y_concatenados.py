import pandas as pd
import glob 
import os

ruta = 'D:\\ADRIÁN\\Estudios\\Universidad UEX\\zzzTFG\\Datos\\*.xlsx'

dfs = []
nombres_archivos = []

for i, archivo in enumerate(glob.glob(ruta), start=1):
    df = pd.read_excel(archivo)

    nombre_archivo_completo = os.path.basename(archivo)
    nombre_archivo, _ = os.path.splitext(nombre_archivo_completo)
    nombre_archivo = nombre_archivo.split('_')[0]
    nombres_archivos.append(nombre_archivo)

    df = df.drop(df.columns[[2] + list(range(4, df.shape[1]))], axis=1)

    df.iloc[:, 2] = df.iloc[:, 2].str.replace('(Instance)', '', regex=False)

    acierto = 'S05N '
    df['Resultado'] = df['Choose Option'].apply(lambda x: 1 if x == acierto else 0)

    df = df[pd.to_numeric(df['Time'], errors='coerce').notnull()]
    df.loc[-1] = [f'Persona {i}'] + [None] * (df.shape[1] - 1)
    df.index = df.index + 1
    df = df.sort_index()


    dfs.append(df)
    print(nombre_archivo)
    print(f'persona{i}')

df_concatenado = pd.concat(dfs, ignore_index=True)

df_concatenado.to_excel('Datos_Concatenados.xlsx', index=False)


