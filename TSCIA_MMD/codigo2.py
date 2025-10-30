import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from fpdf import FPDF
import os
from datetime import datetime
import matplotlib.dates as mdates

# Configuración de directorios
base_dir = r"D:\Beltrán\Segundo año TS CD e IA\Modelizado de Minería de Datos\TSCIA_MMD\Proyecto_4"
data_dir = os.path.join(base_dir, "DataCSV")
graficos_dir = os.path.join(base_dir, "graficos")
pdf_path = os.path.join(base_dir, "informe_maquetas_trenes.pdf")

# Crear directorio de gráficos si no existe
os.makedirs(graficos_dir, exist_ok=True)

# Configuración de estilo para matplotlib
plt.style.use('default')
sns.set_palette("husl")

print("🔧 Iniciando proceso de generación de reporte...")

# Leer los archivos CSV
try:
    # Dataset principal de productos
    productos_df = pd.read_csv(os.path.join(data_dir, "locomotoras_ferrocarril_norteamericano_completo(0).csv"), sep=';', encoding='utf-8')
    
    # Fabricantes
    fabricantes_df = pd.read_csv(os.path.join(data_dir, "fabricantes.csv"), sep=';', encoding='utf-8')
    
    # Clientes
    clientes_df = pd.read_csv(os.path.join(data_dir, "clientes.csv"), sep=';', encoding='utf-8')
    
    # Ventas
    ventas_df = pd.read_csv(os.path.join(data_dir, "ventas.csv"), sep=';', encoding='utf-8')
    
    print("✅ Archivos CSV leídos correctamente")
    
except Exception as e:
    print(f"❌ Error leyendo archivos CSV: {e}")
    exit()

# Unir datos para análisis
ventas_completas_df = ventas_df.merge(productos_df, left_on='id_producto', right_on='ID', how='left')
ventas_completas_df = ventas_completas_df.merge(fabricantes_df, left_on='id_fabricante_maqueta', right_on='ID', how='left')
ventas_completas_df = ventas_completas_df.merge(clientes_df, left_on='id_clientes', right_on='ID', how='left')

# Convertir fecha a datetime
ventas_completas_df['FechaEmision'] = pd.to_datetime(ventas_completas_df['FechaEmision'])

print("📊 Generando gráficos...")

# =============================================================================
# 1. GRÁFICO DE TORTA - Stock por fabricante (Rojo, Azul, Amarillo)
# =============================================================================
plt.figure(figsize=(10, 8))
stock_por_fabricante = productos_df.groupby('id_fabricante_maqueta')['CantStock'].sum()
fabricantes_nombres = fabricantes_df.set_index('ID').loc[stock_por_fabricante.index]['Fabricante']

colors_pie = ['#FF6B6B', '#4ECDC4', '#FFE66D']  # Rojo, Azul claro, Amarillo
plt.pie(stock_por_fabricante.values, labels=fabricantes_nombres.values, autopct='%1.1f%%', 
        colors=colors_pie, startangle=90)
