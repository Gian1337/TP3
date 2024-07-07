'''Libreria con el funcionamiento principal del programa'''
import os
import pandas as pd
import matplotlib.pyplot as plt
from Lib import Var


def mostrarVictimasAnuales(pProvincia=None):
    try:
        #Lectura del origen de datos
        #file_path = os.path.join(Var.DATAPATH, 'data', 'snic-departamentos-anual.csv')
        df = pd.read_csv('victimas-data.csv', sep=";")
        
        if pProvincia is None:
            # Mostrar listado de provincias disponibles
            provincias_disponibles = df['provincia_nombre'].unique()
            print("Provincias disponibles:")
            for i, prov in enumerate(provincias_disponibles, start=1):
                print(f"{i}. {prov}")
            
            # Pedir al usuario que ingrese el número correspondiente a la provincia deseada
            seleccion = int(input("Ingrese el número de la provincia o '0' para volver: "))
            
            if seleccion == 0:
                return  # Salir si el usuario elige volver
            elif seleccion > 0 and seleccion <= len(provincias_disponibles):
                provincia_seleccionada = provincias_disponibles[seleccion - 1]
                mostrarVictimasAnuales(provincia_seleccionada)  # Llamar recursivamente con la provincia seleccionada
            else:
                print("Selección inválida. Intente de nuevo.")

        
        else:
            # Filtrar por la provincia deseada
            provincia_data = df[df['provincia_nombre'] == pProvincia]
            
            # Agrupar por año y sumar las víctimas
            totalVictimas = provincia_data.groupby('anio')['cantidad_victimas'].sum().reset_index()
            
            # Renombrar la columna cantidad_victimas a victimas
            totalVictimas = totalVictimas.rename(columns={'anio': 'AÑO'})
            totalVictimas = totalVictimas.rename(columns={'cantidad_victimas': 'VICTIMAS'})
            
            print(f"Total de víctimas por año en {pProvincia}:")
            print()
            print(totalVictimas.to_string(index=False))
            

            # Crear gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.bar(totalVictimas['AÑO'], totalVictimas['VICTIMAS'], color='red')
            plt.xlabel('Año')
            plt.ylabel('Número de víctimas')
            plt.title(f'Número de víctimas por año en {pProvincia}')
            plt.xticks(totalVictimas['AÑO'])
            plt.grid(True)
            plt.show()

    except pd.errors.ParserError as e:
        print(f"Error al leer el archivo .CSV: {e}")
    

def mostrarTiposDelitosRosario(pAño):
    try:
        df = pd.read_csv('victimas-data.csv', sep=";")
        #Filtra por departamento y por año
        rosario_data = df[(df['departamento_nombre'] == 'Rosario') & (df['anio'] == pAño)]
        
        #Agrupa por tipo de delito y cantidad
        tipos_delitos_cantidad = rosario_data.groupby('codigo_delito_snic_nombre')['cantidad_hechos'].sum().reset_index()
        print(f"Tipos de delitos en el departamento de Rosario en el año {pAño}:") 
        
        # Calcula el total de delitos
        total_delitos = tipos_delitos_cantidad['cantidad_hechos'].sum()
        
        # Calcula el porcentaje de cada tipo de delito
        tipos_delitos_cantidad['porcentaje'] = (tipos_delitos_cantidad['cantidad_hechos'] / total_delitos) * 100
        
        # Filtra los delitos que representan más del 1% del total
        delitos_mayores_1 = tipos_delitos_cantidad[tipos_delitos_cantidad['porcentaje'] > 1]
        
         # Ordena por porcentaje en orden descendente
        delitos_mayores_1 = delitos_mayores_1.sort_values(by='porcentaje', ascending=True)
        
        #Recorre los tipos de delitos con % mayor a 1
        '''
        NOTA: _, row: es una convención en Py que indica que la var no será usada. Recibe el índice de la fila.
        '''
        for _, row in delitos_mayores_1.iterrows():
            print(f"{row['codigo_delito_snic_nombre']}: {row['cantidad_hechos']}")
        
        # Crea gráfico de torta
        plt.figure(figsize=(10, 7))
        plt.pie(delitos_mayores_1['cantidad_hechos'], labels=delitos_mayores_1['codigo_delito_snic_nombre'], autopct='%1.1f%%', startangle=140)
        plt.title(f"Distribución de tipos de delitos en Rosario en el año {pAño}")
        plt.axis('equal')
        plt.show()
    except pd.errors.ParserError as e:
        print(f"Error al leer el archivo CSV: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
   
    
def mostrarDelitosPorSexo(pAño):
    try:
        df = pd.read_csv('victimas-data.csv', sep=";")
        data_anio = df[df['anio'] == pAño]
        
        # Suma las cantidades de víctimas masculinas y femeninas por provincia
        victimas_por_provincia = data_anio.groupby('provincia_nombre')[['cantidad_victimas_masc', 'cantidad_victimas_fem']].sum().reset_index()
        
        # datos para el gráfico
        provincias = victimas_por_provincia['provincia_nombre']
        victimas_masc = victimas_por_provincia['cantidad_victimas_masc']
        victimas_fem = victimas_por_provincia['cantidad_victimas_fem']
        
        # gráfico de barras según género
        x = range(len(provincias))
        
        plt.figure(figsize=(14, 8))
        plt.bar(x, victimas_masc, width=0.4, label='Hombres', align='center')
        plt.bar(x, victimas_fem, width=0.4, label='Mujeres', align='edge')
        
        plt.xlabel('Provincias')
        plt.ylabel('Cantidad de Víctimas')
        plt.title(f"Distribución de víctimas por género en el año {pAño}")
        plt.xticks(ticks=x, labels=provincias, rotation=90)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
    except pd.errors.ParserError as e:
        print(f"Error al leer el archivo CSV: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")   



        