from funciones_csv import leer_csv, existe_modificado, CARPETA_ORIGINAL, CARPETA_MODIFICADA
from operaciones_csv import agregar_fila, eliminar_fila, modificar_fila, buscar_fila
from listado_csv import listar_originales, listar_modificados, mostrar_preview, elegir_archivo, preguntar_uso_modificado, leer_csv as leer_csv_listado, comparar_csv

def menu():
    while True:
        print("-"*70)
        print("MENÚ PRINCIPAL: ")
        print()
        print("1. Leer CSVs.")
        print("2. Agregar fila.")
        print("3. Eliminar fila (Sólo sobre CSVs modificados).")
        print("4. Modificar fila. ")
        print("5. Buscar datos. ")
        print("6. Comparar CSV Original y Modificado.")
        print("7. Salir.")
        print("-"*70)

        opcion = input("Seleccione una opción: ").strip()
        if opcion == '7':
            break

        originales = listar_originales()
        modificados = listar_modificados()

        if opcion == '1':
            leer_csv_listado()
            continue

        if opcion == '2':
            archivo = elegir_archivo(originales, "Seleccione el número del archivo para agregar: ")
            if not archivo:
                continue
            usar_mod = preguntar_uso_modificado(archivo)
            df = leer_csv(archivo, use_modificado=usar_mod)
            mostrar_preview(df, archivo)
            agregar_fila(archivo)
            continue

        if opcion == '3':
            mods = listar_modificados()
            if not mods:
                print("No hay archivos modificados. Cree/modifique primero para poder eliminar.")
                continue
            archivo = elegir_archivo(mods, "Seleccione el número del archivo modificado para eliminar fila: ")
            if not archivo:
                continue
            df = leer_csv(archivo, use_modificado=True)
            mostrar_preview(df, archivo)
            eliminar_fila(archivo)
            continue

        if opcion == '4':
            archivo = elegir_archivo(originales, "Seleccione el número del archivo para modificar: ")
            if not archivo:
                continue
            usar_mod = preguntar_uso_modificado(archivo)
            df = leer_csv(archivo, use_modificado=usar_mod)
            mostrar_preview(df, archivo)
            modificar_fila(archivo)
            continue

        if opcion == '5':
            archivo = elegir_archivo(originales, "Seleccione el número del archivo para buscar: ")
            if not archivo:
                continue
            usar_mod = preguntar_uso_modificado(archivo)
            df = leer_csv(archivo, use_modificado=usar_mod)
            mostrar_preview(df, archivo)
            try:
                buscar_fila(archivo, use_modificado=usar_mod)
            except TypeError:
                buscar_fila(archivo)
            continue

        if opcion == '6':
            archivo = elegir_archivo(originales, "Seleccione el archivo para comparar original vs modificado: ")
            if archivo:
                comparar_csv(archivo)
            continue

        print("Opción no válida.")

if __name__ == "__main__":
    menu()

# Cambios a realizar: Levantar todos los CSV primero. (Agregar bandera a la opción 1)