import os
import pandas as pd
import json

# Configuración de carpetas
CARPETA_DATABASE = "database"
CARPETA_HIST = "tablas_hist"

def ruta_database(nombre_archivo):
    return os.path.join(CARPETA_DATABASE, nombre_archivo)

def ruta_hist(nombre_archivo):
    base, ext = os.path.splitext(nombre_archivo)
    return os.path.join(CARPETA_HIST, f"{base}_hist{ext}")

def existe_en_database(nombre_archivo):
    return os.path.exists(ruta_database(nombre_archivo))

def obtener_formato_archivo(nombre_archivo):
    """Detecta si el archivo es CSV o JSON basado en extensión"""
    if nombre_archivo.lower().endswith('.json'):
        return 'json'
    elif nombre_archivo.lower().endswith('.csv'):
        return 'csv'
    return None

def leer_archivo(nombre_archivo, formato=None):
    """
    Lee archivo desde database. Si no existe, busca en tablas_hist.
    Devuelve DataFrame para CSV, dict para JSON, o None si error.
    """
    if formato is None:
        formato = obtener_formato_archivo(nombre_archivo)
    
    # Primero buscar en database
    ruta = ruta_database(nombre_archivo)
    if not os.path.exists(ruta):
        # Si no existe en database, buscar en hist
        ruta = ruta_hist(nombre_archivo)
        if not os.path.exists(ruta):
            return None
    
    try:
        if formato == 'csv':
            # LEER CSV CON COMILLAS - agregar quoting
            df = pd.read_csv(ruta, header=None, dtype=str, quoting=1)  # quoting=1 para QUOTE_ALL
            # Limpiar comillas de todas las celdas
            df = df.map(lambda x: str(x).strip('"\'') if pd.notna(x) else x)
            return df
        elif formato == 'json':
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return None
    except Exception as e:
        print(f"Error leyendo archivo {nombre_archivo}: {e}")
        return None