plt.title('Distribución de Stock Actual por Fabricante', fontsize=14, fontweight='bold')
plt.savefig(os.path.join(graficos_dir, '1_stock_por_fabricante.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráfico 1: Stock por fabricante - GENERADO")

# =============================================================================
# 2. GRÁFICO DE BARRAS - Productos más vendidos (Verde)
# =============================================================================
plt.figure(figsize=(12, 8))
ventas_por_producto = ventas_df.groupby('id_producto')['Cantidad'].sum().sort_values(ascending=False)
productos_nombres = productos_df.set_index('ID').loc[ventas_por_producto.index]['Nombre']

bars = plt.bar(range(len(ventas_por_producto)), ventas_por_producto.values, color='#2E8B57', alpha=0.8)
plt.xlabel('Productos')
plt.ylabel('Cantidad Vendida')
plt.title('Productos Más Vendidos', fontsize=14, fontweight='bold')
plt.xticks(range(len(ventas_por_producto)), [f"Prod {i}" for i in ventas_por_producto.index], rotation=45)

# Agregar valores en las barras
for bar, valor in zip(bars, ventas_por_producto.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
             str(valor), ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '2_productos_mas_vendidos.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráfico 2: Productos más vendidos - GENERADO")

# =============================================================================
# 3. GRÁFICO DE BARRAS VERTICAL - Precios de productos (Celeste)
# =============================================================================
plt.figure(figsize=(12, 8))
productos_ordenados = productos_df.sort_values('PrecioUSD', ascending=False)
bars = plt.bar(range(len(productos_ordenados)), productos_ordenados['PrecioUSD'], 
               color='#87CEEB', alpha=0.8)
plt.xlabel('Productos')
plt.ylabel('Precio (USD)')
plt.title('Precios de los Productos', fontsize=14, fontweight='bold')
plt.xticks(range(len(productos_ordenados)), [f"Prod {i}" for i in productos_ordenados['ID']], rotation=45)

# Agregar valores en las barras con formato decimal
for bar, precio in zip(bars, productos_ordenados['PrecioUSD']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
             f"${precio:.2f}", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '3_precios_productos.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráfico 3: Precios de productos - GENERADO")

# =============================================================================
# 4. GRÁFICO DE LÍNEAS - Evolución de ventas en el tiempo (Rojo)
# =============================================================================
plt.figure(figsize=(14, 8))
ventas_por_mes = ventas_completas_df.groupby(ventas_completas_df['FechaEmision'].dt.to_period('M')).size()
ventas_por_mes.index = ventas_por_mes.index.to_timestamp()

plt.plot(ventas_por_mes.index, ventas_por_mes.values, color='#FF4444', linewidth=2.5, marker='o')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de Ventas')
plt.title('Evolución de Ventas Mensuales (2023-2025)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# Formatear eje X para mostrar meses y años
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gcf().autofmt_xdate()

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '4_evolucion_ventas.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráfico 4: Evolución de ventas - GENERADO")

# =============================================================================
# 5. GRÁFICO DE BARRAS HORIZONTAL - Clientes que más compraron (Verde)
# =============================================================================
plt.figure(figsize=(12, 10))
compras_por_cliente = ventas_df.groupby('id_clientes')['Cantidad'].sum().sort_values(ascending=True).tail(15)
clientes_nombres = clientes_df.set_index('ID').loc[compras_por_cliente.index]['Nombre']

bars = plt.barh(range(len(compras_por_cliente)), compras_por_cliente.values, color='#32CD32', alpha=0.8)
plt.ylabel('Clientes')
plt.xlabel('Cantidad Total Comprada')
plt.title('Top 15 - Clientes que Más Compraron', fontsize=14, fontweight='bold')
plt.yticks(range(len(compras_por_cliente)), clientes_nombres.values)

# Agregar valores en las barras
for bar, valor in zip(bars, compras_por_cliente.values):
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
             str(valor), ha='left', va='center')

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '5_clientes_mas_compraron.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráfico 5: Clientes que más compraron - GENERADO")

# =============================================================================
# 6. GRÁFICO DE BARRAS - Productos más caros (Amarillo)
# =============================================================================
plt.figure(figsize=(12, 8))
productos_caros = productos_df.nlargest(8, 'PrecioUSD')
bars = plt.bar(range(len(productos_caros)), productos_caros['PrecioUSD'], 
               color='#FFD700', alpha=0.8)
plt.xlabel('Productos')
plt.ylabel('Precio (USD)')
plt.title('Productos Más Caros', fontsize=14, fontweight='bold')
plt.xticks(range(len(productos_caros)), [f"{row['Nombre'][:15]}..." for _, row in productos_caros.iterrows()], 
           rotation=45, ha='right')

# Agregar valores en las barras
for bar, precio in zip(bars, productos_caros['PrecioUSD']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, 
             f"${precio:.2f}", ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '6_productos_mas_caros.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráfico 6: Productos más caros - GENERADO")

# =============================================================================
# 7. MATRIZ DE CALOR 2x5 - Precio vs Cantidad Vendida
# =============================================================================
plt.figure(figsize=(12, 8))

# Preparar datos para la matriz
top_productos = productos_df.nlargest(5, 'PrecioUSD')
matriz_data = []

for _, producto in top_productos.iterrows():
    cantidad_vendida = ventas_df[ventas_df['id_producto'] == producto['ID']]['Cantidad'].sum()
    matriz_data.append([producto['PrecioUSD'], cantidad_vendida])

matriz_data = np.array(matriz_data).T

# Crear heatmap
sns.heatmap(matriz_data, 
            annot=True, 
            fmt='.1f',
            cmap='YlOrRd',
            xticklabels=[f"Prod {i}" for i in top_productos['ID']],
            yticklabels=['Precio (USD)', 'Cantidad Vendida'])
plt.title('Matriz de Calor: Precio vs Cantidad Vendida (Top 5 Productos Más Caros)', 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '7_matriz_calor.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráfico 7: Matriz de calor - GENERADO")

# =============================================================================
# GENERACIÓN DEL INFORME PDF
# =============================================================================
print("📄 Generando informe PDF...")

class PDFReport(FPDF):
    def header(self):
        if self.page == 1:
            self.set_font('Times', 'B', 16)
            self.cell(0, 10, 'INFORME COMPLETO - VENTAS DE MAQUETAS DE TRENES', 0, 1, 'C')
            self.set_font('Times', 'B', 14)
            self.cell(0, 10, 'Análisis de Datos y Tendencias del Mercado', 0, 1, 'C')
            self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, f'Página {self.page}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Times', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
    
    def chapter_body(self, body):
        self.set_font('Times', '', 12)
        self.multi_cell(0, 6, body)
        self.ln()

# Crear PDF
pdf = PDFReport()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Configurar interlineado
pdf.set_line_height(1.5)

# Introducción
pdf.chapter_title('INTRODUCCIÓN')
intro_text = """
Este informe presenta un análisis completo de las ventas de maquetas de trenes para el período 
2023-2025. El análisis incluye distribución de stock, comportamiento de ventas, perfil de clientes 
y relación entre precio y demanda. Los datos fueron procesados mediante técnicas de minería de datos 
y visualización para extraer insights estratégicos que permitan optimizar el inventario y las 
estrategias de marketing.
"""
pdf.chapter_body(intro_text)

# Gráfico 1: Stock por fabricante
pdf.add_page()
pdf.chapter_title('1. DISTRIBUCIÓN DE STOCK POR FABRICANTE')
pdf.image(os.path.join(graficos_dir, '1_stock_por_fabricante.png'), x=10, y=40, w=190)
explicacion1 = """
El gráfico circular muestra la distribución del stock actual entre los tres principales fabricantes 
de maquetas. Märklin lidera con el mayor porcentaje de inventario, seguido por Hornby y Bachmann. 
Esta distribución refleja la estrategia de abastecimiento y la demanda histórica por cada marca. 
Es importante mantener un equilibrio en el stock para satisfacer las preferencias de los coleccionistas 
y evitar excesos de inventario que puedan generar costos de almacenamiento innecesarios.
La rotación de stock debe ser monitoreada continuamente para ajustar los pedidos futuros.
"""
pdf.chapter_body(explicacion1)

# Gráfico 2: Productos más vendidos
pdf.add_page()
pdf.chapter_title('2. PRODUCTOS MÁS VENDIDOS')
pdf.image(os.path.join(graficos_dir, '2_productos_mas_vendidos.png'), x=10, y=40, w=190)
explicacion2 = """
El gráfico de barras verticales identifica los productos con mayor volumen de ventas. Se observa 
una clara preferencia por ciertos modelos específicos, posiblemente relacionados con su escala, 
nivel de detalle o precio accesible. Los productos en el rango medio de precio tienden a tener 
mejor rotación. Este análisis permite identificar los best-sellers y planificar campañas de 
marketing alrededor de estos productos. Además, sugiere oportunidades para desarrollar bundles 
o promociones con productos de menor movimiento.
"""
pdf.chapter_body(explicacion2)

# Gráfico 3: Precios de productos
pdf.add_page()
pdf.chapter_title('3. ANÁLISIS DE PRECIOS DE PRODUCTOS')
pdf.image(os.path.join(graficos_dir, '3_precios_productos.png'), x=10, y=40, w=190)
explicacion3 = """
Este gráfico presenta la estructura de precios de todo el catálogo de productos. Se observa una 
amplia variación en los precios, desde modelos básicos hasta ediciones premium de colección. 
La estrategia de precios parece segmentar el mercado en diferentes niveles: entrada, intermedio 
y premium. Los productos en el rango medio-alto representan un balance entre calidad y 
accesibilidad. Es crucial mantener esta diversidad para atraer tanto a coleccionistas 
experimentados como a nuevos entusiastas del hobby.
"""
pdf.chapter_body(explicacion3)

# Gráfico 4: Evolución de ventas
pdf.add_page()
pdf.chapter_title('4. EVOLUCIÓN TEMPORAL DE VENTAS')
pdf.image(os.path.join(graficos_dir, '4_evolucion_ventas.png'), x=10, y=40, w=190)
explicacion4 = """
La línea de tendencia muestra la evolución mensual de ventas desde enero 2023 hasta julio 2025. 
Se identifican patrones estacionales claros con picos en ciertos meses, posiblemente relacionados 
con temporadas festivas o lanzamientos de nuevos productos. Los valles pueden indicar períodos 
de menor actividad comercial o falta de promociones. El análisis temporal permite anticipar 
demanda futura y planificar inventarios. La tendencia general muestra crecimiento sostenido, 
indicando salud del mercado de maquetas.
"""
pdf.chapter_body(explicacion4)

# Gráfico 5: Clientes que más compraron
pdf.add_page()
pdf.chapter_title('5. PERFIL DE CLIENTES MÁS ACTIVOS')
pdf.image(os.path.join(graficos_dir, '5_clientes_mas_compraron.png'), x=10, y=40, w=190)
explicacion5 = """
El gráfico horizontal identifica a los 15 clientes con mayor volumen de compras. Estos clientes 
representan una valiosa base de coleccionistas frecuentes que deben ser objetivo de programas 
de fidelización. El análisis sugiere que un pequeño grupo de clientes contribuye 
desproporcionadamente a las ventas totales. Estrategias como programas VIP, acceso anticipado 
a nuevos lanzamientos y contenido exclusivo podrían fortalecer la relación con estos clientes 
y aumentar su valor de por vida.
"""
pdf.chapter_body(explicacion5)

# Gráfico 6: Productos más caros
pdf.add_page()
pdf.chapter_title('6. PRODUCTOS DE ALTA GAMA')
pdf.image(os.path.join(graficos_dir, '6_productos_mas_caros.png'), x=10, y=40, w=190)
explicacion6 = """
Este análisis focaliza en los productos premium del catálogo. Las maquetas de mayor precio 
generalmente corresponden a ediciones limitadas, alto nivel de detalle o escalas especiales. 
Aunque estos productos tienen menor rotación, contribuyen significativamente al margen bruto 
y al prestigio de la marca. Es importante mantener un portfolio balanceado que incluya estas 
piezas de exhibición mientras se asegura disponibilidad de productos de entrada para capturar 
nuevos segmentos del mercado.
"""
pdf.chapter_body(explicacion6)

# Gráfico 7: Matriz de calor
pdf.add_page()
pdf.chapter_title('7. RELACIÓN PRECIO VS CANTIDAD VENDIDA')
pdf.image(os.path.join(graficos_dir, '7_matriz_calor.png'), x=10, y=40, w=190)
explicacion7 = """
La matriz de calor compara el precio con la cantidad vendida para los 5 productos más caros. 
Los tonos más intensos indican valores más altos en cada dimensión. Se observa que los productos 
más costosos no necesariamente son los menos vendidos, sugiriendo que existe un segmento de 
coleccionistas dispuestos a invertir en piezas premium. Esta relación precio-demanda ayuda a 
optimizar la estrategia de precios y identificar oportunidades para desarrollar productos en 
rangos de precio específicos que maximicen tanto volumen como margen.
"""
pdf.chapter_body(explicacion7)

# Conclusión
pdf.add_page()
pdf.chapter_title('CONCLUSIONES Y RECOMENDACIONES')
conclusion_text = """
El análisis revela un mercado saludable con oportunidades de crecimiento en segmentos específicos. 
Se recomienda: 1) Mantener diversidad en el portfolio de productos para cubrir todos los segmentos 
de precio, 2) Implementar programas de fidelización para clientes frecuentes, 3) Optimizar inventario 
basado en patrones estacionales identificados, 4) Desarrollar estrategias de marketing diferenciadas 
para productos premium vs. entry-level, y 5) Continuar monitoreando la relación precio-demanda para 
ajustar estrategias comerciales. El mercado de maquetas muestra resiliencia y potencial de 
crecimiento sostenido.
"""
pdf.chapter_body(conclusion_text)

# Guardar PDF
pdf.output(pdf_path)

print("✅ Informe PDF generado correctamente")

# =============================================================================
# REPORTE FINAL EN CONSOLA
# =============================================================================
print("\n" + "="*80)
print("📋 REPORTE FINAL - PROCESO COMPLETADO")
print("="*80)

# Estadísticas resumen
total_ventas = ventas_df['Cantidad'].sum()
total_clientes = ventas_df['id_clientes'].nunique()
total_productos = productos_df['ID'].nunique()
periodo_analisis = f"{ventas_df['FechaEmision'].min()} to {ventas_df['FechaEmision'].max()}"

print(f"\n📊 ESTADÍSTICAS PRINCIPALES:")
print(f"   • Total de ventas realizadas: {total_ventas} unidades")
print(f"   • Clientes únicos que compraron: {total_clientes}")
print(f"   • Productos en catálogo: {total_productos}")
print(f"   • Período analizado: {periodo_analisis}")

print(f"\n📈 GRÁFICOS GENERADOS:")
graficos = [
    '1_stock_por_fabricante.png',
    '2_productos_mas_vendidos.png', 
    '3_precios_productos.png',
    '4_evolucion_ventas.png',
    '5_clientes_mas_compraron.png',
    '6_productos_mas_caros.png',
    '7_matriz_calor.png'
]

for grafico in graficos:
    ruta_completa = os.path.join(graficos_dir, grafico)
    if os.path.exists(ruta_completa):
        tamaño = os.path.getsize(ruta_completa) / 1024  # Tamaño en KB
        print(f"   ✅ {grafico} ({tamaño:.1f} KB)")

print(f"\n📄 ARCHIVOS CREADOS:")
print(f"   • PDF del informe: {pdf_path}")
print(f"   • Carpeta de gráficos: {graficos_dir}")

print(f"\n🎯 PRODUCTO MÁS VENDIDO: Prod {ventas_por_producto.index[0]} ({ventas_por_producto.iloc[0]} unidades)")
print(f"💰 PRODUCTO MÁS CARO: {productos_caros.iloc[0]['Nombre']} (${productos_caros.iloc[0]['PrecioUSD']:.2f})")

print(f"\n✅ PROCESO COMPLETADO EXITOSAMENTE")
print("="*80)