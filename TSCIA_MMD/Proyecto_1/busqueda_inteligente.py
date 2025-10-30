import pandas as pd
import os
import unicodedata
from herramientas import CARPETA_DATABASE, CARPETA_HIST, leer_archivo
import json 

def normalizar_texto(texto):
    """
    Normaliza texto: quita acentos, convierte a minúsculas, elimina espacios extras Y COMILLAS
    """
    if pd.isna(texto):
        return ""
    
    texto = str(texto)
    # QUITAR COMILLAS primero
    texto = texto.strip('"\'')  # Elimina comillas dobles y simples al inicio/final
    # Quitar acentos y caracteres especiales
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    # Convertir a minúsculas y quitar espacios extras
    texto = texto.lower().strip()
    # Eliminar múltiples espacios
    texto = ' '.join(texto.split())
    return texto

def crear_diccionario_busqueda(tabla_referencia, columna_id=0, columna_nombre=1):
    """
    Crea un diccionario de búsqueda: texto_normalizado -> ID
    """
    diccionario = {}
    
    if isinstance(tabla_referencia, pd.DataFrame):
        # Es un DataFrame CSV
        print(f"🔍 Procesando DataFrame con {len(tabla_referencia)} filas")
        for idx, fila in tabla_referencia.iterrows():
            if len(fila) > max(columna_id, columna_nombre):
                id_valor = str(fila[columna_id])
                nombre_valor = str(fila[columna_nombre])
                
                # DEBUG: Mostrar lo que se está procesando
                print(f"   Fila {idx}: ID='{id_valor}', Nombre='{nombre_valor}'")
                
                texto_normalizado = normalizar_texto(nombre_valor)
                if texto_normalizado:
                    diccionario[texto_normalizado] = id_valor
                    print(f"   ✅ Agregado: '{texto_normalizado}' -> {id_valor}")
    else:
        # Es JSON
        print(f"🔍 Procesando JSON con {len(tabla_referencia)} elementos")
        for item in tabla_referencia:
            if isinstance(item, dict):
                # Buscar campos ID y nombre
                id_valor = None
                nombre_valor = None
                for key, value in item.items():
                    if 'id' in key.lower() or key == 'columna_0':
                        id_valor = str(value)
                    elif 'nombre' in key.lower() or 'descripcion' in key.lower() or key == 'columna_1':
                        nombre_valor = str(value)
                
                if id_valor and nombre_valor:
                    texto_normalizado = normalizar_texto(nombre_valor)
                    if texto_normalizado:
                        diccionario[texto_normalizado] = id_valor
                        print(f"   ✅ Agregado: '{texto_normalizado}' -> {id_valor}")
    
    print(f"📚 Diccionario final: {len(diccionario)} entradas")
    return diccionario

