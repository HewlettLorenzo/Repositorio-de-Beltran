import os
import pandas as pd
import json
from herramientas import existe_en_database, CARPETA_DATABASE, CARPETA_HIST, leer_archivo, obtener_formato_archivo

def listar_archivos(directorio, formato=None):
    """Devuelve una lista de archivos en el directorio especificado, opcionalmente filtrados por formato"""
    if not os.path.exists(directorio):
        return []
    
    archivos = sorted([f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))])
    
    if formato:
        if formato == 'csv':
            archivos = [f for f in archivos if f.lower().endswith('.csv')]
        elif formato == 'json':
            archivos = [f for f in archivos if f.lower().endswith('.json')]
    
    return archivos

def mostrar_archivo(ruta, formato=None):
    """Lee e imprime las primeras filas/elementos de un archivo"""
    try:
        nombre_archivo = os.path.basename(ruta)
        if formato is None:
            formato = obtener_formato_archivo(nombre_archivo)
        
        if formato == 'csv':
            df = pd.read_csv(ruta, header=None)
            print(f"\nArchivo mostrado: {nombre_archivo}")
            print(df.head(20))
            print(f"Filas: {len(df)} | Columnas: {len(df.columns)}\n")
        elif formato == 'json':
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            print(f"\nArchivo mostrado: {nombre_archivo}")
            if isinstance(datos, list):
                for i, item in enumerate(datos[:20]):
                    print(f"{i}: {item}")
                print(f"Elementos: {len(datos)}")
            else:
                print(datos)
            print()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def levantar_archivos():
    """
    Función para levantar todos los CSV y JSON disponibles.
    Retorna: (bandera, conteo_csv, conteo_json)
    """
    print("\n¿Desea levantar todos los CSV y JSON disponibles?")
    respuesta = input("Ingrese 'si' para levantar todos los archivos, o 'no' para salir: ").strip().lower()
    
    if respuesta in ('si', 's', 'yes', 'y'):
        # Contar archivos en database e hist
        csv_database = listar_archivos(CARPETA_DATABASE, 'csv')
        json_database = listar_archivos(CARPETA_DATABASE, 'json')
        csv_hist = listar_archivos(CARPETA_HIST, 'csv')
        json_hist = listar_archivos(CARPETA_HIST, 'json')
        
        total_csv = len(csv_database) + len(csv_hist)
        total_json = len(json_database) + len(json_hist)
        
        print(f"\n✓ Se detectaron {total_csv} archivos CSV y {total_json} archivos JSON")
        print(f"  - Database: {len(csv_database)} CSV, {len(json_database)} JSON")
        print(f"  - Históricos: {len(csv_hist)} CSV, {len(json_hist)} JSON")
        
        return True, total_csv, total_json
    else:
        return False, 0, 0

def preguntar_formato_guardado(nombre_base):
    """
    Pregunta al usuario en qué formato desea guardar el archivo
    """
    print(f"\nArchivo: {nombre_base}")
    print("¿En qué formato desea guardar?")
    print("1. CSV")
    print("2. JSON")
    
    while True:
        opcion = input("Seleccione formato (1-2): ").strip()
        if opcion == '1':
            return f"{nombre_base}.csv"
        elif opcion == '2':
            return f"{nombre_base}.json"
        else:
            print("Opción inválida. Seleccione 1 para CSV o 2 para JSON.")

