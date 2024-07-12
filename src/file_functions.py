import os
import csv
import json

def tomar_ruta_actual(archivo):
    ruta_actual = os.path.dirname(__file__)
    return os.path.join(ruta_actual, archivo)

def cargar_archivo_csv(archivo: str):
    """
    Carga datos de un archivo CSV.

    Args:
        archivo (str): Nombre del archivo CSV.

    Returns:
        list: Lista de diccionarios con los datos.
    """
    lista = []
    with open(tomar_ruta_actual(f"{archivo}.csv"), 'r', encoding='utf-8') as archivo_csv:
        encabezados = archivo_csv.readline().strip().split(',')

        for linea in archivo_csv:
            valores = linea.strip().split(',')
            fila = {}
            for i in range(len(encabezados)):
                fila[encabezados[i]] = valores[i]
            fila['nombre'] = fila['nombre']
            fila['puntaje'] = int(fila['puntaje'])
            lista.append(fila)
    return lista

def guardar_archivo_csv(archivo:str, lista:list):
    """
    Guarda los puntajes en un archivo CSV.

    Args:
        lista (list): Lista de diccionarios con los puntajes.
        archivo (str): Nombre del archivo CSV.
    """

    with open(tomar_ruta_actual(f"{archivo}.csv"), 'w', encoding='utf-8', newline='') as archivo_csv:
        campos = ['nombre', 'puntaje']
        archivo_csv.write(','.join(campos) + '\n')
        for item in lista:
            archivo_csv.write(f"{item['nombre']},{item['puntaje']}\n")
        
def guardar_archivo_json(lista:list, ruta:str):
    
    """
    Funcion que carga lista en archivo JSON

    Args:
        lista (list): Recibe la lista 
        ruta (str): Recibe nombre de la ruta sin la extension
    """
    with open(tomar_ruta_actual(f"{ruta}.json"), 'w', encoding='utf-8') as file:
        json.dump(lista, file, indent=4)
        
def cargar_archivo_json(ruta):
    """
    Carga los puntajes de un archivo JSON.
    
    Args:
        ruta (str): Nombre del archivo sin extensión.
        
    Returns:
        list: Lista de diccionarios con los puntajes.
    """
    try:
        with open(tomar_ruta_actual(f"{ruta}.json"), 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []