import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from fpdf import FPDF
import os
from datetime import datetime
import matplotlib.dates as mdates
from pathlib import Path

# -------------------------------
# Configuración de directorios
# -------------------------------
base_dir = Path(r"D:\Beltrán\Segundo año TS CD e IA\Modelizado de Minería de Datos\TSCIA_MMD\Proyecto_4\DataCSV")
data_dir = base_dir
graficos_dir = base_dir / "graficos"
pdf_path = base_dir / "informe_maquetas_trenes.pdf"

graficos_dir.mkdir(parents=True, exist_ok=True)

print("🔧 Iniciando proceso de carga de CSV...")

# -------------------------------
# Lectura de archivos CSV
# -------------------------------
try:
    productos_df = pd.read_csv(data_dir / "producto_trenes.csv", sep=';', encoding='utf-8')
    fabricantes_df = pd.read_csv(data_dir / "fabricantes.csv", sep=';', encoding='utf-8')
    clientes_df = pd.read_csv(data_dir / "clientes.csv", sep=';', encoding='utf-8')
    ventas_df = pd.read_csv(data_dir / "facturas.csv", sep=';', encoding='utf-8')

    # Renombrar columnas ID para evitar conflictos
    productos_df = productos_df.rename(columns={'ID':'producto_ID'})
    fabricantes_df = fabricantes_df.rename(columns={'ID':'fabricante_ID'})
    clientes_df = clientes_df.rename(columns={'ID':'cliente_ID'})

    print("✅ Archivos CSV leídos y columnas renombradas correctamente")

except Exception as e:
    print(f"❌ Error leyendo archivos CSV: {e}")
    exit()

# -------------------------------
# Merge de los datos
# -------------------------------
ventas_completas_df = ventas_df.merge(productos_df, left_on='id_producto', right_on='producto_ID', how='left')
ventas_completas_df = ventas_completas_df.merge(fabricantes_df, left_on='id_fabricante_maqueta', right_on='fabricante_ID', how='left')
ventas_completas_df = ventas_completas_df.merge(clientes_df, left_on='id_clientes', right_on='cliente_ID', how='left')

ventas_completas_df['FechaEmision'] = pd.to_datetime(ventas_completas_df['FechaEmision'])

print("✅ Merge de datos completado correctamente")
print("📊 Generando gráficos...")

# -------------------------------
# 1. Stock por fabricante
# -------------------------------
plt.figure(figsize=(10, 8))
stock_por_fabricante = productos_df.groupby('id_fabricante_maqueta')['CantStockActual'].sum()
fabricantes_nombres = fabricantes_df.set_index('fabricante_ID').loc[stock_por_fabricante.index]['Fabricante']

colors_pie = ['#FF6B6B', '#4ECDC4', '#FFE66D']
plt.pie(stock_por_fabricante.values, labels=fabricantes_nombres.values, autopct='%1.1f%%', colors=colors_pie, startangle=90)
plt.title('Distribución de Stock Actual por Fabricante', fontsize=14, fontweight='bold')
plt.savefig(os.path.join(graficos_dir, '1_stock_por_fabricante.png'), dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# 2. Productos más vendidos
# -------------------------------
plt.figure(figsize=(12, 8))
ventas_por_producto = ventas_df.groupby('id_producto')['Cantidad'].sum().sort_values(ascending=False)
productos_nombres = productos_df.set_index('producto_ID').loc[ventas_por_producto.index]['Nombre']

bars = plt.bar(range(len(ventas_por_producto)), ventas_por_producto.values, color='#2E8B57', alpha=0.8)
plt.xlabel('Productos')
plt.ylabel('Cantidad Vendida')
plt.title('Productos Más Vendidos', fontsize=14, fontweight='bold')
plt.xticks(range(len(ventas_por_producto)), [f"Prod {i}" for i in ventas_por_producto.index], rotation=45)

for bar, valor in zip(bars, ventas_por_producto.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, str(valor), ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '2_productos_mas_vendidos.png'), dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# 3. Precios de productos
# -------------------------------
plt.figure(figsize=(12, 8))
productos_ordenados = productos_df.sort_values('PrecioUSD', ascending=False)
bars = plt.bar(range(len(productos_ordenados)), productos_ordenados['PrecioUSD'], color='#87CEEB', alpha=0.8)
plt.xlabel('Productos')
plt.ylabel('Precio (USD)')
plt.title('Precios de los Productos', fontsize=14, fontweight='bold')
plt.xticks(range(len(productos_ordenados)), [f"Prod {i}" for i in productos_ordenados['producto_ID']], rotation=45)

for bar, precio in zip(bars, productos_ordenados['PrecioUSD']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, f"${precio:.2f}", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '3_precios_productos.png'), dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# 4. Evolución de ventas
# -------------------------------
plt.figure(figsize=(14, 8))
ventas_por_mes = ventas_completas_df.groupby(ventas_completas_df['FechaEmision'].dt.to_period('M')).size()
ventas_por_mes.index = ventas_por_mes.index.to_timestamp()

plt.plot(ventas_por_mes.index, ventas_por_mes.values, color='#FF4444', linewidth=2.5, marker='o')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de Ventas')
plt.title('Evolución de Ventas Mensuales (2023-2025)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gcf().autofmt_xdate()

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '4_evolucion_ventas.png'), dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# 5. Clientes que más compraron
# -------------------------------
plt.figure(figsize=(12, 10))
compras_por_cliente = ventas_df.groupby('id_clientes')['Cantidad'].sum().sort_values(ascending=True).tail(15)
clientes_nombres = clientes_df.set_index('cliente_ID').loc[compras_por_cliente.index]['Nombre']

bars = plt.barh(range(len(compras_por_cliente)), compras_por_cliente.values, color='#32CD32', alpha=0.8)
plt.ylabel('Clientes')
plt.xlabel('Cantidad Total Comprada')
plt.title('Top 15 - Clientes que Más Compraron', fontsize=14, fontweight='bold')
plt.yticks(range(len(compras_por_cliente)), clientes_nombres.values)

for bar, valor in zip(bars, compras_por_cliente.values):
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, str(valor), ha='left', va='center')

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '5_clientes_mas_compraron.png'), dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# 6. Productos más caros
# -------------------------------
plt.figure(figsize=(12, 8))
productos_caros = productos_df.nlargest(8, 'PrecioUSD')
bars = plt.bar(range(len(productos_caros)), productos_caros['PrecioUSD'], color='#FFD700', alpha=0.8)
plt.xlabel('Productos')
plt.ylabel('Precio (USD)')
plt.title('Productos Más Caros', fontsize=14, fontweight='bold')
plt.xticks(range(len(productos_caros)), [f"{row['Nombre'][:15]}..." for _, row in productos_caros.iterrows()], rotation=45, ha='right')

