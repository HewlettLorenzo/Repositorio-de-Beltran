import pandas as pd
from funciones_csv import leer_csv, guardar_modificado, ruta_modificada, ruta_original, existe_modificado

def agregar_fila(nombre_archivo, columnas=None):
    """
    Agrega una fila: trabaja sobre archivo modificado si existe, sino sobre el original.
    Calcula ID como max(ID)+1 usando la columna detectada (col 0 o columna llamada 'ID').
    """
    # intentar leer modificado, si no existe leer original
    df = leer_csv(nombre_archivo, use_modificado=True) if existe_modificado(nombre_archivo) else leer_csv(nombre_archivo, use_modificado=False)
    if df is None:
        print(f"No existe el archivo original ni modificado para '{nombre_archivo}'.")
        return

    # determinar columna ID: por nombre 'ID' (ignorando case) o por posición 0
    id_col = None
    for c in df.columns:
        if str(c).strip().lower() == 'id':
            id_col = c
            break
    if id_col is None:
        id_col = df.columns[0]

    # calcular nuevo ID (max + 1), manejando strings
    try:
        ids = pd.to_numeric(df[id_col], errors='coerce')
        max_id = ids.max()
        nuevo_id = int(max_id) + 1 if not pd.isna(max_id) else 1
    except Exception:
        nuevo_id = 1

    print(f"Agregando nueva fila a '{nombre_archivo}' (ID -> {nuevo_id})")

    # construir nueva fila en el orden de df.columns
    nueva_fila = []
    for col in df.columns:
        if col == id_col:
            nueva_fila.append(str(nuevo_id))
        else:
            val = input(f"Ingrese valor para columna '{col}': ").strip()
            nueva_fila.append(val)

    # concatenar de forma segura
    df_nueva = pd.DataFrame([nueva_fila], columns=df.columns)
    df_modificado = pd.concat([df, df_nueva], ignore_index=True)

    ruta = guardar_modificado(df_modificado, nombre_archivo)
    print(f"Guardado en: {ruta}")

def eliminar_fila(nombre_archivo, columnas=None):
    """
    Elimina fila del archivo modificado. Si no existe modificado, avisa y no hace nada.
    Muestra el DataFrame modificado (preview) antes de pedir índice.
    """
    if not existe_modificado(nombre_archivo):
        print("No existe archivo modificado. No se puede eliminar. (Cree o agregue primero)")
        return

    df = leer_csv(nombre_archivo, use_modificado=True)
    if df is None:
        print("Error leyendo archivo modificado.")
        return

    # Mostrar preview (solo aquí, para eliminar)
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
    ruta = guardar_modificado(df, nombre_archivo)
    print(f"Fila {idx} eliminada. Guardado en: {ruta}")

def modificar_fila(nombre_archivo, columnas=None):
    """
    Modifica fila. Trabaja sobre modificado si existe, si no sobre original y guarda como modificado.
    """
    df = leer_csv(nombre_archivo, use_modificado=True) if existe_modificado(nombre_archivo) else leer_csv(nombre_archivo, use_modificado=False)
    if df is None:
        print("No se puede leer el archivo.")
        return

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
        if str(col).strip().lower() == 'id':
            continue
        actual = df.at[idx, col]
        nuevo = input(f"{col} (actual: {actual}) -> Nuevo (enter = conservar): ").strip()
        if nuevo != "":
            df.at[idx, col] = nuevo

    ruta = guardar_modificado(df, nombre_archivo)
    print(f"Fila {idx} modificada. Guardado en: {ruta}")

def buscar_fila(nombre_archivo, use_modificado=False):
    """
    Buscar en el archivo. Si use_modificado=True fuerza lectura del modificado (si existe).
    Soporta:
      - búsqueda por ID (primera columna): te pide el valor de ID y devuelve filas coincidentes.
      - búsqueda por columna índice: pide el índice de columna y el texto/valor a buscar.
      - búsqueda general (texto): busca en cualquier columna que contenga el texto.
    """
    # leer DF adecuado
    df = leer_csv(nombre_archivo, use_modificado=use_modificado)
    if df is None:
        print("No se pudo leer el archivo para buscar.")
        return

    # Pedir tipo de búsqueda
    print("Opciones de búsqueda:")
    print("1 - Buscar por ID (primera columna)")
    print("2 - Buscar por columna índice")
    print("3 - Búsqueda de texto en cualquier campo")
    opc = input("Seleccione opción (1/2/3): ").strip()

    if opc == '1':
        valor = input("Ingrese el ID a buscar (coincidencia exacta): ").strip()
        # coincidencia exacta en la primera columna
        resultado = df[df.iloc[:, 0].astype(str) == valor]
        if resultado.empty:
            print("No se encontraron filas con ese ID.")
        else:
            print(resultado)
        return

    if opc == '2':
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
        return

    if opc == '3':
        texto = input("Ingrese texto a buscar en todo el registro: ").strip()
        resultado = df[df.apply(lambda row: row.astype(str).str.contains(texto, case=False, na=False).any(), axis=1)]
        if resultado.empty:
            print("No se encontraron coincidencias.")
        else:
            print(resultado)
        return

    print("Opción inválida.")