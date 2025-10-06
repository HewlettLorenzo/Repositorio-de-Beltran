import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. Datos de ejemplo
noticias = [
    "El presidente anunció una nueva reforma educativa",
    "Descubren que la vacuna convierte a las personas en robots",
    "La NASA confirma el hallazgo de agua en Marte",
    "Científicos afirman que la Tierra es plana",
    "El ministerio de salud lanza campaña contra el dengue",
    "Celebridades usan crema milagrosa para rejuvenecer 30 años",
    "Se inaugura el nuevo hospital en la ciudad",
    "Estudio revela que comer chocolate cura el cáncer",
    "Gobierno aprueba ley de protección ambiental",
    "Investigadores aseguran que los teléfonos espían nuestros sueños", 

    "Si es cuadrupedo tiene cuatro patas, si es bidupedo tiene dos patas",
    "La verdadera frecuencia cardiaca normal es de 45 latidos por minuto",
    "La Tierra es redonda",
    "El petroleo se encuentra en Marte"
]
etiquetas = [
    "real", "fake", "real", "fake", "real",
    "fake", "real", "fake", "real", "fake", 
    "real", "fake", "real", "fake"
]

tabla = pd.DataFrame({"texto": noticias, "etiqueta": etiquetas})

# 2. Preparar los datos
textos = tabla["texto"]
clases = tabla["etiqueta"]

# 3. Convertir texto en matriz de conteo de palabras
vectorizador = CountVectorizer()
matriz = vectorizador.fit_transform(textos)

# 4. Dividir en entrenamiento y prueba
textoTrain, textoTest, claseTrain, claseTest = train_test_split(
    matriz, clases, test_size=0.2, random_state=42)

# 5. Crear y entrenar el modelo
modelo = MultinomialNB()
modelo.fit(textoTrain, claseTrain)

# 6. Evaluar el modelo
predicciones = modelo.predict(textoTest)
precision = accuracy_score(claseTest, predicciones)
matrizConfusion = confusion_matrix(claseTest, predicciones, labels=["real", "fake"])

# 7. Probar con nuevos textos
nuevosTextos = [
    "Nuevo estudio demuestra que el café mejora la memoria",
    "Expertos afirman que los gatos pueden hablar con humanos",
    
    "La reforma educativa fue aprobada por el parlamento",
    "Los gatos son animales de cuatro patas",
    "La frecuencia cardiaca es de 60 latidos por minuto es un pico de presión",
    "Científicos desmienten que la Tierra es redonda",
    "El petroleo no se encuentra fuera de la Tierra"]

nuevosVector = vectorizador.transform(nuevosTextos)
nuevasPredicciones = modelo.predict(nuevosVector)

# 8. Resultados
print("\nRESULTADOS DEL MODELO: ")
print(f"Precisión del modelo: {precision:.2f}\n")
print("Matriz de confusión:")
print(matrizConfusion)

print("\nPREDICCIONES PARA NUEVAS NOTICIAS: ")
for texto, resultado in zip(nuevosTextos, nuevasPredicciones):
    print(f"Noticia: '{texto}'-> Predicción: {resultado}")
print()