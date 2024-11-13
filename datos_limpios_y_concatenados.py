import pandas as pd
import glob 
import os

ruta = 'D:\\ADRIÁN\\Estudios\\Universidad UEX\\zzzTFG\\Datos\\*.xlsx'  # importante las \\ para evitar errores de escape en la cadena de la ruta

dfs = []
nombres_archivos = []

# Lee todos los archivos Excel y procesa los DataFrames
for i, archivo in enumerate(glob.glob(ruta), start=1):  # Usa enumerate para contar desde 1
    df = pd.read_excel(archivo)

    nombre_archivo_completo = os.path.basename(archivo)
    # Eliminar la extensión del archivo y quitar el sufijo después del guion bajo
    nombre_archivo, _ = os.path.splitext(nombre_archivo_completo)
    nombre_archivo = nombre_archivo.split('_')[0]  # Obtener solo la parte antes del guion bajo
    nombres_archivos.append(nombre_archivo)

    df = df.drop(df.columns[[2] + list(range(4, df.shape[1]))], axis=1)  # borramos las columnas que no interesan

    # Quitar '(Instance)' de la columna 3
    df.iloc[:, 2] = df.iloc[:, 2].str.replace('(Instance)', '', regex=False)

    acierto = 'S05N '
    df['Resultado'] = df['Choose Option'].apply(lambda x: 1 if x == acierto else 0)  # nueva columna: 1 es acierto, 0 es fallo

    df = df[pd.to_numeric(df['Time'], errors='coerce').notnull()]  # convierte 'Time' a un valor numérico, y luego filtra el DataFrame eliminando las filas donde null

    # Insertar el nombre en la primera celda de la primera fila
    df.loc[-1] = [f'Persona {i}'] + [None] * (df.shape[1] - 1)  # Añadir una nueva fila al inicio
    df.index = df.index + 1  # Aumentar el índice
    df = df.sort_index()  # Ordenar el índice para que la nueva fila esté en la parte superior


    dfs.append(df)  # Agrega el DataFrame a la lista
    print(nombre_archivo)
    print(f'persona{i}')
    #print(df)

# Concatenar todos los DataFrames en uno solo
df_concatenado = pd.concat(dfs, ignore_index=True)
#print (df_concatenado)

# Guardar el DataFrame concatenado como un archivo Excel
df_concatenado.to_excel('Datos_Concatenados.xlsx', index=False)


