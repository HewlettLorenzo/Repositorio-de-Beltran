import pandas as pd

# Datos de ejemplo
data = {
    "Usuario": ["user01", "user02", "user03", "user04", "user05"],
    "Acción": ["Combate", "Exploración", "Interacción social", "Combate", "Exploración"],
    "Duración (segundos)": [120, 300, 180, 90, 240],
    "Resultado": ["Victoria", "Descubrimiento", "Mensaje enviado", "Derrota", "Sin hallazgos"]
}

df = pd.DataFrame(data)

# Clasificación basada en reglas
def clasificar_accion(row):
    if row["Acción"] == "Combate":
        return "Combate largo" if row["Duración (segundos)"] >= 100 else "Combate corto"
    return row["Acción"] if row["Acción"] in ["Exploración", "Interacción social"] else "Desconocida"

# Aplicar clasificación
df["Clasificación"] = df.apply(clasificar_accion, axis=1)

# Mostrar resultados
print("Clasificación de Acciones de Usuarios: ")
print(df)