def leer_archivos():
    """Permite elegir entre leer archivos de database o históricos (solo lectura)"""
    print("\n¿Qué tipo de archivos desea leer?")
    print("1. Archivos de database (modificados)")
    print("2. Archivos históricos (originales) - SOLO LECTURA")
    
    opcion_tipo = input("Seleccione una opción (1-2): ").strip()

    if opcion_tipo == "1":
        directorio = CARPETA_DATABASE
        tipo = "database"
    elif opcion_tipo == "2":
        directorio = CARPETA_HIST
        tipo = "históricos (SOLO LECTURA)"
        if not os.path.exists(directorio) or not listar_archivos(directorio):
            print("\nNo existen archivos históricos actualmente.\n")
            return
    else:
        print("\nOpción inválida.\n")
        return

    # Preguntar formato
    print("\n¿Qué formato desea listar?")
    print("1. CSV")
    print("2. JSON")
    print("3. Ambos formatos")
    
    opcion_formato = input("Seleccione una opción (1-3): ").strip()
    
    if opcion_formato == "1":
        formato = 'csv'
        tipo_formato = "CSV"
    elif opcion_formato == "2":
        formato = 'json'
        tipo_formato = "JSON"
    elif opcion_formato == "3":
        formato = None
        tipo_formato = "CSV y JSON"
    else:
        print("\nOpción inválida.\n")
        return

    archivos = listar_archivos(directorio, formato)
    if not archivos:
        print(f"\nNo se encontraron archivos {tipo_formato} {tipo} en '{directorio}'.\n")
        return

    print(f"\nArchivos disponibles ({tipo_formato} {tipo}):")
    for i, archivo in enumerate(archivos, 1):
        if tipo == "históricos (SOLO LECTURA)":
            print(f"{i}. {archivo} (SOLO LECTURA)")
        else:
            print(f"{i}. {archivo}")

    try:
        seleccion = int(input("Seleccione el número del archivo a leer: "))
        if 1 <= seleccion <= len(archivos):
            archivo_seleccionado = archivos[seleccion - 1]
            ruta = os.path.join(directorio, archivo_seleccionado)
            formato_archivo = obtener_formato_archivo(archivo_seleccionado)
            mostrar_archivo(ruta, formato_archivo)
            
            # Si es histórico, mostrar mensaje de solo lectura
            if tipo == "históricos (SOLO LECTURA)":
                print("⚠ Este archivo es de solo lectura. Para modificarlo, use los archivos de database.")
        else:
            print("\nNúmero fuera de rango.\n")
    except ValueError:
        print("\nEntrada inválida. Debe ingresar un número.\n")

def listar_database():
    """Devuelve lista ordenada de archivos en database"""
    return listar_archivos(CARPETA_DATABASE)

def listar_historicos():
    """Devuelve lista ordenada de archivos en tablas_hist"""
    return listar_archivos(CARPETA_HIST)

def mostrar_preview(datos, nombre, max_rows=20):
    """Imprime un resumen (preview) del DataFrame o datos JSON recibidos"""
    if datos is None:
        print(f"No se pudo leer '{nombre}'.")
        return
    
    formato = obtener_formato_archivo(nombre)
    print(f"\nArchivo mostrado: {nombre}")
    
    if formato == 'csv' and isinstance(datos, pd.DataFrame):
        print(datos.head(max_rows))
        print(f"Filas: {len(datos)} | Columnas: {len(datos.columns)}\n")
    elif formato == 'json':
        if isinstance(datos, list):
            for i, item in enumerate(datos[:max_rows]):
                print(f"{i}: {item}")
            print(f"Elementos: {len(datos)}")
        else:
            print(datos)
        print()

def elegir_archivo(lista, prompt):
    """Muestra una lista numerada y devuelve el nombre seleccionado (o None)"""
    if not lista:
        print("Lista vacía.")
        return None
    
    for i, a in enumerate(lista, start=1):
        tag = " (en database)" if existe_en_database(a) else " (sólo histórico)"
        print(f"{i}. {a}{tag}")
    
    try:
        sel = int(input(prompt).strip()) - 1
        if sel < 0 or sel >= len(lista):
            print("Selección fuera de rango.")
            return None
        return lista[sel]
    except ValueError:
        print("Selección inválida.")
        return None

def preguntar_uso_database(nombre):
    """Si existe versión en database, pregunta si usarla. Devuelve True/False"""
    if existe_en_database(nombre):
        r = input("Existe versión en database. ¿Usar la versión de database? (s/N): ").strip().lower()
        return r in ('s', 'si')
    return False
