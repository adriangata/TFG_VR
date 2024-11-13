import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.proportion import proportion_confint
from scipy import stats

# Función para calcular el intervalo de confianza de Clopper-Pearson
def clopper_pearson(n, x, alpha=0.05):
    return proportion_confint(x, n, alpha=alpha, method='binom_test')

ruta = 'D:\\ADRIÁN\\Estudios\\Universidad UEX\\zzzTFG\\Datos\\*.xlsx'  # importante las \\ para evitar errores de escape en la cadena de la ruta

dfs = []

for archivo in glob.glob(ruta):
    df = pd.read_excel(archivo)
    dfs.append(df)  # Agrega el DataFrame a la lista

df_concat = pd.concat(dfs, ignore_index=True)  # se unen todos los dataframes

df_concat = df_concat.drop(df_concat.columns[[2] + list(range(4, df_concat.shape[1]))], axis=1)  # borramos las columnas que no interesan

acierto = 'S05N (Instance)'
df_concat['Resultado'] = df_concat['Choose Option'].apply(lambda x: 1 if x == acierto else 0)  # nueva columna: 1 es acierto, 0 es fallo

df_concat = df_concat[pd.to_numeric(df_concat['Time'], errors='coerce').notnull()]  # convierte 'Time' a un valor numérico, y luego filtra el DataFrame eliminando las filas donde null

# Crear 4 dataframes, uno por cada color
dfs_luces = {luz: df_concat[df_concat['Lighting'] == luz] for luz in df_concat['Lighting'].unique()}  # se crean varios dataframes, uno por cada color

n = 40  # Tamaño de la muestra
Z = 1.96  # Valor Z para un nivel de confianza del 95%

