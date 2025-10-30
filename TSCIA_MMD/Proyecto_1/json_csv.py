"""
Módulo para conversión entre formatos JSON y CSV
"""
import os
import pandas as pd
from herramientas import leer_archivo, guardar_archivo, ruta_database, obtener_formato_archivo

def convertir_csv_a_json(nombre_csv):
    """Convierte archivo CSV a JSON (reemplaza el original)"""
    df = leer_archivo(nombre_csv, 'csv')
    if df is None:
        print(f"No se pudo leer el CSV: {nombre_csv}")
        return False
    
    # Convertir DataFrame a lista de diccionarios
    datos_json = []
    for _, fila in df.iterrows():
        fila_dict = {f"columna_{i}": str(val) for i, val in enumerate(fila)}
        datos_json.append(fila_dict)
    
    # Eliminar el archivo CSV original de database
    ruta_csv = ruta_database(nombre_csv)
    if os.path.exists(ruta_csv):
        os.remove(ruta_csv)
    
    # Guardar como JSON con el mismo nombre base
    nombre_json = nombre_csv.replace('.csv', '.json')
    return guardar_archivo(datos_json, nombre_json, 'json')

def convertir_json_a_csv(nombre_json):
    """Convierte archivo JSON a CSV (reemplaza el original)"""
    datos = leer_archivo(nombre_json, 'json')
    if datos is None:
        print(f"No se pudo leer el JSON: {nombre_json}")
        return False
    
    # Convertir a DataFrame
    if isinstance(datos, list) and datos:
        claves = list(datos[0].keys())
        filas = []
        for item in datos:
            fila = [item.get(clave, '') for clave in claves]
            filas.append(fila)
        
        df = pd.DataFrame(filas)
        
        # Eliminar el archivo JSON original de database
        ruta_json = ruta_database(nombre_json)
        if os.path.exists(ruta_json):
            os.remove(ruta_json)
        
        # Guardar como CSV con el mismo nombre base
        nombre_csv = nombre_json.replace('.json', '.csv')
        return guardar_archivo(df, nombre_csv, 'csv')
    else:
        print("Formato JSON no soportado para conversión")
        return False

def menu_conversion():
    """
    Menú para conversión entre formatos JSON y CSV
    """
    from listado_csv import listar_database, elegir_archivo
    
    print("\n--- CONVERSIÓN DE FORMATOS ---")
    print("1. Convertir CSV a JSON")
    print("2. Convertir JSON a CSV")
    print("3. Volver al menú principal")
    
    opcion = input("Seleccione una opción (1-3): ").strip()
    
    if opcion == '1':
        # Buscar archivos CSV disponibles
        csv_database = listar_database()
        csv_database = [f for f in csv_database if f.endswith('.csv')]
        
        if not csv_database:
            print("No se encontraron archivos CSV en database para convertir.")
            return
        
        print("\nArchivos CSV disponibles en database:")
        archivo = elegir_archivo(csv_database, "Seleccione el archivo CSV a convertir a JSON: ")
        if not archivo:
            return
        
        if convertir_csv_a_json(archivo):
            print(f"✓ Conversión exitosa: {archivo} -> {archivo.replace('.csv', '.json')}")
            print("El archivo CSV original fue eliminado.")
        else:
            print("✗ Error en la conversión")
            
    elif opcion == '2':
        # Buscar archivos JSON disponibles
        json_database = listar_database()
        json_database = [f for f in json_database if f.endswith('.json')]
        
        if not json_database:
            print("No se encontraron archivos JSON en database para convertir.")
            return
        
        print("\nArchivos JSON disponibles en database:")
        archivo = elegir_archivo(json_database, "Seleccione el archivo JSON a convertir a CSV: ")
        if not archivo:
            return
        
        if convertir_json_a_csv(archivo):
            print(f"✓ Conversión exitosa: {archivo} -> {archivo.replace('.json', '.csv')}")
            print("El archivo JSON original fue eliminado.")
        else:
            print("✗ Error en la conversión")
            
    elif opcion == '3':
        return
    else:
        print("Opción inválida.")

# Funciones de conveniencia para uso externo
def csv_a_json(nombre_csv):
    """Convierte archivo CSV a JSON (alias de convertir_csv_a_json)"""
    return convertir_csv_a_json(nombre_csv)

def json_a_csv(nombre_json):
    """Convierte archivo JSON a CSV (alias de convertir_json_a_csv)"""
    return convertir_json_a_csv(nombre_json)