for bar, precio in zip(bars, productos_caros['PrecioUSD']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f"${precio:.2f}", ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '6_productos_mas_caros.png'), dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# 7. Matriz de calor
# -------------------------------
plt.figure(figsize=(12, 8))
top_productos = productos_df.nlargest(5, 'PrecioUSD')
matriz_data = []
for _, producto in top_productos.iterrows():
    cantidad_vendida = ventas_df[ventas_df['id_producto'] == producto['producto_ID']]['Cantidad'].sum()
    matriz_data.append([producto['PrecioUSD'], cantidad_vendida])

matriz_data = np.array(matriz_data).T
sns.heatmap(matriz_data, annot=True, fmt='.1f', cmap='YlOrRd',
            xticklabels=[f"Prod {i}" for i in top_productos['producto_ID']],
            yticklabels=['Precio (USD)', 'Cantidad Vendida'])
plt.title('Matriz de Calor: Precio vs Cantidad Vendida (Top 5 Productos Más Caros)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '7_matriz_calor.png'), dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# Generación del PDF
# -------------------------------
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

pdf = PDFReport()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# -------------------------------
# Introducción
# -------------------------------
pdf.chapter_title('INTRODUCCIÓN')
intro_text = """
Este informe presenta un análisis completo de las ventas de maquetas de trenes para el período 
2023-2025. El análisis incluye distribución de stock, comportamiento de ventas, perfil de clientes 
y relación entre precio y demanda. Los datos fueron procesados mediante técnicas de minería de datos 
y visualización para extraer insights estratégicos que permitan optimizar el inventario y las 
estrategias de marketing.
"""
pdf.chapter_body(intro_text)

# -------------------------------
# Agregar gráficos y explicaciones
# -------------------------------
graficos = [
    ('1. DISTRIBUCIÓN DE STOCK POR FABRICANTE', '1_stock_por_fabricante.png', 
     "El gráfico circular muestra la distribución del stock actual entre los principales fabricantes. "
     "Märklin lidera con el mayor porcentaje, seguido por Hornby y Bachmann. Esto permite identificar "
     "qué fabricantes requieren ajustes de inventario."),
    ('2. PRODUCTOS MÁS VENDIDOS', '2_productos_mas_vendidos.png', 
     "Este gráfico de barras representa los productos más vendidos en el período 2023-2025. "
     "Se observa que los productos de la serie X son los más populares."),
    ('3. PRECIOS DE LOS PRODUCTOS', '3_precios_productos.png', 
     "Se muestra la variación de precios de todos los productos. Los productos de gama premium destacan "
     "con precios significativamente más altos."),
    ('4. EVOLUCIÓN DE VENTAS MENSUALES', '4_evolucion_ventas.png', 
     "El gráfico de líneas indica cómo evolucionaron las ventas mes a mes, permitiendo detectar picos "
     "y caídas estacionales."),
    ('5. CLIENTES QUE MÁS COMPRARON', '5_clientes_mas_compraron.png', 
     "Top 15 clientes que realizaron mayores compras. Identificar clientes clave ayuda a estrategias "
     "de fidelización."),
    ('6. PRODUCTOS MÁS CAROS', '6_productos_mas_caros.png', 
     "Los productos más caros del inventario. Su análisis permite definir márgenes y estrategias de venta."),
    ('7. MATRIZ DE CALOR: PRECIO VS CANTIDAD VENDIDA', '7_matriz_calor.png', 
     "La matriz muestra la relación entre precio y cantidad vendida de los productos más caros. "
     "Ayuda a detectar la elasticidad de la demanda."),
]

for titulo, archivo, descripcion in graficos:
    pdf.add_page()
    pdf.chapter_title(titulo)
    pdf.image(os.path.join(graficos_dir, archivo), x=10, w=190)
    pdf.chapter_body(descripcion)

# -------------------------------
# Conclusión
# -------------------------------
pdf.add_page()
pdf.chapter_title('CONCLUSIONES')
conclusion_text = """
El análisis integral de ventas permite varias conclusiones clave:
- Identificación de los fabricantes con mayor stock y necesidad de rotación.
- Reconocimiento de los productos más vendidos y estrategias de reposición.
- Comprensión de la evolución temporal de las ventas y detección de patrones estacionales.
- Identificación de clientes estratégicos y oportunidades de fidelización.
- Relación precio-demanda para optimizar precios y márgenes de productos premium.

Este informe constituye una herramienta útil para la toma de decisiones estratégicas en la gestión
de inventario y comercialización de maquetas de trenes.
"""
pdf.chapter_body(conclusion_text)

# -------------------------------
# Guardar PDF
# -------------------------------
pdf.output(pdf_path)
print(f"✅ Informe PDF generado correctamente en {pdf_path}")
