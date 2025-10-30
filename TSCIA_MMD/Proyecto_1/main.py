from herramientas import leer_archivo, agregar_fila, eliminar_fila, modificar_fila, buscar_fila
from listado_csv import (levantar_archivos, leer_archivos, listar_database, listar_historicos, 
                         mostrar_preview, elegir_archivo, preguntar_uso_database)  # ← QUITAR 'comparar_archivos' de aquí
from json_csv import menu_conversion
from busqueda_inteligente import RELACIONES_TABLAS
from comparador import menu_comparacion  # ← AGREGAR ESTE NUEVO IMPORT

def menu():
    # Bandera para controlar si se levantaron todos los archivos
    archivos_levantados = False
    conteo_csv = 0
    conteo_json = 0
    
    # Al iniciar el programa, preguntar inmediatamente si desea levantar archivos
    print("=" * 70)
    print("SISTEMA DE GESTIÓN DE ARCHIVOS")
    print("=" * 70)
    
    archivos_levantados, conteo_csv, conteo_json = levantar_archivos()
    
    # Si no se levantaron archivos, salir del programa
    if not archivos_levantados:
        print("Saliendo del programa...")
        return
    
    # Mostrar información sobre las relaciones disponibles
    # MOVER ESTO DENTRO DEL WHILE LOOP para evitar el error
    # if RELACIONES_TABLAS:
    #     print(f"\nℹ Sistema de búsqueda inteligente activo para {len(RELACIONES_TABLAS)} tablas")
    #     print("  Puede ingresar nombres en lugar de IDs (ej: 'Buenos Aires' en lugar de '1')")
    
    while True:
        print("-" * 70)
        print("MENÚ PRINCIPAL")
        print("-" * 70)
        
        # Mostrar estado de archivos levantados
        print(f"✓ Archivos detectados: {conteo_csv} CSV, {conteo_json} JSON")
        
        # Mostrar información sobre búsqueda inteligente (AHORA SÍ DENTRO DEL LOOP)
        if RELACIONES_TABLAS:
            print(f"ℹ Búsqueda inteligente activa para {len(RELACIONES_TABLAS)} tablas")
            print("  Escriba nombres en lugar de IDs (ej: 'tandil' en lugar de '4')")
        print()
        
        print("1. Leer archivos")
        print("2. Agregar fila/elemento")
        print("3. Eliminar fila/elemento")
        print("4. Modificar fila/elemento")
        print("5. Buscar datos")
        print("6. Comparar archivo Database vs Histórico")
        print("7. Conversión entre formatos (JSON/CSV)")
        print("8. Salir")
        print("-" * 70)

        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '8':
            print("¡Hasta luego!")
            break

        # Opción 1: Leer archivos
        if opcion == '1':
            leer_archivos()
            continue

        # Para las demás opciones, solo trabajar con archivos de database
        archivos_database = listar_database()

        if not archivos_database:
            print("No hay archivos en database. Use las opciones de agregar/modificar para crear archivos.")
            continue

        # Opción 2: Agregar fila/elemento
        if opcion == '2':
            archivo = elegir_archivo(archivos_database, 
                                "Seleccione el número del archivo para agregar: ")
            if not archivo:
                continue
                
            datos = leer_archivo(archivo)
            mostrar_preview(datos, archivo)
            
            # Mostrar información sobre búsqueda inteligente si aplica
            if archivo in RELACIONES_TABLAS:  # ← ESTE "if" ESTABA MAL INDENTADO
                relaciones = RELACIONES_TABLAS[archivo]
                print("ℹ Búsqueda inteligente activa para:")
                for campo, tabla in relaciones.items():
                    print(f"   - {tabla.replace('.csv', '')} (columna {campo})")
                print("   Escriba nombres en lugar de IDs")
                print("   Escriba 'lista' para ver todas las opciones")
                print("-" * 50)
            
            agregar_fila(archivo)  # ← ESTA LÍNEA DEBE ESTAR AL MISMO NIVEL QUE EL PRIMER "if"
            continue

        # Opción 3: Eliminar fila/elemento
        if opcion == '3':
            archivo = elegir_archivo(archivos_database, 
                                   "Seleccione el número del archivo para eliminar: ")
            if not archivo:
                continue
                
            datos = leer_archivo(archivo)
            mostrar_preview(datos, archivo)
            eliminar_fila(archivo)
            continue

        # Opción 4: Modificar fila/elemento
        if opcion == '4':
            archivo = elegir_archivo(archivos_database, 
                                   "Seleccione el número del archivo para modificar: ")
            if not archivo:
                continue
                
            datos = leer_archivo(archivo)
            mostrar_preview(datos, archivo)
            
            # Mostrar información sobre búsqueda inteligente si aplica
            if archivo in RELACIONES_TABLAS:
                relaciones = RELACIONES_TABLAS[archivo]
                print("ℹ Búsqueda inteligente activa para campos relacionados")
                print("   Escriba 'lista' para ver opciones disponibles")
                print("-" * 50)
            
            modificar_fila(archivo)
            continue

        # Opción 5: Buscar datos
        if opcion == '5':
            archivo = elegir_archivo(archivos_database, 
                                   "Seleccione el número del archivo para buscar: ")
            if not archivo:
                continue
                
            datos = leer_archivo(archivo)
            mostrar_preview(datos, archivo)
            buscar_fila(archivo)
            continue

        # Opción 6: Comparar archivos
        if opcion == '6':
            menu_comparacion()  # ← SOLO ESTA LÍNEA
            continue

        # Opción 7: Conversión entre formatos
        if opcion == '7':
            menu_conversion()
            continue

        print("Opción no válida.")

if __name__ == "__main__":
    # Crear carpetas si no existen
    import os
    from herramientas import CARPETA_DATABASE, CARPETA_HIST
    
    for carpeta in [CARPETA_DATABASE, CARPETA_HIST]:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)
    
    # Iniciar menú principal
    menu()