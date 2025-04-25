print("-"*70)
def imprimir_corpus(leer_corpus):
    contenido = ""
    with open ('CorpusLenguajes.txt', 'r', encoding = "utf-8") as corpus:
        print("Contenido original del Corpus a analizar: ")
        for contenido in corpus:
            print(contenido, end = " ")
    return contenido

contenido = imprimir_corpus('CorpusLenguajes.txt')

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Leer el contenido del archivo
with open("CorpusLenguajes.txt", "r", encoding="utf-8") as corpus:
    contenido = corpus.read().strip().lower() # Limpia y convierte cada palabra en minúscula.

# Tokenizar el contenido del corpus.
print()
palabras = word_tokenize(contenido)
print("-" * 70)
print("Texto completo tokenizado: \n")
print(palabras)

# Acá importo la función para trabajar sobre stopwords.
from nltk.corpus import stopwords
import string

# Esta es la función encargada de quitar las stopwords en inglés.
def quitarStopwords_eng(palabras):
    ingles = stopwords.words("english")
    texto_limpio = [w.lower() for w in palabras if w.lower() not in ingles 
                    and w not in string.punctuation
                    and w.isalpha()
                    and w not in ["-", '|', '--', "''", "``", "_", ".-", "-.", "[", "]", "(", ")", 
                                  "quitarstopwords_eng", "word_tokenize", "lematizar", "node.js", "corpus"]]
    return texto_limpio

# Esta linea llama a la función para remover stopwords sobre las palabras tokenizadas.
texto_limpio = quitarStopwords_eng(palabras)

# Dividir el texto en oraciones.
oraciones = sent_tokenize(contenido)

# Inicializar lista para almacenar oraciones limpias.
texto_limpio_por_oracion = []

# Procesar cada oración eliminando stopwords y puntuación.
for oracion in oraciones:
    palabras = word_tokenize(oracion)  # Tokenizar palabras dentro de la oración
    stop_words = set(stopwords.words("english"))  # Ajusta el idioma según el corpus
    palabras_limpias = [w for w in palabras if w.lower() #not in stop_words 
                        and w not in string.punctuation
                        and w not in ["-", '|', '--', "''", "``", "_", ".-", "-.", "[", "]", "(", ")", 
                                      "quitarstopwords_eng", "word_tokenize", "lematizar", "corpus"]]
    texto_limpio_por_oracion.append(" ".join(palabras_limpias))  # Reconstruir la oración sin stopwords

# Imprimir cada oración limpiada en una línea separada.
print("-"*70)
print("Texto limpio con conectores gramaticales, sacando solamente stopwords: \n")
for oracion in texto_limpio_por_oracion:
    print("* "+ oracion +".")
print("-"*70)

def obtener_oraciones_limpias(ruta_corpus):
    with open(ruta_corpus, "r", encoding="utf-8") as corpus:
        texto = corpus.read()

    oraciones = sent_tokenize(texto)
    oraciones_limpias = []  # Acá se guardan oraciones como strings (cadena de caracteres).

    for oracion in oraciones:
        tokens = word_tokenize(oracion)
        limpio = quitarStopwords_eng(tokens)
        oracion_limpia = " ".join(limpio)  # Unimos los tokens en una cadena.
        oraciones_limpias.append(oracion_limpia)
    return oraciones_limpias

oraciones_tokens = obtener_oraciones_limpias("CorpusLenguajes.txt")

print("Texto limpio con remoción de Stopwords completa, incluyendo conectores gramaticales: \n")
for oracion in oraciones_tokens:
    print("* "+ oracion +".")

# Comenzamos a importar el lematizador.
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
#from nltk import pos_tag

# Inicializar lematizador.
lemmatizer = WordNetLemmatizer()
#oracion_tag = pos_tag()

# Desde acá comienzo a lematizar por separado: Verbo(v), sustantivo(n), adjetivo(a) y adverbio(v).
print("-"*70)
print("Palabras lematizadas; verbos, sustantivos, adjetivos y adverbios: \n")
lemmatized_verbs = [lemmatizer.lemmatize(w, pos='v') for w in texto_limpio if w != lemmatizer.lemmatize(w, pos='v')]
print(f"Verbos lematizados: {lemmatized_verbs} \n")
lemmatized_nouns= [lemmatizer.lemmatize(w, pos='n') for w in texto_limpio if w != lemmatizer.lemmatize(w, pos='n')]
print(f"Sustantivos lematizados: {lemmatized_nouns} \n")
lemmatized_adj=[lemmatizer.lemmatize(w, pos='a') for w in texto_limpio if w != lemmatizer.lemmatize(w, pos='a')]  
print(f"Adjetivos lematizados: {lemmatized_adj} \n")
lemmatized_adv=[lemmatizer.lemmatize(w, pos= 'r') for w in texto_limpio if w != lemmatizer.lemmatize(w, pos='r')]
print(f"Adverbios lematizados: {lemmatized_adv} \n")

# Función para eliminar palabras duplicadas manteniendo el orden original.
def eliminar_duplicados(lista):
    vista = set()
    resultado = []
    for palabra in lista:
        if palabra not in vista:
            resultado.append(palabra)
            vista.add(palabra)
    return resultado

# Se aplica la función a cada lista.
print("-"*70)
print("Eliminando duplicados...\n")
lemmatized_verbs = eliminar_duplicados(lemmatized_verbs)
print(f"Verbos lematizados (sin duplicados): {lemmatized_verbs} \n")
lemmatized_nouns = eliminar_duplicados(lemmatized_nouns)
print(f"Sustantivos lematizados (sin duplicados): {lemmatized_nouns} \n")
lemmatized_adj = eliminar_duplicados(lemmatized_adj)
print(f"Adjetivos lematizados (sin duplicados): {lemmatized_adj} \n")
lemmatized_adv = eliminar_duplicados(lemmatized_adv)
print(f"Adverbios lematizados (sin duplicados): {lemmatized_adv} \n")

print("-" * 70)
print()
print("-" * 70)

# Desde acá ya se empieza a trabajar con la MATRIZ TF-IDF.

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import FreqDist

print("Calculando matriz TF-IDF...\n")
print("-" * 70)

vectorizador = TfidfVectorizer()
tfidf_matrix = vectorizador.fit_transform(oraciones_tokens)
palabras = vectorizador.get_feature_names_out()
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=palabras)

print(df_tfidf.round(4))

# ANÁLISIS DE FRECUENCIA Y GRÁFICO.

print("-" * 70)
print("Frecuencia de palabras más comunes en texto limpio (top 25):\n")

# Usamos directamente texto_limpio (ya sin stopwords ni símbolos).
frecuencia = FreqDist(texto_limpio)

# Mostrar las 25 palabras más comunes.
for palabra, freq in frecuencia.most_common(25):
    frecuencia_rel = frecuencia.freq(palabra)
    print(f"{freq}\t{frecuencia_rel:.6f}\t{palabra}")

print("-" * 70)
print("Gráfico de frecuencia (top 20): ")
print("Reflejado en una ventana emergente... \n")
frecuencia.plot(20, show=True)

print("Trabajo realizado por: Gil Lascano Lorenzo.")