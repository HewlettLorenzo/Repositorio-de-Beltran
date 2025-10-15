import numpy as np
import matplotlib.pyplot as plt

# Función para visualizar los clusters.
def graficar_clusters(df, centroides_original, map_labels):
    plt.figure(figsize=(12,6))
    x = np.arange(len(df))

    for cluster_id in sorted(df['cluster'].unique()):
        grupo = df[df['cluster'] == cluster_id]
        plt.scatter(grupo.index, grupo['Viviendas Habitadas'], s=100, label=map_labels[cluster_id])

    for cluster_id in range(len(centroides_original)):
        plt.hlines(centroides_original[cluster_id], xmin=-0.5, xmax=len(df)-0.5, linestyles='dashed')

    plt.xticks(x, df['Jurisdicción'], rotation=90)
    plt.xlabel('Jurisdicción')
    plt.ylabel('Viviendas Habitadas')
    plt.title('Agrupamiento de jurisdicciones por cantidad de viviendas (K-Means, 3 clusters)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()