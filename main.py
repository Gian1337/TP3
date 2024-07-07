import os
from Lib import Core
import os
import pandas as pd
import matplotlib.pyplot as mp

def main():
    os.system('cls')
    print('BIENVENIDO!')
    print('¿Que datos desea observar?')
    print('1- Número de VÍCTIMAS por provincia en período [2000-2022]')
    print('2- Distribución de DELITOS por TIPO en ROSARIO según AÑO')
    print('3- Distribución de VÍCTIMAS según el SEXO y AÑO')
    print('4- Tasa de VÍCTIMAS en Rosario según período ingresado')
    print()
    opcion = int(input("Ingrese su opción: "))
    if opcion == 1:
        provincia = input("Ingrese una Provincia o escriba 'listar' para ver todas las provincias disponibles: ")
        if provincia.lower() == "listar":
            Core.mostrarVictimasAnuales()
        else:
            Core.mostrarVictimasAnuales(provincia)
        
    elif opcion == 2:
        año = int(input("Ingrese un año (YYYY) para ver los delitos en Rosario: "))
        Core.mostrarTiposDelitosRosario(año)
    if opcion == 3:
        año = int(input("Ingrese un año (YYYY) para ver los delitos en hombres y mujeres: "))
        Core.mostrarDelitosPorSexo(año)

if __name__ == '__main__':
    main()