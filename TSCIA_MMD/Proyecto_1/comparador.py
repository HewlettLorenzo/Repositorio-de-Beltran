import os
import pandas as pd
import json
from herramientas import CARPETA_DATABASE, CARPETA_HIST, obtener_formato_archivo

def listar_archivos_comparables():
    """
    Devuelve lista de archivos que existen tanto en database como en histórico
    """
    if not os.path.exists(CARPETA_DATABASE) or not os.path.exists(CARPETA_HIST):
        return []
    
    archivos_database = [f for f in os.listdir(CARPETA_DATABASE) if os.path.isfile(os.path.join(CARPETA_DATABASE, f))]
    archivos_historicos = [f for f in os.listdir(CARPETA_HIST) if os.path.isfile(os.path.join(CARPETA_HIST, f))]
    
    comparables = []
    for archivo_db in archivos_database:
        # Buscar correspondiente en históricos
        for archivo_hist in archivos_historicos:
            base_db = archivo_db.replace('.csv', '').replace('.json', '')
            base_hist = archivo_hist.replace('_hist.csv', '').replace('_hist.json', '')
            
            if base_db == base_hist:
                comparables.append(archivo_db)
                break
    
    return sorted(comparables)

def mostrar_opciones_comparacion():
    """
    Muestra archivos disponibles para comparación
    """
    comparables = listar_archivos_comparables()
    
    if not comparables:
        print("No hay archivos para comparar (deben existir en database e histórico).")
        return None
    
    print("\nArchivos disponibles para comparación:")
    for i, archivo in enumerate(comparables, 1):
        print(f"{i}. {archivo}")
    
    try:
        seleccion = int(input("Seleccione el número del archivo a comparar: ")) - 1
        if 0 <= seleccion < len(comparables):
            return comparables[seleccion]
        else:
            print("Selección fuera de rango.")
            return None
    except ValueError:
        print("Selección inválida.")
        return None

def comparar_archivos(nombre_archivo):
    """
    Función principal de comparación
    """
    database_path = os.path.join(CARPETA_DATABASE, nombre_archivo)
    
    # Encontrar archivo histórico correspondiente
    archivos_hist = os.listdir(CARPETA_HIST)
    archivo_hist_correspondiente = None
    
    for archivo_hist in archivos_hist:
        base_nombre = nombre_archivo.replace('.csv', '').replace('.json', '')
        base_hist = archivo_hist.replace('_hist.csv', '').replace('_hist.json', '')
        
        if base_nombre == base_hist:
            archivo_hist_correspondiente = archivo_hist
            break
    
    if not archivo_hist_correspondiente:
        print(f"No se encontró la versión histórica correspondiente para '{nombre_archivo}'.")
        return

    hist_path = os.path.join(CARPETA_HIST, archivo_hist_correspondiente)

    if not os.path.exists(database_path):
        print(f"No existe el archivo en database: {nombre_archivo}")
        return

    if not os.path.exists(hist_path):
        print(f"No existe la versión histórica: {archivo_hist_correspondiente}")
        return

    formato = obtener_formato_archivo(nombre_archivo)
    
    try:
        if formato == 'csv':
            _comparar_csv(nombre_archivo, database_path, hist_path)
        elif formato == 'json':
            _comparar_json(nombre_archivo, database_path, hist_path)
    except Exception as e:
        print(f"Error al comparar los archivos: {e}")

