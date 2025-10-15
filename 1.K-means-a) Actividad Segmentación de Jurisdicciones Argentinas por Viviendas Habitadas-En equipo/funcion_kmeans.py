import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Función para aplicar K-Means y mostrar resultados.
def aplicar_kmeans(df, scaler, X_scaled, k=3, mostrar_codo=True):
    # Mostrar gráfico del codo.
    if mostrar_codo:
        inercia = []
        K = range(1, 10)
        for i in K:
            kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inercia.append(kmeans.inertia_)

        plt.figure(figsize=(8,5))
        plt.plot(K, inercia, marker='o', color='b')
        plt.title('Método del Codo (Elbow Method)')
        plt.xlabel('Número de Clusters (k)')
        plt.ylabel('Inercia')
        plt.xticks(K)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Aplicar K-Means final.
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Calcular centroides en escala original.
    centroides_escalados = kmeans.cluster_centers_.flatten().reshape(-1, 1)
    centroides_original = scaler.inverse_transform(centroides_escalados).flatten()

    # Etiquetas interpretables.
    orden_clusters = np.argsort(centroides_original)
    map_labels = {
        orden_clusters[0]: "Pocas viviendas",
        orden_clusters[1]: "Cantidad normal de viviendas",
        orden_clusters[2]: "Muchas viviendas"
    }
    df['Segmento'] = df['cluster'].map(map_labels)

    # Imprimir resultados.
    print("\nCentroides (viviendas) por cluster:")
    for i, c in enumerate(centroides_original):
        print(f"  Cluster {i} -> {map_labels[i]}: {int(round(c))} viviendas")

    print("\nAsignación de segmentos:")
    print(df[['Jurisdicción', 'Viviendas Habitadas', 'Segmento']]
          .sort_values('Viviendas Habitadas', ascending=False)
          .to_string(index=False))

    return df, centroides_original, map_labels