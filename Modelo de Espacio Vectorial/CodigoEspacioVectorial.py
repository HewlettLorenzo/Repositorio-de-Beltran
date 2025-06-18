import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargamos los documentos mediante una variable.
docs = {"doc1": "El veloz zorro marrón salta sobre el perro perezoso.",
    "doc2": "Un perro marrón persiguió al zorro.",
    "doc3": "El perro es perezoso."}

# Listamos los textos y nombres.
nombres = list(docs.keys())
textos = list(docs.values())

# Realizamos la vectorización con la matriz TF-IDF.
vectorizador = TfidfVectorizer()
tfidf_matrix = vectorizador.fit_transform(textos)

# Mostramos la similitud del coseno entre documentos.
sim_matrix = cosine_similarity(tfidf_matrix)

# Lineas que muestran la matriz de similitud numérica. 
print("Matriz de similitud (coseno):")
for i in range(len(sim_matrix)):
    print(f"{nombres[i]}: {sim_matrix[i]}")

# Graficamos haciendo uso de "matplotlib".
fig, ax = plt.subplots()
cax = ax.matshow(sim_matrix, cmap='Greens')
plt.title("Matriz de Similitud de Coseno", pad=20)
plt.colorbar(cax)

# Etiquetas de las filas y las columnas de la matriz TF-IDF.
ax.set_xticks(range(len(nombres)))
ax.set_yticks(range(len(nombres)))
ax.set_xticklabels(nombres)
ax.set_yticklabels(nombres)

# Acá se muestran los valores de cada celda.
for i in range(len(nombres)):
    for j in range(len(nombres)):
        valor = sim_matrix[i][j]
        ax.text(j, i, f"{valor:.2f}", va='center', ha='center', color='black')

plt.tight_layout()
plt.show()