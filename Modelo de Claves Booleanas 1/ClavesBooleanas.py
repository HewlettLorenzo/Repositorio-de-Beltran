import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Creamos la lista de documentos con la que vamos a tarabajar.
documents = {
    "doc1": "La inteligencia artificial está revolucionando la tecnología.",
    "doc2": "El aprendizaje automático es clave en la inteligencia artificial.",
    "doc3": "Procesamiento del lenguaje natural y redes neuronales.",
    "doc4": "Las redes neuronales son fundamentales en deep learning.",
    "doc5": "El futuro de la IA está en el aprendizaje profundo."
}

# Preprocesamiento: Se tokeniza, pasa a minúsculas y se elimnan las stopwords del español.
stop_words = set(stopwords.words('spanish'))

def preprocess(text):
    tokens = word_tokenize(text.lower())  # Convierte a minsuculas y tokeniza.
    return {word for word in tokens if word.isalnum() and word not in stop_words} # Filtra los tokens alfanúmericos.

# Construcción del índice invertido (palabra clave -> documentos en los que aparece).
index = {}
for doc_id, text in documents.items():
    words = preprocess(text)
    for word in words:
        if word not in index:
            index[word] = set()
        index[word].add(doc_id)

# Dividir la consulta en tokens: Si el token representa un operador, pasa a mayúsculas. En caso contrario, pasa a minúsculas.
def boolean_search(query):
    tokens = query.split()
    tokens = [token.upper() if token.upper() in {"AND", "OR", "NOT"} else token.lower() for token in tokens]
    
    # Acá se inicia la variable "documents".
    result_set = set(documents.keys())
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "AND":
            i += 1
            term = tokens[i]
            result_set &= index.get(term, set())
        elif token == "OR":
            i += 1
            term = tokens[i]
            result_set |= index.get(term, set())
        elif token == "NOT":
            i += 1
            term = tokens[i]
            result_set -= index.get(term, set())
        else:
            # Si es un término sin operador explícito (o el primer), se realiza la intersección.
            result_set &= index.get(token, set())
        i += 1
    return result_set

# Este es el bucle interactivo que permite al usuario realizar sus consultas booleanas.
print("\n--- Modo búsqueda interactiva ---")
while True:
    query = input("Ingrese una consulta booleana (o 'salir' para terminar): ").strip()
    if query.lower() == "salir":
        print("Saliendo del programa.")
        break
    resultados = boolean_search(query)
    if resultados:
        print("Documentos encontrados: ", resultados)
    else:
        print("No se encontró ningún documento que coincida con la consulta.")