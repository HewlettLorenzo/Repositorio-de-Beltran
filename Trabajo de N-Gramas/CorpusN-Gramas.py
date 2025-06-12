from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
import es_core_news_sm as core

nlp = core.load()

# Función principal que nos permite llamar y leer el Corpus.
def cargar_corpus(ruta):
    with open(ruta, 'r') as corpus:
        texto = corpus.read().lower()
    return texto

# Esta función tokeniza el texto en español.
def tokenizar(texto):
    tokens = word_tokenize(texto, language='spanish')
    tokens = [t for t in tokens if t.isalpha()]  # Linea encargada de remover putuación y símbolos.
    return tokens

# Función para eliminar Stopwords del español.
def quitar_stopwords(tokens):
    stop_words = set(stopwords.words("spanish"))
    return [t for t in tokens if t not in stop_words]

# Acá está el lematizador.
def lematizar(tokens):
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc if token.is_alpha]

# La funcion permitirá extraer y calcular los N-Gramas.
def obtener_ngrama_frecuencias(texto, n, min_df=1):
    vectorizador = CountVectorizer(ngram_range=(n, n), min_df=min_df, token_pattern=r"(?u)\b\w+\b")
    try:
        matriz = vectorizador.fit_transform([texto])
        conteo = matriz.toarray().sum(axis=0)
        frec = [(ngrama.replace(" ", "_"), int(conteo[idx])) for ngrama, idx in vectorizador.vocabulary_.items()]
        return sorted(frec, key=lambda x: x[1], reverse=True)
    except ValueError as e:
        print(f"[Error] No se pudieron calcular {n}-gramas: {e}")
        return []

# Esta funcion grafica los N-gramas.
def graficar_frecuencias(frecuencias, titulo):
    if not frecuencias:
        print(f"No hay datos para graficar: {titulo}")
        return
    etiquetas = [x[0] for x in frecuencias[:15]]
    valores = [x[1] for x in frecuencias[:15]]
    plt.figure(figsize=(12, 5))
    plt.bar(etiquetas, valores, color='mediumseagreen')
    plt.xticks(rotation=45, ha='right')
    plt.title(titulo)
    plt.xlabel("N-Gramas")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

# Función secundaria: Nos permitirá mostrar la tokenización del texto, y mostrarlo sin stopwords y lematizado.
def procesar_corpus(ruta_corpus):
    texto = cargar_corpus(ruta_corpus)

    # Tokenizamos.
    tokens = tokenizar(texto)
    print("-"*70)
    print("Texto tokenizado: ")
    print(tokens)

    # Mostrar oraciones sin stopwords y lematizadas, una debajo de otra.
    oraciones = sent_tokenize(texto, language='spanish')

    print("-"*70)
    print("Oraciones sin stopwords: ")
    for oracion in oraciones:
        tokens_oracion = tokenizar(oracion)
        tokens_limpios = quitar_stopwords(tokens_oracion)
        print("* "+" ".join(tokens_limpios)+".")

    print("-"*70)
    print("Oraciones lematizadas: ")
    oraciones_lematizadas = []
    for oracion in oraciones:
        tokens_oracion = tokenizar(oracion)
        tokens_limpios = quitar_stopwords(tokens_oracion)
        lemas_oracion = lematizar(tokens_limpios)
        lematizada = " ".join(lemas_oracion)
        print("* "+lematizada+".")
        oraciones_lematizadas.append(lematizada)

    texto_lema = " ".join(oraciones_lematizadas)

    # N-gramas
    bigramas = obtener_ngrama_frecuencias(texto_lema, n=2, min_df=1)
    trigramas = obtener_ngrama_frecuencias(texto_lema, n=3, min_df=1)

    # Representar los gráficos.
    graficar_frecuencias(bigramas, "Frecuencia de Bigramas.")
    graficar_frecuencias(trigramas, "Frecuencia de Trigramas.")

# Línea de ejecución.
procesar_corpus("CorpusEducacion.txt")