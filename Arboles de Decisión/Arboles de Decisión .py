import math
import pandas as pd

# FUNCIONES AUXILIARES

def entropia(p, n):
    # Calcula la entropía de un conjunto con p positivos y n negativos.
    if p == 0 or n == 0:
        return 0
    total = p + n
    p_ratio, n_ratio = p / total, n / total
    return - (p_ratio * math.log2(p_ratio) + n_ratio * math.log2(n_ratio))

def ganancia_info(total_p, total_n, divisiones):
    # Calcula la ganancia de información de un atributo.
    # Divisiones: lista de tuplas (positivos, negativos.
    total = total_p + total_n
    entropia_total = entropia(total_p, total_n)
    entropia_ponderada = sum(((p + n) / total) * entropia(p, n) for p, n in divisiones)
    ganancia = entropia_total - entropia_ponderada
    return entropia_total, entropia_ponderada, ganancia

def evaluar_atributo(data, atributo, p_total, n_total, nombre=None):
    # Evalúa la ganancia de información para un atributo categórico o agrupado.
    nombre = nombre or atributo
    tabla = data.groupby(atributo, observed=False)["Acepta"].value_counts().unstack().fillna(0)
    divisiones = [(fila.get("Sí", 0), fila.get("No", 0)) for _, fila in tabla.iterrows()]
    _, _, ganancia = ganancia_info(p_total, n_total, divisiones)

    print(f"\n {nombre}: ")
    print(tabla.astype(int))
    print()
    print(f"{nombre} -> Ganancia: {ganancia:.4f}")
    return ganancia

# 1) CARGAR DATOS.

data = pd.DataFrame({
    "Edad": [24, 38, 29, 45, 52, 33, 41, 27, 36, 31],
    "UsoGB": [2.5, 6.0, 3.0, 8.0, 7.5, 4.0, 5.5, 2.0, 6.5, 3.5],
    "LineaFija": ["No", "Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí", "No"],
    "Acepta": ["No", "Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí", "No"]
})

print("\n1. CONJUNTO DE DATOS: ")
print()
print(data)

# 2) ENTROPÍA TOTAL.

p_total = sum(data["Acepta"] == "Sí")
n_total = sum(data["Acepta"] == "No")
print("\n 1. ENTROPÍA DEL CONJUNTO ORIGINAL: ")
print()
print(f"Positivos (Sí): {p_total}, Negativos (No): {n_total}")
print(f"Entropía total: {entropia(p_total, n_total):.4f}")

# 3) GANANCIA DE INFORMACIÓN POR ATRIBUTO.

print("\2. GANANCIA DE INFORMACIÓN POR ATRIBUTO: ")
print()

# Edad agrupada 
data["EdadGrupo"] = pd.cut(data["Edad"], bins=[0, 30, 50, 100], labels=["Joven", "Adulto", "Mayor"])
evaluar_atributo(data, "EdadGrupo", p_total, n_total, "Edad agrupada")

# Línea fija 
evaluar_atributo(data, "LineaFija", p_total, n_total, "Línea fija")

# Uso de datos agrupado 
data["UsoGrupo"] = pd.cut(data["UsoGB"], bins=[0, 3, 6, 100], labels=["Bajo", "Medio", "Alto"])
evaluar_atributo(data, "UsoGrupo", p_total, n_total, "Uso de datos agrupado")