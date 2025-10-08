import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from funciones_entropia import calcular_entropia
from funciones_ganancia import ganancia_informacion

# 1. Cargamos los datos llamando al Excel.
archivo_entrada = "TablaPrediccionAbandono-DatosFinal.xlsx"
tabla = pd.read_excel(archivo_entrada)
tabla.columns = tabla.columns.str.strip()

# 1.1. Creamos la columna "EstadoFinal" en el Excel.
columna_objetivo = "EstadoFinal"
tabla[columna_objetivo] = np.nan

print("\nColumnas detectadas en el archivo:")
print(list(tabla.columns))

print("\nCONJUNTO DE DATOS: ")
print(tabla.head())

# 2. Mostramos entropía y ganancia usando "funciones_entropia" y "funciones_ganancia".

# 2.1. Para mostrar algo, necesitamos tener algunas etiquetas de ejemplo. Usamos el criterio: Promedio >= 7 -> Continua, <7 -> Abandona.
tabla[columna_objetivo] = np.where(tabla["PromedioPrimerCuatrimestre"] >= 7, "Continua", "Abandona")

positivos_totales = sum(tabla[columna_objetivo] == "Continua")
negativos_totales = sum(tabla[columna_objetivo] == "Abandona")
entropia_total = calcular_entropia(positivos_totales, negativos_totales)

# 2.2. Imprimimos en consola la entropía obtenida. 
print("\n1. ENTROPÍA DEL CONJUNTO ORIGINAL: ")
print(f"Positivos (Continúa): {positivos_totales}, Negativos (Abandona): {negativos_totales}")
print(f"Entropía total: {entropia_total:.4f}")

# 2.3. Mostramos la ganancia de información obtenida.
print("\n2. GANANCIA DE INFORMACIÓN POR ATRIBUTO: ")
atributos = [col for col in tabla.columns if col != columna_objetivo]
ganancias = {}

# 2.4. El bucle va a procesar cada columna una por una, evaluando su poder predictivo.
for atributo in atributos:
    if pd.api.types.is_numeric_dtype(tabla[atributo]):
        tabla_temp = tabla.copy()
        tabla_temp["GrupoTemp"] = pd.qcut(tabla_temp[atributo], q=3, duplicates="drop")
        grupos = tabla_temp.groupby("GrupoTemp")[columna_objetivo].value_counts().unstack().fillna(0)
    else:
        grupos = tabla.groupby(atributo)[columna_objetivo].value_counts().unstack().fillna(0)
        # 2.4.I. El 'if' comprueba si la columna actual (atributo) es numérica.
        # 2.4.II. Si es numérica, se hace una agrupación por rangos usando cuartiles.
        # 2.4.III. Si no es numérica (categórica), se usa directamente cada categoría como grupo.
    divisiones = [(fila.get("Continua", 0), fila.get("Abandona", 0)) for _, fila in grupos.iterrows()]
    ganancia = ganancia_informacion(positivos_totales, negativos_totales, divisiones)
    ganancias[atributo] = ganancia
        # 2.4.IV. Se crean tuplas (Continua, Abandona) por cada grupo/categoría para calcular, mediante 
        # la función "ganancia_informacion", cuánto reduce la incertidumbre en ese atributo y guardar el resultado 
        # en el diccionario "ganancias".
    print(f"\n-- {atributo} --")
    print(grupos)
    print(f"Ganancia: {ganancia:.4f}")
        # 2.4. V. Muestra en consola el conteo de Continua/Abandona por grupo/categoría y la ganancia de información calculada.

# 2.5. Acá se imprime la mejor ganancia para comenzar el árbol. 
mejor_atributo = max(ganancias, key=ganancias.get)
print("\n3. MEJOR ATRIBUTO PARA COMENZAR EL ÁRBOL: ")
print(f"El atributo con mayor ganancia de información es: {mejor_atributo}")
print(f"Ganancia: {ganancias[mejor_atributo]:.4f}")

# 3. Entrenamos el árbol con scikit-learn.
tabla_modelo = tabla.copy()
le_dict = {}

# 3.1. Convertimos las variables categóricas a números.
for col in tabla_modelo.columns:
    if tabla_modelo[col].dtype == object and col != columna_objetivo:
        le = LabelEncoder()
        tabla_modelo[col] = le.fit_transform(tabla_modelo[col])
        le_dict[col] = le

# 3.2. Calculamos la columna objetivo.
le_target = LabelEncoder()
y = le_target.fit_transform(tabla[columna_objetivo])
X = tabla_modelo.drop(columns=[columna_objetivo])

# 3.3. Entrenamos el arbol de decisión.
modelo = DecisionTreeClassifier(criterion="entropy", random_state=42)
modelo.fit(X, y)

# 4. Predecimos el "EstadoFinal".
predicciones = modelo.predict(X)
tabla[columna_objetivo] = le_target.inverse_transform(predicciones)

# 5. Exportamos los resultados en un nuevo archivo de Excel.
archivo_salida = "TablaPrediccionAbandono-Final.xlsx"
tabla.to_excel(archivo_salida, index=False)

# 6. La impresion final asegura que el codigo funcione correctamente. 
print(f"\nArchivo exportado correctamente como '{archivo_salida}'")
print("\nCONJUNTO DE DATOS CON PREDICCIONES.")
print(tabla.head())

# Trabajo hecho por: Gil Lascano Lorenzo, Bayaslian Santiago, Núñez Mauro Nicolás, Buchholz Ariel.  
# Instalar pip para que el codigo funcione: "pip install openpyxl".