for luz, dfs_luz in dfs_luces.items():
    dfs_luz = dfs_luz.reset_index(drop=True)

    if luz == 'Red':
        nombre_luz = 'rojo'
        color_grafico = 'red'
    elif luz == 'Blue':
        nombre_luz = 'azul'
        color_grafico = 'blue'
    elif luz == 'Green':
        nombre_luz = 'verde'
        color_grafico = 'green'
    else:
        nombre_luz = 'D65'
        color_grafico = 'white'
        
    print(f"% de acierto para la luz: {luz}")

    promedio_acierto = dfs_luz.groupby('Time')['Resultado'].mean().reset_index()

    

    # Calcular el intervalo de confianza de Clopper-Pearson
    for index, row in promedio_acierto.iterrows():
        p = row['Resultado']
        x = p * n  # Número de éxitos
        lower_ci, upper_ci = clopper_pearson(n, x)  # IC de Clopper-Pearson
        error_estandar = (upper_ci - lower_ci) / 2  # Error como la mitad del rango

        # Añadir error estándar como nueva columna
        promedio_acierto.at[index, 'error_estandar'] = round(upper_ci - lower_ci) / 2  # Error como la mitad del rango


        # Asegúrate de que no sea negativo
        error_estandar = max(0, error_estandar)
        promedio_acierto.at[index, 'error_estandar'] = error_estandar

    print(promedio_acierto)    

    plt.style.use('seaborn-v0_8-dark-palette')  # Cambia el estilo del gráfico
    plt.figure(figsize=(8, 6))  # Ajusta el tamaño del gráfico

    # Graficar con barras de error
    plt.errorbar(promedio_acierto['Time'], promedio_acierto['Resultado'],
                 yerr=promedio_acierto['error_estandar'].clip(lower=0), fmt='o', color=color_grafico,
                 ecolor='black', elinewidth=1, capsize=4, markeredgecolor='black', markersize=8)

    plt.xlabel('Tiempo (en segundos)', fontsize=12)
    plt.ylabel('Porcentaje de acierto (normalizado)', fontsize=12)
    plt.title(f"Porcentaje de acierto para el iluminante {nombre_luz}", fontsize=14, fontweight='bold')

    plt.ylim(-0.1, 1.1)
    plt.grid(True, linestyle='--', alpha=0.7)  # Ajusta el estilo de la cuadrícula

    plt.tight_layout()  # Ajusta automáticamente los márgenes
    plt.show()

    # Extraer los resultados para time=0 y time=120
    resultado_0 = promedio_acierto[promedio_acierto['Time'] == 20.0]['Resultado'].values[0]
    resultado_120 = promedio_acierto[promedio_acierto['Time'] == 120.0]['Resultado'].values[0]

    # Número de muestras para cada tiempo
    n_0 = n  # Tamaño de muestra para time=0
    n_120 = n  # Tamaño de muestra para time=120

    # Calcular la prueba Z
    p1 = resultado_0  # Proporción de aciertos en time=0
    p2 = resultado_120  # Proporción de aciertos en time=120

    # Calculando el error estándar
    p = (p1 * n_0 + p2 * n_120) / (n_0 + n_120)
    se = np.sqrt(p * (1 - p) * (1/n_0 + 1/n_120))

    # Calcular la estadística Z
    z = (p1 - p2) / se

    # Valor p (bilateral)
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    print(f"Estadística Z: {z:.3f}, valor p: {p_value:.3f}")
    if p_value < 0.05:
        print("Hay un aumento significativo en el porcentaje de aciertos entre time=0 y time=120.")
    else:
        print("No hay un aumento significativo en el porcentaje de aciertos entre time=0 y time=120.")

    # Opciones a contar
    opciones = ['S05N (Instance)', 'S05R50B (Instance)', 'S05Y (Instance)', 
                'S05Y50R (Instance)', 'S05G (Instance)', 'S05B (Instance)', 
                'S05B50G (Instance)', 'S05R (Instance)', 'S05G50Y (Instance)']

    # Mapa de letras para cada opción
    letras = {
        'S05N (Instance)': 'N',  # Gray
        'S05R50B (Instance)': 'RB',  # Rojo azulado (Purple)
        'S05Y (Instance)': 'Y',  # Yellow
        'S05Y50R (Instance)': 'YR',  # Orange
        'S05G (Instance)': 'G',  # Green
        'S05B (Instance)': 'B',  # Blue
        'S05B50G (Instance)': 'BG',  # Azul verdoso (Aqua)
        'S05R (Instance)': 'R',  # Red
        'S05G50Y (Instance)': 'GY'   # Verde amarillento (Light Green)
    }

    # Colores asociados
    colores = {
        'S05N (Instance)': 'gray',  
        'S05R50B (Instance)': '#8A2BE2',  # Rojo azulado
        'S05Y (Instance)': 'yellow',
        'S05Y50R (Instance)': 'orange',
        'S05G (Instance)': 'green',
        'S05B (Instance)': 'blue',
        'S05B50G (Instance)': '#20B2AA',  # Azul verdoso
        'S05R (Instance)': 'red',
        'S05G50Y (Instance)': '#ADFF2F'   # Verde amarillento
    }

    # Almacenar los resultados
    resultados = {}

    conteo = dfs_luz['Choose Option'].value_counts()
    resultados[luz] = {opcion: conteo.get(opcion, 0) for opcion in opciones}

    # Filtrar resultados para excluir los valores con 0
    resultados_filtrados = {opcion: valor for opcion, valor in resultados[luz].items() if valor > 0}

    # Ordenar los resultados filtrados de mayor a menor
    resultados_ordenados = dict(sorted(resultados_filtrados.items(), key=lambda item: item[1], reverse=True))

    # Crear gráfico circular solo si hay opciones con valores > 0
    if resultados_ordenados:
        plt.figure(figsize=(8, 8))
        plt.pie(resultados_ordenados.values(),
                labels=[letras[opcion] for opcion in resultados_ordenados.keys()],
                autopct=lambda p: f'{p:.1f}',
                colors=[colores[opcion] for opcion in resultados_ordenados.keys()],
                startangle=90,
                pctdistance=0.85)  # Ajusta la distancia de los porcentajes

        plt.title(f'% de selección en el iluminante {nombre_luz}', pad=25)
        plt.axis('equal')  # Para que el gráfico sea un círculo
        plt.tight_layout()  # Ajusta el diseño automáticamente para evitar solapamiento
        plt.show()

