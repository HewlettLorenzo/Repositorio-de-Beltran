import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates
from io import BytesIO
import os

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Maquetas de Trenes",
    page_icon="🚂",
    layout="wide"
)

# Título principal
st.title("🚂 Dashboard de Ventas - Maquetas de Trenes")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    try:
        # Definir rutas absolutas
        base_dir = r"D:\Beltrán\Segundo año TS CD e IA\Modelizado de Minería de Datos\TSCIA_MMD\Proyecto_4\DataCSV"
        
        # Verificar que el directorio existe
        if not os.path.exists(base_dir):
            st.error(f"❌ No se encuentra el directorio: {base_dir}")
            return None
            
        # Construir rutas completas
        productos_path = os.path.join(base_dir, "producto_trenes.csv")
        fabricantes_path = os.path.join(base_dir, "fabricantes.csv")
        clientes_path = os.path.join(base_dir, "clientes.csv")
        ventas_path = os.path.join(base_dir, "facturas.csv")
        
        # Verificar que los archivos existen
        archivos = {
            "producto_trenes.csv": productos_path,
            "fabricantes.csv": fabricantes_path,
            "clientes.csv": clientes_path,
            "facturas.csv": ventas_path
        }
        
        for nombre, ruta in archivos.items():
            if not os.path.exists(ruta):
                st.error(f"❌ No se encuentra el archivo: {ruta}")
                return None
        
        st.success("✅ Todos los archivos encontrados correctamente")
        
        # Cargar todos los datasets
        productos_df = pd.read_csv(productos_path, sep=';', encoding='utf-8')
        fabricantes_df = pd.read_csv(fabricantes_path, sep=';', encoding='utf-8')
        clientes_df = pd.read_csv(clientes_path, sep=';', encoding='utf-8')
        ventas_df = pd.read_csv(ventas_path, sep=';', encoding='utf-8')

        # Renombrar columnas ID para evitar conflictos
        productos_df = productos_df.rename(columns={'ID': 'producto_ID'})
        fabricantes_df = fabricantes_df.rename(columns={'ID': 'fabricante_ID'})
        clientes_df = clientes_df.rename(columns={'ID': 'cliente_ID'})

        # Merge de datos
        ventas_completas_df = ventas_df.merge(
            productos_df, left_on='id_producto', right_on='producto_ID', how='left'
        ).merge(
            fabricantes_df, left_on='id_fabricante_maqueta', right_on='fabricante_ID', how='left'
        ).merge(
            clientes_df, left_on='id_clientes', right_on='cliente_ID', how='left'
        )

        ventas_completas_df['FechaEmision'] = pd.to_datetime(ventas_completas_df['FechaEmision'])
        
        return {
            'productos': productos_df,
            'fabricantes': fabricantes_df,
            'clientes': clientes_df,
            'ventas': ventas_df,
            'ventas_completas': ventas_completas_df
        }
        
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return None

# Mostrar información de carga
st.subheader("📂 Cargando datos...")
data = load_data()