def cargar_tabla_referencia(nombre_tabla):
    """
    Carga una tabla de referencia (provincias, localidades, etc.) desde database o hist
    """
    # Primero intentar desde database
    datos = leer_archivo(nombre_tabla)
    if datos is not None:
        return datos
    
    # Si no existe en database, buscar en hist
    base, ext = os.path.splitext(nombre_tabla)
    nombre_hist = f"{base}_hist{ext}"
    ruta_hist = os.path.join(CARPETA_HIST, nombre_hist)
    
    if os.path.exists(ruta_hist):
        if nombre_tabla.endswith('.csv'):
            return pd.read_csv(ruta_hist, header=None, dtype=str)
        else:  # JSON
            with open(ruta_hist, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    return None

def buscar_id_por_nombre(nombre_tabla, texto_busqueda, columna_id=0, columna_nombre=1):
    """
    Busca un ID por nombre en una tabla de referencia
    """
    tabla = cargar_tabla_referencia(nombre_tabla)
    if tabla is None:
        return None
    
    diccionario = crear_diccionario_busqueda(tabla, columna_id, columna_nombre)
    texto_normalizado = normalizar_texto(texto_busqueda)
    
    # Búsqueda exacta
    if texto_normalizado in diccionario:
        return diccionario[texto_normalizado]
    
    # Búsqueda parcial
    for texto_ref, id_valor in diccionario.items():
        if texto_normalizado in texto_ref or texto_ref in texto_normalizado:
            return id_valor
    
    return None

def crear_diccionario_busqueda(tabla_referencia, columna_id=0, columna_nombre=1):
    """
    Crea un diccionario de búsqueda: texto_normalizado -> ID
    """
    diccionario = {}
    
    if isinstance(tabla_referencia, pd.DataFrame):
        # Es un DataFrame CSV
        for idx, fila in tabla_referencia.iterrows():
            if len(fila) > max(columna_id, columna_nombre):
                id_valor = str(fila[columna_id])
                nombre_valor = str(fila[columna_nombre])
                texto_normalizado = normalizar_texto(nombre_valor)
                if texto_normalizado:
                    diccionario[texto_normalizado] = id_valor
    else:
        # Es JSON
        for item in tabla_referencia:
            if isinstance(item, dict):
                # Buscar campos ID y nombre
                id_valor = None
                nombre_valor = None
                for key, value in item.items():
                    if 'id' in key.lower() or key == 'columna_0':
                        id_valor = str(value)
                    elif 'nombre' in key.lower() or 'descripcion' in key.lower() or key == 'columna_1':
                        nombre_valor = str(value)
                
                if id_valor and nombre_valor:
                    texto_normalizado = normalizar_texto(nombre_valor)
                    if texto_normalizado:
                        diccionario[texto_normalizado] = id_valor
    
    return diccionario

def mostrar_opciones_tabla(nombre_tabla, columna_nombre=1):
    """
    Muestra las opciones disponibles en una tabla de referencia
    """
    tabla = cargar_tabla_referencia(nombre_tabla)
    if tabla is None:
        print(f"No se encontró la tabla de referencia: {nombre_tabla}")
        return
    
    print(f"\nOpciones disponibles en {nombre_tabla}:")
    
    if isinstance(tabla, pd.DataFrame):
        for _, fila in tabla.iterrows():
            if len(fila) > columna_nombre:
                print(f"  - {fila[columna_nombre]}")
    else:
        for item in tabla:
            if isinstance(item, dict):
                for key, value in item.items():
                    if 'nombre' in key.lower() or 'descripcion' in key.lower() or key == 'columna_1':
                        print(f"  - {value}")
                        break

def input_con_busqueda_inteligente(prompt, nombre_tabla_referencia, columna_id=0, columna_nombre=1):
    """
    Input que permite búsqueda inteligente en tablas de referencia
    """
    # QUITAR EL DEBUG DE LA TABLA COMPLETA
    # Mostrar opciones disponibles (solo las primeras 10 para no saturar)
    print(f"\nOpciones disponibles en {nombre_tabla_referencia} (primeras 10):")
    tabla = cargar_tabla_referencia(nombre_tabla_referencia)
    if tabla is not None:
        if isinstance(tabla, pd.DataFrame):
            for i in range(min(10, len(tabla))):
                if len(tabla.iloc[i]) > columna_nombre:
                    print(f"  - {tabla.iloc[i][columna_nombre]}")
        else:
            for i, item in enumerate(tabla[:10]):
                if isinstance(item, dict):
                    for key, value in item.items():
                        if 'nombre' in key.lower() or 'descripcion' in key.lower() or key == 'columna_1':
                            print(f"  - {value}")
                            break
        if len(tabla) > 10:
            print(f"  ... y {len(tabla) - 10} más")
    
    while True:
        entrada = input(f"\n{prompt} (o 'lista' para ver todas las opciones): ").strip()
        
        if entrada.lower() == 'lista':
            mostrar_opciones_tabla(nombre_tabla_referencia, columna_nombre)
            continue
        
        # Buscar ID correspondiente
        id_encontrado = buscar_id_por_nombre(nombre_tabla_referencia, entrada, columna_id, columna_nombre)
        
        if id_encontrado:
            print(f"✓ Encontrado: '{entrada}' -> ID {id_encontrado}")
            return id_encontrado
        else:
            print("✗ No se encontró coincidencia. Intente nuevamente o ingrese el ID manualmente.")
            id_manual = input("O ingrese el ID manualmente (enter para reintentar): ").strip()
            if id_manual:
                return id_manual

# Mapeo de tablas hijas a sus tablas padre
RELACIONES_TABLAS = {
    "clientes.csv": {
        "columna_4": "localidades.csv"  # ← EXPLÍCITO: columna 4 usa localidades.csv
    },
    "proveedores.csv": {
        "columna_4": "localidades.csv"   # ← Misma lógica
    },
    "sucursales.csv": {
        "columna_3": "localidades.csv"   # ← Ajustar según la columna correcta
    },
    "productos.csv": {
        "rubro": "rubros.csv",
        "proveedor": "proveedores.csv"
    },
    "factura_enc.csv": {
        "cliente": "clientes.csv",
        "sucursal": "sucursales.csv"
    },
    "factura_det.csv": {
        "producto": "productos.csv"
    }
}

def obtener_relaciones_tabla(nombre_archivo):
    """Obtiene las relaciones para una tabla específica - VERSIÓN MEJORADA"""
    relaciones = RELACIONES_TABLAS.get(nombre_archivo, {})
    
    # Si no hay relaciones definidas, usar detección automática
    if not relaciones:
        return relaciones
    
    # Convertir nombres de columna a índices si es necesario
    relaciones_mejoradas = {}
    for col_key, tabla in relaciones.items():
        if col_key.startswith('columna_'):
            # Es un índice explícito: "columna_4" -> 4
            try:
                idx = int(col_key.split('_')[1])
                relaciones_mejoradas[idx] = tabla
            except:
                relaciones_mejoradas[col_key] = tabla
        else:
            relaciones_mejoradas[col_key] = tabla
    
    return relaciones_mejoradas