def _comparar_csv(nombre_archivo, database_path, hist_path):
    """Compara archivos CSV"""
    df_database = pd.read_csv(database_path, header=None, dtype=str)
    df_hist = pd.read_csv(hist_path, header=None, dtype=str)

    id_col_db = df_database.columns[0]
    id_col_hist = df_hist.columns[0]

    df_database_idx = df_database.set_index(id_col_db)
    df_hist_idx = df_hist.set_index(id_col_hist)

    ids_database = set(df_database_idx.index.astype(str))
    ids_hist = set(df_hist_idx.index.astype(str))

    nuevas = sorted(ids_database - ids_hist, key=lambda x: str(x))
    eliminadas = sorted(ids_hist - ids_database, key=lambda x: str(x))
    comunes = sorted(ids_hist & ids_database, key=lambda x: str(x))

    modificadas = []
    for idx in comunes:
        fila_hist = df_hist_idx.loc[idx]
        fila_db = df_database_idx.loc[idx]

        def to_list(r):
            if hasattr(r, "to_list"):
                return [str(x).strip() for x in r.to_list()]
            return [str(r).strip()]

        if to_list(fila_hist) != to_list(fila_db):
            modificadas.append(idx)

    filas_mod_text = str(len(modificadas)) if modificadas else "No se modificaron filas"

    print(f"\nComparando: {nombre_archivo}")
    print("-" * 70)
    print(f"Filas históricas: {len(df_hist)} | Filas en database: {len(df_database)}")
    print(f"Cambios detectados: {filas_mod_text}")

    # FILAS MODIFICADAS
    if modificadas:
        print(f"\nFilas modificadas ({len(modificadas)}):")
        for idx in modificadas:
            hist = ", ".join(df_hist_idx.loc[idx].to_list())
            db = ", ".join(df_database_idx.loc[idx].to_list())
            print(f"  ID {idx}:")
            print(f"    Histórico → {hist}")
            print(f"    Database → {db}")

    # FILAS AGREGADAS
    if nuevas:
        print(f"\nFilas agregadas ({len(nuevas)}):")
        for idx in nuevas:
            contenido = ", ".join(df_database_idx.loc[idx].to_list())
            print(f"  ID {idx}: {contenido}")

    # FILAS ELIMINADAS
    if eliminadas:
        print(f"\nFilas eliminadas ({len(eliminadas)}):")
        for idx in eliminadas:
            contenido = ", ".join(df_hist_idx.loc[idx].to_list())
            print(f"  ID {idx}: {contenido}")

    print("-" * 70)

def _comparar_json(nombre_archivo, database_path, hist_path):
    """Compara archivos JSON"""
    with open(database_path, 'r', encoding='utf-8') as f:
        datos_db = json.load(f)
    with open(hist_path, 'r', encoding='utf-8') as f:
        datos_hist = json.load(f)

    if not isinstance(datos_db, list) or not isinstance(datos_hist, list):
        print("Solo se pueden comparar JSON con formato de lista")
        return

    # Buscar IDs en ambos archivos
    def obtener_ids(datos):
        ids = {}
        for i, item in enumerate(datos):
            if isinstance(item, dict):
                for key, val in item.items():
                    if 'id' in key.lower() or key == 'columna_0':
                        ids[str(val)] = i
                        break
        return ids

    ids_db = obtener_ids(datos_db)
    ids_hist = obtener_ids(datos_hist)

    nuevas = sorted(set(ids_db.keys()) - set(ids_hist.keys()))
    eliminadas = sorted(set(ids_hist.keys()) - set(ids_db.keys()))
    comunes = sorted(set(ids_hist.keys()) & set(ids_db.keys()))

    modificadas = []
    for idx in comunes:
        if datos_db[ids_db[idx]] != datos_hist[ids_hist[idx]]:
            modificadas.append(idx)

    elementos_mod_text = str(len(modificadas)) if modificadas else "No se modificaron elementos"

    print(f"\nComparando: {nombre_archivo}")
    print("-" * 70)
    print(f"Elementos históricos: {len(datos_hist)} | Elementos en database: {len(datos_db)}")
    print(f"Cambios detectados: {elementos_mod_text}")

    # ELEMENTOS MODIFICADOS
    if modificadas:
        print(f"\nElementos modificados ({len(modificadas)}):")
        for idx in modificadas:
            print(f"  ID {idx}:")
            print(f"    Histórico → {datos_hist[ids_hist[idx]]}")
            print(f"    Database → {datos_db[ids_db[idx]]}")

    # ELEMENTOS AGREGADOS
    if nuevas:
        print(f"\nElementos agregados ({len(nuevas)}):")
        for idx in nuevas:
            print(f"  ID {idx}: {datos_db[ids_db[idx]]}")

    # ELEMENTOS ELIMINADAS
    if eliminadas:
        print(f"\nElementos eliminados ({len(eliminadas)}):")
        for idx in eliminadas:
            print(f"  ID {idx}: {datos_hist[ids_hist[idx]]}")

    print("-" * 70)

def menu_comparacion():
    """
    Menú principal de comparación
    """
    archivo = mostrar_opciones_comparacion()
    if archivo:
        comparar_archivos(archivo)