import pandas as pd
import glob #para leer todo lo que haya en una carpeta
import os

ruta = 'D:\\ADRIÁN\\Estudios\\Universidad UEX\\zzzTFG\\Datos\\*.xlsx' #importante las \\ para para evitar errores de escape en la cadena de la ruta

dfs = []
nombres_archivos = []

for archivo in glob.glob(ruta):
    df = pd.read_excel(archivo)
    dfs.append(df)  # Agrega el DataFrame a la lista

    nombre_archivo_completo = os.path.basename(archivo)
     # Eliminar la extensión del archivo y quitar el sufijo después del guion bajo
    nombre_archivo, _ = os.path.splitext(nombre_archivo_completo)
    nombre_archivo = nombre_archivo.split('_')[0]  # Obtener solo la parte antes del guion bajo ()
    nombres_archivos.append(nombre_archivo)

suma1=0
suma2=0
suma3=0
suma4=0

for i in range(len(dfs)):
    df=dfs[i]
    df = df.drop(df.columns[[2] + list(range(4, df.shape[1]))], axis=1)
    df = df[df['Lighting'] == 'D65']
    df=df.reset_index(drop=True)
    acierto = 'S05N (Instance)'
    df['Resultado'] = df['Choose Option'].apply(lambda x: 1 if x == acierto else 0) #nueva columna: 1 es acierto, 0 es fallo
    
    if ((df['Time'] == 100) & (df['Resultado'] == 1)).any() and ((df['Time'] == 120) & (df['Resultado'] == 0)).any():
        print(nombres_archivos[i])
        print(df)  
        suma1+=1
    if ((df['Time'] == 100) & (df['Resultado'] == 1)).any() and ((df['Time'] == 120) & (df['Resultado'] == 1)).any():
        suma2+=1
    if ((df['Time'] == 100) & (df['Resultado'] == 0)).any() and ((df['Time'] == 120) & (df['Resultado'] == 1)).any():        
        suma3+=1
    if ((df['Time'] == 100) & (df['Resultado'] == 0)).any() and ((df['Time'] == 120) & (df['Resultado'] == 0)).any():
        suma4+=1
        



print (f'ACierta la penultima pero no la ultima:{suma1}')
print (f'ACierta la penultima y la ultima:{suma2}')
print (f'Falla la penultima y acierta la ultima:{suma3}')
print (f'Falla las dos ultimas:{suma4}')