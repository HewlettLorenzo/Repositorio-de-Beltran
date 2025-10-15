import pandas as pd
from sklearn.preprocessing import StandardScaler
from funcion_kmeans import aplicar_kmeans
from funcion_graficos import graficar_clusters

# Función para cargar y escalar los datos.
def cargar_y_escalar_datos():
    data = {
        "Jurisdicción": [
            "Ciudad Autónoma de Buenos Aires",
            "Buenos Aires",
            "Catamarca",
            "Chaco",
            "Chubut",
            "Córdoba",
            "Corrientes",
            "Entre Ríos",
            "Formosa",
            "Jujuy",
            "La Pampa",
            "La Rioja",
            "Mendoza",
            "Misiones",
            "Neuquén",
            "Río Negro",
            "Salta",
            "San Juan",
            "San Luis",
            "Santa Cruz",
            "Santa Fe",
            "Santiago del Estero",
            "Tierra del Fuego, Antártida e Islas del Atlántico Sur",
            "Tucumán"
        ],
        "Viviendas Habitadas": [
            1391258, 5970702, 131978, 368728, 213317, 1378237, 370958,
            494473, 194689, 238141, 140879, 124149, 639467, 420101, 254545,
            276371, 404504, 241436, 182886, 118047, 1273460, 311361, 65535, 493794
        ]
    }

    df = pd.DataFrame(data)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[['Viviendas Habitadas']])
    return df, scaler, X_scaled

# MAIN
if __name__ == "__main__":
    df, scaler, X_scaled = cargar_y_escalar_datos()
    df, centroides, etiquetas = aplicar_kmeans(df, scaler, X_scaled, k=3, mostrar_codo=True)
    graficar_clusters(df, centroides, etiquetas)