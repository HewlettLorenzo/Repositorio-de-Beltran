import os
import pandas as pd
from funciones_csv import existe_modificado, CARPETA_ORIGINAL, CARPETA_MODIFICADA

def listar_archivos(directorio):
    """Devuelve una lista de archivos CSV en el directorio especificado."""
    if not os.path.exists(directorio):
        return []
    return sorted([f for f in os.listdir(directorio) if f.endswith(".csv")])

def mostrar_archivo(ruta):
    """Lee e imprime las primeras filas de un CSV."""
    try:
        df = pd.read_csv(ruta, header=None)
        print(f"\nArchivo mostrado: {os.path.basename(ruta)}")
        print(df.head(20))
        print(f"Filas: {len(df)} | Columnas: {len(df.columns)}\n")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def leer_csv():
    """Permite elegir entre leer archivos originales o modificados."""
    print("\n¿Qué tipo de archivos desea leer?")
    print("1. Archivos originales")
    print("2. Archivos modificados")

    opcion_tipo = input("Seleccione una opción (1-2): ").strip()

    if opcion_tipo == "1":
        directorio = CARPETA_ORIGINAL
        tipo = "originales"
    elif opcion_tipo == "2":
        directorio = CARPETA_MODIFICADA
        tipo = "modificados"
        if not os.path.exists(directorio) or not listar_archivos(directorio):
            print("\nNo existen archivos modificados actualmente.\n")
            return
    else:
        print("\nOpción inválida.\n")
        return

    archivos = listar_archivos(directorio)
    if not archivos:
        print(f"\nNo se encontraron archivos {tipo} en '{directorio}'.\n")
        return

    print(f"\nArchivos disponibles ({tipo}):")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")

    try:
        seleccion = int(input("Seleccione el número del archivo a leer: "))
        if 1 <= seleccion <= len(archivos):
            archivo_seleccionado = archivos[seleccion - 1]
            ruta = os.path.join(directorio, archivo_seleccionado)
            mostrar_archivo(ruta)
        else:
            print("\nNúmero fuera de rango.\n")
    except ValueError:
        print("\nEntrada inválida. Debe ingresar un número.\n")

def listar_originales():
    """Devuelve lista ordenada de CSV dentro de la carpeta original."""
    if not os.path.exists(CARPETA_ORIGINAL):
        return []
    archivos = [f for f in os.listdir(CARPETA_ORIGINAL) if f.endswith(".csv")]
    archivos.sort()
    return archivos

def listar_modificados():
    """Devuelve lista ordenada de nombres originales para los archivos modificados existentes."""
    if not os.path.exists(CARPETA_MODIFICADA):
        return []
    mods = []
    for f in os.listdir(CARPETA_MODIFICADA):
        if f.endswith("_modificado.csv"):
            base = f.rsplit("_modificado", 1)[0] + ".csv"
            mods.append(base)
    mods.sort()
    return mods

def mostrar_preview(df, nombre, max_rows=20):
    """Imprime un resumen (preview) del DataFrame recibido."""
    if df is None:
        print(f"No se pudo leer '{nombre}'.")
        return
    print(f"\nArchivo mostrado: {nombre}")
    print(df.head(max_rows))
    print(f"Filas: {len(df)} | Columnas: {len(df.columns)}\n")

def elegir_archivo(lista, prompt):
    """Muestra una lista numerada y devuelve el nombre seleccionado (o None)."""
    if not lista:
        print("Lista vacía.")
        return None
    for i, a in enumerate(lista, start=1):
        tag = " (modificado)" if existe_modificado(a) else ""
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

def preguntar_uso_modificado(nombre):
    """Si existe versión modificada, pregunta si usarla. Devuelve True/False."""
    if existe_modificado(nombre):
        r = input("Existe versión modificada. ¿Usar la versión modificada? (s/N): ").strip().lower()
        return r in ('s', 'si')
    return False

def comparar_csv(nombre):
    """
    Compara un CSV original con su versión modificada (_modificado.csv).
    Informa filas agregadas, eliminadas y modificadas con su contenido.
    Si no hay cambios reales, indica "No se modificaron filas" en lugar de un número.
    """
    import pandas as pd
    import os

    original_path = os.path.join(CARPETA_ORIGINAL, nombre)
    modificado_path = os.path.join(CARPETA_MODIFICADA, nombre.replace(".csv", "_modificado.csv"))

    if not os.path.exists(original_path):
        print(f"No existe el archivo original: {nombre}")
        return

    if not os.path.exists(modificado_path):
        print(f"No existe la versión modificada de '{nombre}'.")
        return

    try:
        df_original = pd.read_csv(original_path, header=None, dtype=str)
        df_modificado = pd.read_csv(modificado_path, header=None, dtype=str)
    except Exception as e:
        print(f"Error al leer los CSV: {e}")
        return

    id_col_orig = df_original.columns[0]
    id_col_mod = df_modificado.columns[0]

    df_original_idx = df_original.set_index(id_col_orig)
    df_modificado_idx = df_modificado.set_index(id_col_mod)

    ids_original = set(df_original_idx.index.astype(str))
    ids_modificado = set(df_modificado_idx.index.astype(str))

    nuevas = sorted(ids_modificado - ids_original, key=lambda x: str(x))
    eliminadas = sorted(ids_original - ids_modificado, key=lambda x: str(x))
    comunes = sorted(ids_original & ids_modificado, key=lambda x: str(x))

    modificadas = []
    for idx in comunes:
        fila_orig = df_original_idx.loc[idx]
        fila_mod = df_modificado_idx.loc[idx]

        def to_list(r):
            if hasattr(r, "to_list"):
                return [str(x).strip() for x in r.to_list()]
            return [str(r).strip()]

        if to_list(fila_orig) != to_list(fila_mod):
            modificadas.append(idx)

    filas_mod_text = str(len(modificadas)) if modificadas else "No se modificaron filas"

    print(f"\nComparando: {nombre}")
    print("-" * 70)
    print(f"Filas originales: {len(df_original)} | Filas modificadas: {filas_mod_text}")

    # FILAS MODIFICADAS
    if modificadas:
        print(f"\nFilas modificadas ({len(modificadas)}):")
        for idx in modificadas:
            orig = ", ".join(df_original_idx.loc[idx].to_list())
            mod = ", ".join(df_modificado_idx.loc[idx].to_list())
            print(f"  ID {idx}:")
            print(f"    Original → {orig}")
            print(f"    Modificado → {mod}")
    # FILAS AGREGADAS
    if nuevas:
        print(f"\nFilas agregadas ({len(nuevas)}):")
        for idx in nuevas:
            contenido = ", ".join(df_modificado_idx.loc[idx].to_list())
            print(f"  ID {idx}: {contenido}")

    # FILAS ELIMINADAS
    if eliminadas:
        print(f"\nFilas eliminadas ({len(eliminadas)}):")
        for idx in eliminadas:
            contenido = ", ".join(df_original_idx.loc[idx].to_list())
            print(f"  ID {idx}: {contenido}")

    print("-" * 70)