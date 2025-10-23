import os
import pandas as pd

CARPETA_ORIGINAL = "data_original"
CARPETA_MODIFICADA = "data_modificada"

def ruta_original(nombre_archivo):
    return os.path.join(CARPETA_ORIGINAL, nombre_archivo)

def ruta_modificada(nombre_archivo):
    base, ext = os.path.splitext(nombre_archivo)
    return os.path.join(CARPETA_MODIFICADA, f"{base}_modificado{ext}")

def existe_modificado(nombre_archivo):
    return os.path.exists(ruta_modificada(nombre_archivo))

def leer_csv(nombre_archivo, use_modificado=False, columnas=None):
    """
    Devuelve un DataFrame sin imprimir.
    Si use_modificado=True intentará leer el archivo modificado; si no existe, devuelve None.
    Si columnas se pasa, se usan como names al leer (header=None).
    """
    if use_modificado:
        ruta = ruta_modificada(nombre_archivo)
        if not os.path.exists(ruta):
            return None
    else:
        ruta = ruta_original(nombre_archivo)
        if not os.path.exists(ruta):
            return None

    # Leemos todo como string para evitar conversiones inesperadas
    if columnas:
        df = pd.read_csv(ruta, header=None, names=columnas, dtype=str)
    else:
        df = pd.read_csv(ruta, header=None, dtype=str)
    return df

def guardar_modificado(df, nombre_archivo):
    """
    Guarda df en data_modificada con sufijo _modificado.csv.
    Devuelve la ruta donde guardó.
    """
    if not os.path.exists(CARPETA_MODIFICADA):
        os.makedirs(CARPETA_MODIFICADA, exist_ok=True)
    ruta = ruta_modificada(nombre_archivo)
    df.to_csv(ruta, index=False, header=False)
    return ruta

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

def agregar_fila(nombre_archivo):
    ruta = os.path.join(CARPETA_ORIGINAL, nombre_archivo)
    df = pd.read_csv(ruta, header=None)

    # Generar ID automáticamente
    nueva_fila = [df.iloc[:,0].max() + 1 if not df.empty else 1]

    # Pedir valores para las demás columnas
    for i in range(1, len(df.columns)):
        valor = input(f"Ingrese valor para columna {i}: ")
        nueva_fila.append(valor)

    # Crear DataFrame de la nueva fila y concatenar
    nueva_fila_df = pd.DataFrame([nueva_fila], columns=df.columns)
    df_modificado = pd.concat([df, nueva_fila_df], ignore_index=True)

    # Guardar
    if not os.path.exists(CARPETA_MODIFICADA):
        os.makedirs(CARPETA_MODIFICADA)
    base, ext = os.path.splitext(nombre_archivo)
    df_modificado.to_csv(os.path.join(CARPETA_MODIFICADA, f"{base}_modificado{ext}"),
                         index=False, header=False)
    print(f"Fila agregada correctamente.")