def guardar_archivo(datos, nombre_archivo, formato=None):
    """
    Guarda datos en database. Solo crea histórico la primera vez que se modifica.
    """
    if formato is None:
        formato = obtener_formato_archivo(nombre_archivo)
    
    # Crear carpetas si no existen
    if not os.path.exists(CARPETA_DATABASE):
        os.makedirs(CARPETA_DATABASE, exist_ok=True)
    if not os.path.exists(CARPETA_HIST):
        os.makedirs(CARPETA_HIST, exist_ok=True)
    
    ruta_actual = ruta_database(nombre_archivo)
    ruta_hist_archivo = ruta_hist(nombre_archivo)
    
    # Lógica de versionado:
    # - Si existe en database pero NO en hist → mover a hist (primera modificación)
    # - Si existe en database Y en hist → solo sobreescribir database (modificaciones posteriores)
    # - Si no existe en database → guardar directamente
    
    if os.path.exists(ruta_actual):
        if not os.path.exists(ruta_hist_archivo):
            # Primera modificación: crear histórico
            os.rename(ruta_actual, ruta_hist_archivo)
            print(f"✓ Versión histórica creada: {ruta_hist_archivo}")
        else:
            # Modificación posterior: solo actualizar database
            print(f"✓ Actualizando versión en database")
    else:
        print(f"✓ Creando nuevo archivo en database")
    
    # Guardar nuevo archivo en database
    try:
        if formato == 'csv':
            datos.to_csv(ruta_actual, index=False, header=False)
        elif formato == 'json':
            with open(ruta_actual, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Archivo guardado en: {ruta_actual}")
        return ruta_actual
    except Exception as e:
        print(f"✗ Error guardando archivo {nombre_archivo}: {e}")
        return None

def obtener_nuevo_id(df):
    """Devuelve el próximo ID autoincremental basado en la primera columna (0)"""
    if df.empty:
        return 1
    try:
        ids = pd.to_numeric(df.iloc[:,0], errors='coerce')
        max_id = ids.max()
        return int(max_id) + 1 if not pd.isna(max_id) else 1
    except:
        return 1

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
    
    # Eliminar el archivo CSV original
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
        # Asumir que todos los dict tienen las mismas claves
        claves = list(datos[0].keys())
        filas = []
        for item in datos:
            fila = [item.get(clave, '') for clave in claves]
            filas.append(fila)
        
        df = pd.DataFrame(filas)
        
        # Eliminar el archivo JSON original
        ruta_json = ruta_database(nombre_json)
        if os.path.exists(ruta_json):
            os.remove(ruta_json)
        
        # Guardar como CSV con el mismo nombre base
        nombre_csv = nombre_json.replace('.json', '.csv')
        return guardar_archivo(df, nombre_csv, 'csv')
    else:
        print("Formato JSON no soportado para conversión")
        return False

# --- OPERACIONES CRUD ---
def agregar_fila(nombre_archivo):
    """
    Agrega una fila. Trabaja sobre archivo en database.
    Pregunta formato si es necesario.
    """
    formato = obtener_formato_archivo(nombre_archivo)
    
    if formato == 'csv':
        _agregar_fila_csv(nombre_archivo)
    elif formato == 'json':
        _agregar_fila_json(nombre_archivo)
    else:
        print("Formato no soportado")

def guardar_archivo_con_formato(datos, nombre_base):
    """
    Guarda datos preguntando el formato deseado
    """
    from listado_csv import preguntar_formato_guardado
    
    nombre_archivo = preguntar_formato_guardado(nombre_base)
    formato = obtener_formato_archivo(nombre_archivo)
    
    return guardar_archivo(datos, nombre_archivo, formato)

from busqueda_inteligente import input_con_busqueda_inteligente, RELACIONES_TABLAS
def obtener_relaciones_tabla(nombre_archivo):
    """Obtiene las relaciones para una tabla específica"""
    return RELACIONES_TABLAS.get(nombre_archivo, {})

def _agregar_fila_csv(nombre_archivo):
    df = leer_archivo(nombre_archivo, 'csv')
    if df is None:
        print(f"No se pudo leer el archivo: {nombre_archivo}")
        return
    
    nuevo_id = obtener_nuevo_id(df)
    print(f"Agregando nueva fila a '{nombre_archivo}' (ID -> {nuevo_id})")
    
    from busqueda_inteligente import obtener_relaciones_tabla
    relaciones = obtener_relaciones_tabla(nombre_archivo)
    
    nueva_fila = [str(nuevo_id)]
    
    for i in range(1, len(df.columns)):
        tabla_relacionada = relaciones.get(i)
        
        if tabla_relacionada:
            valor = input_con_busqueda_inteligente(
                f"Ingrese valor para columna {i}: ", 
                tabla_relacionada,
                columna_id=0,
                columna_nombre=1
            )
        else:
            valor = input(f"Ingrese valor para columna {i}: ").strip()
        
        nueva_fila.append(valor)
    
    # QUITAR EL PRINT DE LA FILA COMPLETA
    # Guardar
    nueva_fila_df = pd.DataFrame([nueva_fila], columns=df.columns)
    df_modificado = pd.concat([df, nueva_fila_df], ignore_index=True)
    
    nombre_base = nombre_archivo.replace('.csv', '').replace('.json', '')
    guardar_archivo_con_formato(df_modificado, nombre_base)

def _agregar_fila_json(nombre_archivo):
    """Agrega elemento a archivo JSON"""
    datos = leer_archivo(nombre_archivo, 'json')
    if datos is None or not isinstance(datos, list):
        print(f"No se pudo leer el archivo JSON: {nombre_archivo}")
        return
    
    # Calcular nuevo ID
    ids = []
    for item in datos:
        if isinstance(item, dict):
            # Buscar campo ID (primera clave que contenga 'id' o columna_0)
            for key, val in item.items():
                if 'id' in key.lower() or key == 'columna_0':
                    try:
                        ids.append(int(val))
                    except:
                        pass
                    break
    
    nuevo_id = max(ids) + 1 if ids else 1
    print(f"Agregando nuevo elemento a '{nombre_archivo}' (ID -> {nuevo_id})")
    
    # Construir nuevo elemento
    nuevo_elemento = {}
    if datos:  # Usar primer elemento como plantilla
        primer_elemento = datos[0]
        for key in primer_elemento.keys():
            if 'id' in key.lower() or key == 'columna_0':
                nuevo_elemento[key] = str(nuevo_id)
            else:
                val = input(f"Ingrese valor para '{key}': ").strip()
                nuevo_elemento[key] = val
    
    datos.append(nuevo_elemento)
    
    # Guardar preguntando formato
    nombre_base = nombre_archivo.replace('.csv', '').replace('.json', '')
    guardar_archivo_con_formato(datos, nombre_base)

def eliminar_fila(nombre_archivo):
    """
    Elimina fila/elemento. Solo funciona si existe en database.
    """
    if not existe_en_database(nombre_archivo):
        print("No existe archivo en database. No se puede eliminar.")
        return
    
    formato = obtener_formato_archivo(nombre_archivo)
    
    if formato == 'csv':
        _eliminar_fila_csv(nombre_archivo)
    elif formato == 'json':
        _eliminar_fila_json(nombre_archivo)

def _eliminar_fila_csv(nombre_archivo):
    """Elimina fila de CSV"""
    df = leer_archivo(nombre_archivo, 'csv')
    if df is None:
        print("Error leyendo archivo.")
        return
    
    print("Vista previa (primeras 20 filas):")
    print(df.head(20))
    
    try:
        idx = int(input("Ingrese el índice de la fila a eliminar: ").strip())
    except ValueError:
        print("Índice inválido.")
        return
    
    if idx < 0 or idx >= len(df):
        print("Índice fuera de rango.")
        return
    
    df = df.drop(idx).reset_index(drop=True)
    guardar_archivo(df, nombre_archivo, 'csv')  # ← Usa la función corregida
    print(f"Fila {idx} eliminada.")

def _eliminar_fila_csv(nombre_archivo):
    """Elimina fila de CSV"""
    df = leer_archivo(nombre_archivo, 'csv')
    if df is None:
        print("Error leyendo archivo.")
        return
    
    print("Vista previa (primeras 20 filas):")
    print(df.head(20))
    
    try:
        idx = int(input("Ingrese el índice de la fila a eliminar: ").strip())
    except ValueError:
        print("Índice inválido.")
        return
    
    if idx < 0 or idx >= len(df):
        print("Índice fuera de rango.")
        return
    
    df = df.drop(idx).reset_index(drop=True)
    guardar_archivo(df, nombre_archivo, 'csv')
    print(f"Fila {idx} eliminada.")

def _eliminar_fila_json(nombre_archivo):
    """Elimina elemento de JSON"""
    datos = leer_archivo(nombre_archivo, 'json')
    if datos is None or not isinstance(datos, list):
        print("Error leyendo archivo.")
        return
    
    print("Vista previa (primeros 20 elementos):")
    for i, item in enumerate(datos[:20]):
        print(f"{i}: {item}")
    
    try:
        idx = int(input("Ingrese el índice del elemento a eliminar: ").strip())
    except ValueError:
        print("Índice inválido.")
        return
    
    if idx < 0 or idx >= len(datos):
        print("Índice fuera de rango.")
        return
    
    elemento_eliminado = datos.pop(idx)
    guardar_archivo(datos, nombre_archivo, 'json')
    print(f"Elemento {idx} eliminado: {elemento_eliminado}")

def modificar_fila(nombre_archivo):
    """
    Modifica fila/elemento. Trabaja sobre archivo en database.
    """
    formato = obtener_formato_archivo(nombre_archivo)
    
    if formato == 'csv':
        _modificar_fila_csv(nombre_archivo)
    elif formato == 'json':
        _modificar_fila_json(nombre_archivo)
    else:
        print("Formato no soportado")

def _modificar_fila_csv(nombre_archivo):
    """Modifica fila en CSV con búsqueda inteligente"""
    df = leer_archivo(nombre_archivo, 'csv')
    if df is None:
        print("No se puede leer el archivo.")
        return
    
    print("Vista previa (primeras 20 filas):")
    print(df.head(20))
    
    try:
        idx = int(input("Ingrese el índice de la fila a modificar: ").strip())
    except ValueError:
        print("Índice inválido.")
        return
    
    if idx < 0 or idx >= len(df):
        print("Índice fuera de rango.")
        return
    
    # Obtener relaciones de esta tabla
    relaciones = obtener_relaciones_tabla(nombre_archivo)
    
    for col in df.columns:
        if str(col).strip() == '0':  # Columna ID (primera)
            continue
        
        actual = df.at[idx, col]
        
        # Verificar si esta columna tiene una relación
        tabla_relacionada = None
        for clave, tabla in relaciones.items():
            if clave in str(col).lower() or f"id_{clave}" in str(col).lower():
                tabla_relacionada = tabla
                break
        
        if tabla_relacionada:
            print(f"\nColumna: {col} (actual: {actual})")
            nuevo = input_con_busqueda_inteligente(
                f"Nuevo valor para {clave} (enter = conservar): ",
                tabla_relacionada,
                columna_id=0,
                columna_nombre=1
            )
        else:
            nuevo = input(f"{col} (actual: {actual}) -> Nuevo (enter = conservar): ").strip()
        
        if nuevo != "":
            df.at[idx, col] = nuevo
    
    guardar_archivo(df, nombre_archivo, 'csv')  # ← Usa la función corregida
    print(f"Fila {idx} modificada.")

def _modificar_fila_csv(nombre_archivo):
    """Modifica fila en CSV"""
    df = leer_archivo(nombre_archivo, 'csv')
    if df is None:
        print("No se puede leer el archivo.")
        return
    
    print("Vista previa (primeras 20 filas):")
    print(df.head(20))
    
    try:
        idx = int(input("Ingrese el índice de la fila a modificar: ").strip())
    except ValueError:
        print("Índice inválido.")
        return
    
    if idx < 0 or idx >= len(df):
        print("Índice fuera de rango.")
        return
    
    for col in df.columns:
        if str(col).strip() == '0':  # Columna ID (primera)
            continue
        actual = df.at[idx, col]
        nuevo = input(f"Columna {col} (actual: {actual}) -> Nuevo (enter = conservar): ").strip()
        if nuevo != "":
            df.at[idx, col] = nuevo
    
    guardar_archivo(df, nombre_archivo, 'csv')
    print(f"Fila {idx} modificada.")

def _modificar_fila_json(nombre_archivo):
    """Modifica elemento en JSON"""
    datos = leer_archivo(nombre_archivo, 'json')
    if datos is None or not isinstance(datos, list):
        print("No se puede leer el archivo.")
        return
    
    print("Vista previa (primeros 20 elementos):")
    for i, item in enumerate(datos[:20]):
        print(f"{i}: {item}")
    
    try:
        idx = int(input("Ingrese el índice del elemento a modificar: ").strip())
    except ValueError:
        print("Índice inválido.")
        return
    
    if idx < 0 or idx >= len(datos):
        print("Índice fuera de rango.")
        return
    
    elemento = datos[idx]
    for key in elemento.keys():
        if 'id' in key.lower():  # No modificar IDs
            continue
        actual = elemento[key]
        nuevo = input(f"{key} (actual: {actual}) -> Nuevo (enter = conservar): ").strip()
        if nuevo != "":
            elemento[key] = nuevo
    
    guardar_archivo(datos, nombre_archivo, 'json')
    print(f"Elemento {idx} modificado.")

def buscar_fila(nombre_archivo):
    """
    Busca en el archivo. Soporta CSV y JSON.
    """
    formato = obtener_formato_archivo(nombre_archivo)
    
    if formato == 'csv':
        _buscar_fila_csv(nombre_archivo)
    elif formato == 'json':
        _buscar_fila_json(nombre_archivo)

def _buscar_fila_csv(nombre_archivo):
    """Busca en archivo CSV"""
    df = leer_archivo(nombre_archivo, 'csv')
    if df is None:
        print("No se pudo leer el archivo para buscar.")
        return
    
    print("Opciones de búsqueda:")
    print("1 - Buscar por ID (primera columna)")
    print("2 - Buscar por columna índice")
    print("3 - Búsqueda de texto en cualquier campo")
    opc = input("Seleccione opción (1/2/3): ").strip()
    
    if opc == '1':
        valor = input("Ingrese el ID a buscar (coincidencia exacta): ").strip()
        resultado = df[df.iloc[:, 0].astype(str) == valor]
        if resultado.empty:
            print("No se encontraron filas con ese ID.")
        else:
            print(resultado)
    
    elif opc == '2':
        col_idx_raw = input("Ingrese el índice de columna (ej: 0, 1, 2): ").strip()
        if not col_idx_raw.isdigit():
            print("Índice inválido.")
            return
        col_idx = int(col_idx_raw)
        if col_idx not in df.columns:
            print("Columna no válida.")
            return
        texto = input("Ingrese texto/valor a buscar (coincidencia parcial): ").strip()
        resultado = df[df[col_idx].astype(str).str.contains(texto, case=False, na=False)]
        if resultado.empty:
            print("No se encontraron coincidencias.")
        else:
            print(resultado)
    
    elif opc == '3':
        texto = input("Ingrese texto a buscar en todo el registro: ").strip()
        resultado = df[df.apply(lambda row: row.astype(str).str.contains(texto, case=False, na=False).any(), axis=1)]
        if resultado.empty:
            print("No se encontraron coincidencias.")
        else:
            print(resultado)
    
    else:
        print("Opción inválida.")

def _buscar_fila_json(nombre_archivo):
    """Busca en archivo JSON"""
    datos = leer_archivo(nombre_archivo, 'json')
    if datos is None or not isinstance(datos, list):
        print("No se pudo leer el archivo para buscar.")
        return
    
    print("Opciones de búsqueda:")
    print("1 - Buscar por ID")
    print("2 - Búsqueda de texto en cualquier campo")
    opc = input("Seleccione opción (1/2): ").strip()
    
    if opc == '1':
        valor = input("Ingrese el ID a buscar: ").strip()
        resultados = [item for item in datos if any(str(v) == valor for k, v in item.items() if 'id' in k.lower())]
        if not resultados:
            print("No se encontraron elementos con ese ID.")
        else:
            for resultado in resultados:
                print(resultado)
    
    elif opc == '2':
        texto = input("Ingrese texto a buscar: ").strip().lower()
        resultados = []
        for item in datos:
            if any(texto in str(v).lower() for v in item.values()):
                resultados.append(item)
        
        if not resultados:
            print("No se encontraron coincidencias.")
        else:
            for resultado in resultados:
                print(resultado)
    
    else:
        print("Opción inválida.")

def debug_agregar_fila(nombre_archivo):
    """Función temporal para debuggear"""
    df = leer_archivo(nombre_archivo, 'csv')
    if df is None:
        print(f"No se pudo leer el archivo: {nombre_archivo}")
        return
    
    print(f"DEBUG - ANALIZANDO {nombre_archivo}")
    print(f"DataFrame shape: {df.shape}")
    print(f"Columnas: {list(df.columns)}")
    print("Primeras 3 filas:")
    print(df.head(3))
    
    # Ver relaciones
    from busqueda_inteligente import RELACIONES_TABLAS, obtener_relaciones_tabla
    relaciones = obtener_relaciones_tabla(nombre_archivo)
    print(f"Relaciones encontradas: {relaciones}")
    
    # Mostrar qué columnas coinciden con las relaciones
    for i, col in enumerate(df.columns):
        print(f"Columna {i}: '{col}'")
        for clave, tabla in relaciones.items():
            if str(clave) in str(col).lower() or f"id_{clave}" in str(col).lower():
                print(f"COINCIDE con relación: {clave} -> {tabla}")
            else:
                print(f"NO coincide con: {clave}")

def guardar_archivo_con_formato(datos, nombre_base):
    """
    Guarda datos preguntando el formato deseado
    """
    from listado_csv import preguntar_formato_guardado
    
    nombre_archivo = preguntar_formato_guardado(nombre_base)
    formato = obtener_formato_archivo(nombre_archivo)
    
    return guardar_archivo(datos, nombre_archivo, formato)  # ← Usa la función corregida