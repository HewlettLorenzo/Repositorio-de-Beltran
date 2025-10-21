import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Datos de ejemplo
df = pd.DataFrame([
    {'edad': 42, 'horas_estudio': 2, 'promedio_academico': 8.87},
    {'edad': 26, 'horas_estudio': 8, 'promedio_academico': 9.11},
    {'edad': 56, 'horas_estudio': 5, 'promedio_academico': 7.29},
    {'edad': 29, 'horas_estudio': 14, 'promedio_academico': 7.27},
    {'edad': 43, 'horas_estudio': 8, 'promedio_academico': 8.5},
    {'edad': 34, 'horas_estudio': 10, 'promedio_academico': 4.45},
    {'edad': 51, 'horas_estudio': 3, 'promedio_academico': 6.12},
    {'edad': 22, 'horas_estudio': 12, 'promedio_academico': 4.33},
    {'edad': 47, 'horas_estudio': 6, 'promedio_academico': 7.0},
    {'edad': 38, 'horas_estudio': 9, 'promedio_academico': 4.75},
    {'edad': 60, 'horas_estudio': 2, 'promedio_academico': 9.0},
    {'edad': 31, 'horas_estudio': 11, 'promedio_academico': 2.0},
    {'edad': 45, 'horas_estudio': 4, 'promedio_academico': 8.0},
    {'edad': 27, 'horas_estudio': 13, 'promedio_academico': 3.2},
    {'edad': 50, 'horas_estudio': 5, 'promedio_academico': 7.0},
    {'edad': 36, 'horas_estudio': 7, 'promedio_academico': 5.0},
    {'edad': 40, 'horas_estudio': 6, 'promedio_academico': 6.0},
    {'edad': 24, 'horas_estudio': 15, 'promedio_academico': 3.0},
    {'edad': 55, 'horas_estudio': 3, 'promedio_academico': 9.0},
    {'edad': 33, 'horas_estudio': 10, 'promedio_academico': 3.0}
])

# Escalado
X = StandardScaler().fit_transform(df)
# K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)

# Gráfico
plt.figure(figsize=(8,6))
plt.scatter(df['edad'], df['promedio_academico'], c=df['cluster'], cmap='viridis', s=80)
plt.title('Agrupamiento de Estudiantes (K-Means, 4 Clusters)')
plt.xlabel('Edad'); plt.ylabel('Promedio Académico')
plt.grid(True); plt.tight_layout(); plt.show()

# Resultados
centroides = pd.DataFrame(
    StandardScaler().fit(df[['edad','horas_estudio','promedio_academico']]).inverse_transform(kmeans.cluster_centers_),
    columns=['Edad Promedio', 'Horas de Estudio', 'Promedio Académico']
)
print("\nCentroides:\n", centroides.round(2))
print("\nCantidad por grupo:\n", df['cluster'].value_counts().sort_index())
print("\nPrimeros estudiantes clasificados:\n", df.head(10))