if data is not None:
    productos_df = data['productos']
    fabricantes_df = data['fabricantes']
    clientes_df = data['clientes']
    ventas_df = data['ventas']
    ventas_completas_df = data['ventas_completas']
    
    st.success(f"✅ Datos cargados correctamente: {len(productos_df)} productos, {len(ventas_df)} ventas")

    # ========================================
    # 1. STOCK POR FABRICANTE
    # ========================================
    st.header("📦 Distribución de Stock por Fabricante")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 8))
        stock_por_fabricante = productos_df.groupby('id_fabricante_maqueta')['CantStockActual'].sum()
        fabricantes_nombres = fabricantes_df.set_index('fabricante_ID').loc[stock_por_fabricante.index]['Fabricante']
        
        colors_pie = ['#FF6B6B', '#4ECDC4', '#FFE66D']
        ax.pie(stock_por_fabricante.values, labels=fabricantes_nombres.values, 
               autopct='%1.1f%%', colors=colors_pie, startangle=90)
        ax.set_title('Distribución de Stock Actual por Fabricante', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader("📊 Resumen Stock")
        for fabricante_id, stock in stock_por_fabricante.items():
            nombre_fab = fabricantes_df[fabricantes_df['fabricante_ID'] == fabricante_id]['Fabricante'].iloc[0]
            st.metric(f"Stock {nombre_fab}", f"{stock} unidades")
        
        total_stock = stock_por_fabricante.sum()
        st.metric("Stock Total", f"{total_stock} unidades")
    
    st.markdown("""
    **Análisis:** El gráfico circular muestra la distribución del stock actual entre los tres principales fabricantes. 
    Esta distribución refleja la estrategia de abastecimiento y la demanda histórica por cada marca.
    """)
    st.markdown("---")

    # ========================================
    # 2. PRODUCTOS MÁS VENDIDOS
    # ========================================
    st.header("🔥 Productos Más Vendidos")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ventas_por_producto = ventas_df.groupby('id_producto')['Cantidad'].sum().sort_values(ascending=False)
    productos_nombres = productos_df.set_index('producto_ID').loc[ventas_por_producto.index]['Nombre']
    
    bars = ax.bar(range(len(ventas_por_producto)), ventas_por_producto.values, color='#2E8B57', alpha=0.8)
    ax.set_xlabel('Productos')
    ax.set_ylabel('Cantidad Vendida')
    ax.set_title('Productos Más Vendidos', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(ventas_por_producto)))
    ax.set_xticklabels([f"{nombre[:15]}..." for nombre in productos_nombres.values], rotation=45, ha='right')
    
    for bar, valor in zip(bars, ventas_por_producto.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, str(valor), 
                ha='center', va='bottom', fontsize=9)
    
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)
    
    st.markdown("""
    **Análisis:** Se observa una clara preferencia por ciertos modelos específicos, posiblemente relacionados con su escala, 
    nivel de detalle o precio accesible. Los productos en el rango medio de precio tienden a tener mejor rotación.
    """)
    st.markdown("---")

    # ========================================
    # 3. PRECIOS DE PRODUCTOS
    # ========================================
    st.header("💰 Análisis de Precios")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    productos_ordenados = productos_df.sort_values('PrecioUSD', ascending=False)
    bars = ax.bar(range(len(productos_ordenados)), productos_ordenados['PrecioUSD'], color='#87CEEB', alpha=0.8)
    ax.set_xlabel('Productos')
    ax.set_ylabel('Precio (USD)')
    ax.set_title('Precios de los Productos', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(productos_ordenados)))
    ax.set_xticklabels([f"{row['Nombre'][:15]}..." for _, row in productos_ordenados.iterrows()], 
                       rotation=45, ha='right')
    
    for bar, precio in zip(bars, productos_ordenados['PrecioUSD']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, f"${precio:.2f}", 
                ha='center', va='bottom', fontsize=9)
    
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)
    
    st.markdown("""
    **Análisis:** Se observa una amplia variación en los precios, desde modelos básicos hasta ediciones premium de colección. 
    La estrategia de precios parece segmentar el mercado en diferentes niveles: entrada, intermedio y premium.
    """)
    st.markdown("---")

    # ========================================
    # 4. EVOLUCIÓN DE VENTAS
    # ========================================
    st.header("📈 Evolución Temporal de Ventas")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    ventas_por_mes = ventas_completas_df.groupby(ventas_completas_df['FechaEmision'].dt.to_period('M')).size()
    ventas_por_mes.index = ventas_por_mes.index.to_timestamp()
    
    ax.plot(ventas_por_mes.index, ventas_por_mes.values, color='#FF4444', linewidth=2.5, marker='o')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cantidad de Ventas')
    ax.set_title('Evolución de Ventas Mensuales (2023-2025)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    st.pyplot(fig)
    
    st.markdown("""
    **Análisis:** La línea de tendencia muestra la evolución mensual de ventas desde enero 2023 hasta julio 2025. 
    Se identifican patrones estacionales claros con picos en ciertos meses, posiblemente relacionados con temporadas festivas.
    """)
    st.markdown("---")

    # ========================================
    # 5. CLIENTES QUE MÁS COMPRARON
    # ========================================
    st.header("👥 Clientes Más Activos")
    
    fig, ax = plt.subplots(figsize=(12, 10))
    compras_por_cliente = ventas_df.groupby('id_clientes')['Cantidad'].sum().sort_values(ascending=True).tail(15)
    clientes_nombres = clientes_df.set_index('cliente_ID').loc[compras_por_cliente.index]['Nombre']
    
    bars = ax.barh(range(len(compras_por_cliente)), compras_por_cliente.values, color='#32CD32', alpha=0.8)
    ax.set_ylabel('Clientes')
    ax.set_xlabel('Cantidad Total Comprada')
    ax.set_title('Top 15 - Clientes que Más Compraron', fontsize=14, fontweight='bold')
    ax.set_yticks(range(len(compras_por_cliente)))
    ax.set_yticklabels([nombre[:20] + "..." if len(nombre) > 20 else nombre for nombre in clientes_nombres.values])
    
    for bar, valor in zip(bars, compras_por_cliente.values):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, str(valor), 
                ha='left', va='center', fontsize=9)
    
    ax.grid(axis='x', alpha=0.3)
    st.pyplot(fig)
    
    st.markdown("""
    **Análisis:** Estos clientes representan una valiosa base de coleccionistas frecuentes que deben ser objetivo de programas 
    de fidelización. El análisis sugiere que un pequeño grupo de clientes contribuye desproporcionadamente a las ventas totales.
    """)
    st.markdown("---")

    # ========================================
    # 6. PRODUCTOS MÁS CAROS
    # ========================================
    st.header("💎 Productos Premium")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    productos_caros = productos_df.nlargest(8, 'PrecioUSD')
    bars = ax.bar(range(len(productos_caros)), productos_caros['PrecioUSD'], color='#FFD700', alpha=0.8)
    ax.set_xlabel('Productos')
    ax.set_ylabel('Precio (USD)')
    ax.set_title('Productos Más Caros', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(productos_caros)))
    ax.set_xticklabels([f"{row['Nombre'][:15]}..." for _, row in productos_caros.iterrows()], 
                       rotation=45, ha='right')
    
    for bar, precio in zip(bars, productos_caros['PrecioUSD']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f"${precio:.2f}", 
                ha='center', va='bottom', fontsize=9)
    
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)
    
    st.markdown("""
    **Análisis:** Las maquetas de mayor precio generalmente corresponden a ediciones limitadas, alto nivel de detalle o escalas especiales. 
    Aunque estos productos tienen menor rotación, contribuyen significativamente al margen bruto y al prestigio de la marca.
    """)
    st.markdown("---")

    # ========================================
    # 7. MATRIZ DE CALOR
    # ========================================
    st.header("🔍 Relación Precio vs Cantidad Vendida")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    top_productos = productos_df.nlargest(5, 'PrecioUSD')
    matriz_data = []
    for _, producto in top_productos.iterrows():
        cantidad_vendida = ventas_df[ventas_df['id_producto'] == producto['producto_ID']]['Cantidad'].sum()
        matriz_data.append([producto['PrecioUSD'], cantidad_vendida])
    
    matriz_data = np.array(matriz_data).T
    
    sns.heatmap(matriz_data, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax,
                xticklabels=[f"Prod {i}" for i in top_productos['producto_ID']],
                yticklabels=['Precio (USD)', 'Cantidad Vendida'])
    ax.set_title('Matriz de Calor: Precio vs Cantidad Vendida (Top 5 Productos Más Caros)', 
                 fontsize=14, fontweight='bold')
    
    st.pyplot(fig)
    
    st.markdown("""
    **Análisis:** Se observa que los productos más costosos no necesariamente son los menos vendidos, sugiriendo que existe 
    un segmento de coleccionistas dispuestos a invertir en piezas premium. Esta relación precio-demanda ayuda a optimizar 
    la estrategia de precios.
    """)
    st.markdown("---")

    # ========================================
    # ESTADÍSTICAS FINALES
    # ========================================
    st.header("📋 Resumen Ejecutivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ventas = ventas_df['Cantidad'].sum()
        st.metric("Total Ventas Realizadas", f"{total_ventas} unidades")
    
    with col2:
        total_clientes = ventas_df['id_clientes'].nunique()
        st.metric("Clientes Únicos", f"{total_clientes}")
    
    with col3:
        total_productos = productos_df['producto_ID'].nunique()
        st.metric("Productos en Catálogo", f"{total_productos}")
    
    with col4:
        producto_mas_vendido = ventas_por_producto.index[0]
        nombre_mas_vendido = productos_df[productos_df['producto_ID'] == producto_mas_vendido]['Nombre'].iloc[0]
        st.metric("Producto Más Vendido", f"{nombre_mas_vendido[:15]}...")

else:
    st.error("""
    ❌ No se pudieron cargar los datos. 
    
    Verifica que:
    1. Los archivos CSV estén en la ruta: `D:\\Beltrán\\Segundo año TS CD e IA\\Modelizado de Minería de Datos\\TSCIA_MMD\\Proyecto_4\\DataCSV`
    2. Los nombres de archivo sean exactamente:
       - facturas.csv
       - fabricantes.csv  
       - producto_trenes.csv
       - clientes.csv
    """)

# Pie de página
st.markdown("---")
st.caption("Dashboard de Análisis de Ventas - Maquetas de Trenes | Generado con Streamlit")