# proyecto_final.py
# ANÁLISIS DE RECOMPRA - CÓDIGO UNIFICADO CON DATOS DEL ANEXO

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, roc_auc_score, confusion_matrix, classification_report)
import os
from datetime import datetime

# ============================================================
# 1. DATOS DEL ANEXO (20 REGISTROS)
# ============================================================

print("=" * 60)
print("CARGANDO DATOS DEL ANEXO...")
print("=" * 60)

data_anexo = {
    "Cliente_ID": list(range(1, 21)),
    "Genero": ["F", "M"] * 10,
    "Edad": [23, 34, 45, 29, 31, 38, 27, 50, 40, 36,
             25, 33, 46, 28, 39, 42, 30, 48, 35, 37],
    "Recibio_Promo": ["Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí", "No", "Sí",
                      "No", "Sí", "Sí", "No", "No", "Sí", "No", "Sí", "No", "Sí"],
    "Monto_Promocion": [500, 0, 700, 300, 0, 600, 0, 800, 0, 450,
                        0, 620, 710, 0, 0, 480, 0, 750, 0, 520],
    "Recompra": ["Sí", "No", "Sí", "No", "No", "Sí", "No", "Sí", "No", "Sí",
                 "No", "No", "Sí", "No", "No", "Sí", "No", "Sí", "No", "Sí"],
    "Total_Compras": [2, 1, 3, 1, 1, 4, 1, 5, 1, 3,
                      1, 2, 4, 1, 1, 3, 1, 5, 1, 3],
    "Ingreso_Mensual": [30000, 45000, 40000, 28000, 32000, 50000, 31000, 60000,
                        29000, 37000, 31000, 34000, 47000, 30000, 29000, 43000,
                        33000, 55000, 30000, 41000]
}

df = pd.DataFrame(data_anexo)

print(f"Datos cargados: {len(df)} registros")
print(f"Columnas: {list(df.columns)}")
print("\nPrimeras 5 filas:")
print(df.head())

# ============================================================
# 2. GUARDAR DATOS EN EXCEL
# ============================================================

print("\n" + "=" * 60)
print("GUARDANDO DATOS EN EXCEL...")
print("=" * 60)

# Crear carpeta si no existe
os.makedirs("proyecto_final", exist_ok=True)
os.makedirs("proyecto_final/graficos", exist_ok=True)

# Guardar Excel
excel_path = "proyecto_final/datos_clientes.xlsx"
df.to_excel(excel_path, index=False)
print(f"✓ Excel guardado: {excel_path}")

# ============================================================
# 3. PREPROCESAMIENTO
# ============================================================

print("\n" + "=" * 60)
print("PREPROCESANDO DATOS...")
print("=" * 60)

# Mapear variables categóricas a numéricas
df_processed = df.copy()
df_processed["Genero_num"] = df_processed["Genero"].map({"F": 0, "M": 1})
df_processed["Recibio_Promo_num"] = df_processed["Recibio_Promo"].map({"No": 0, "Sí": 1})
df_processed["Recompra_num"] = df_processed["Recompra"].map({"No": 0, "Sí": 1})

print("✓ Variables categóricas mapeadas a numéricas")
print(f"Distribución de Recompra: {df_processed['Recompra_num'].value_counts().to_dict()}")

# ============================================================
# 4. ANÁLISIS EXPLORATORIO Y GRÁFICOS
# ============================================================

print("\n" + "=" * 60)
print("GENERANDO GRÁFICOS...")
print("=" * 60)

# Configurar estilo de gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# 4.1 Distribución de Edad
plt.figure(figsize=(10, 6))
plt.hist(df["Edad"], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
plt.title("Distribución de Edad de Clientes", fontsize=16, fontweight='bold')
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("proyecto_final/graficos/distribucion_edad.png", dpi=300, bbox_inches='tight')
plt.show()

# 4.2 Recompra vs Monto de Promoción
plt.figure(figsize=(10, 6))
promedio_monto = df.groupby("Recompra")["Monto_Promocion"].mean()
plt.bar(promedio_monto.index, promedio_monto.values, color=['#ff6b6b', '#51cf66'])
plt.title("Monto Promocional Promedio por Recompra", fontsize=16, fontweight='bold')
plt.xlabel("Recompra")
plt.ylabel("Monto Promocional Promedio ($)")
plt.grid(True, alpha=0.3)
for i, v in enumerate(promedio_monto.values):
    plt.text(i, v + 10, f"${v:.0f}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig("proyecto_final/graficos/recompra_vs_monto.png", dpi=300, bbox_inches='tight')
plt.show()

# 4.3 Distribución por Género
plt.figure(figsize=(8, 6))
conteo_genero = df["Genero"].value_counts()
colores = ['#ff6fa3', '#4d79ff']
plt.pie(conteo_genero.values, labels=conteo_genero.index, autopct='%1.1f%%', 
        colors=colores, startangle=90)
plt.title("Distribución por Género", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("proyecto_final/graficos/distribucion_genero.png", dpi=300, bbox_inches='tight')
plt.show()

# 4.4 Ingreso Mensual vs Recompra
plt.figure(figsize=(10, 6))
sns.boxplot(x='Recompra', y='Ingreso_Mensual', data=df, palette=['#ff6b6b', '#51cf66'])
plt.title("Distribución de Ingreso Mensual por Recompra", fontsize=16, fontweight='bold')
plt.xlabel("Recompra")
plt.ylabel("Ingreso Mensual ($)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("proyecto_final/graficos/ingreso_vs_recompra.png", dpi=300, bbox_inches='tight')
plt.show()

# 4.5 Total de Compras vs Recompra
plt.figure(figsize=(10, 6))
promedio_compras = df.groupby("Recompra")["Total_Compras"].mean()
plt.bar(promedio_compras.index, promedio_compras.values, color=['#ff6b6b', '#51cf66'])
plt.title("Total de Compras Promedio por Recompra", fontsize=16, fontweight='bold')
plt.xlabel("Recompra")
plt.ylabel("Total de Compras Promedio")
plt.grid(True, alpha=0.3)
for i, v in enumerate(promedio_compras.values):
    plt.text(i, v + 0.1, f"{v:.1f}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig("proyecto_final/graficos/compras_vs_recompra.png", dpi=300, bbox_inches='tight')
plt.show()

print("✓ Gráficos generados y guardados")

# ============================================================
# 5. MODELADO PREDICTIVO
# ============================================================

print("\n" + "=" * 60)
print("ENTRENANDO MODELO PREDICTIVO...")
print("=" * 60)

# Preparar datos para el modelo
X = df_processed[["Genero_num", "Edad", "Recibio_Promo_num", "Monto_Promocion", "Total_Compras", "Ingreso_Mensual"]]
y = df_processed["Recompra_num"]

# Dividir en entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Entrenar modelo de árbol de decisión
clf = DecisionTreeClassifier(max_depth=4, random_state=42)  # Reducida profundidad por datos limitados
clf.fit(X_train, y_train)

# Predicciones
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]

# Métricas del modelo
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)

print("✓ Modelo entrenado")
print(f"Tamaño entrenamiento: {len(X_train)} registros")
print(f"Tamaño prueba: {len(X_test)} registros")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC AUC: {roc_auc:.4f}")

# ============================================================
# 6. GRÁFICO DEL ÁRBOL DE DECISIÓN (PRIMORDIAL)
# ============================================================

print("\n" + "=" * 60)
print("GENERANDO GRÁFICO DEL ÁRBOL DE DECISIÓN...")
print("=" * 60)

plt.figure(figsize=(16, 10))
plot_tree(clf, 
          feature_names=X.columns, 
          class_names=["No Recompra", "Sí Recompra"], 
          filled=True, 
          rounded=True,
          fontsize=10,
          proportion=True)
plt.title("Árbol de Decisión - Predicción de Recompra", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("proyecto_final/graficos/arbol_decision.png", dpi=300, bbox_inches='tight')
plt.show()

print("✓ Árbol de decisión generado y guardado")

# ============================================================
# 7. MATRIZ DE CONFUSIÓN
# ============================================================

plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Recompra', 'Sí Recompra'], 
            yticklabels=['No Recompra', 'Sí Recompra'])
plt.title('Matriz de Confusión', fontsize=16, fontweight='bold')
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.tight_layout()
plt.savefig("proyecto_final/graficos/matriz_confusion.png", dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# 8. IMPORTANCIA DE VARIABLES
# ============================================================

importancias = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=True)

plt.figure(figsize=(10, 6))
importancias.plot(kind='barh', color='steelblue')
plt.title('Importancia de Variables en el Modelo', fontsize=16, fontweight='bold')
plt.xlabel('Importancia')
plt.tight_layout()
plt.savefig("proyecto_final/graficos/importancia_variables.png", dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# 9. GENERACIÓN DEL INFORME PDF
# ============================================================

print("\n" + "=" * 60)
print("GENERANDO INFORME PDF...")
print("=" * 60)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Configurar fuente Times New Roman
try:
    # En Windows
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'C:/Windows/Fonts/times.ttf'))
    font_name = 'TimesNewRoman'
except:
    try:
        # En Linux
        pdfmetrics.registerFont(TTFont('TimesNewRoman', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'))
        font_name = 'TimesNewRoman'
    except:
        font_name = 'Helvetica'  # Fallback
        print("⚠️ Times New Roman no encontrada, usando Helvetica")

# Crear estilos personalizados
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='TituloPrincipal',
    parent=styles['Heading1'],
    fontName=font_name,
    fontSize=16,
    spaceAfter=12,
    alignment=1  # Centrado
))
styles.add(ParagraphStyle(
    name='Subtitulo',
    parent=styles['Heading2'],
    fontName=font_name,
    fontSize=14,
    spaceAfter=12,
    spaceBefore=12
))
styles.add(ParagraphStyle(
    name='Cuerpo',
    parent=styles['Normal'],
    fontName=font_name,
    fontSize=10,
    leading=15,  # Interlineado 1.5
    spaceAfter=6
))

# Crear el documento PDF
pdf_path = "proyecto_final/informe_recompra.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)

# Contenido del informe
contenido = []

# Título principal
titulo_principal = Paragraph("INFORME DE ANÁLISIS DE RECOMPRA", styles['TituloPrincipal'])
contenido.append(titulo_principal)
contenido.append(Spacer(1, 20))

# 1. INTRODUCCIÓN
subtitulo1 = Paragraph("1. INTRODUCCIÓN", styles['Subtitulo'])
contenido.append(subtitulo1)
intro_texto = Paragraph(
    "Este informe presenta el análisis predictivo del comportamiento de recompra de 20 clientes "
    "basado en variables demográficas y de comportamiento. El modelo de árbol de decisión "
    "se utilizó para predecir la probabilidad de que un cliente realice una recompra después "
    "de recibir una promoción.", 
    styles['Cuerpo']
)
contenido.append(intro_texto)
contenido.append(Spacer(1, 12))

# 2. RESUMEN DEL DATASET
subtitulo2 = Paragraph("2. RESUMEN DEL DATASET", styles['Subtitulo'])
contenido.append(subtitulo2)

resumen_datos = [
    ["Total de clientes", "20"],
    ["Clientes que recompraron", "10 (50%)"],
    ["Clientes que recibieron promoción", "12 (60%)"],
    ["Edad promedio", f"{df['Edad'].mean():.1f} años"],
    ["Ingreso mensual promedio", f"${df['Ingreso_Mensual'].mean():,.0f}"],
    ["Monto promedio de promoción", f"${df['Monto_Promocion'].mean():,.0f}"],
]

tabla_resumen = Table(resumen_datos, colWidths=[3*inch, 2*inch])
tabla_resumen.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
contenido.append(tabla_resumen)
contenido.append(Spacer(1, 12))

# 3. RESULTADOS DEL MODELO
subtitulo3 = Paragraph("3. RESULTADOS DEL MODELO PREDICTIVO", styles['Subtitulo'])
contenido.append(subtitulo3)

metricas_modelo = [
    ["Métrica", "Valor"],
    ["Accuracy (Exactitud)", f"{accuracy:.4f}"],
    ["Precision", f"{precision:.4f}"],
    ["Recall (Sensibilidad)", f"{recall:.4f}"],
    ["F1-Score", f"{f1:.4f}"],
    ["ROC AUC", f"{roc_auc:.4f}"]
]

tabla_metricas = Table(metricas_modelo, colWidths=[2*inch, 1.5*inch])
tabla_metricas.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
contenido.append(tabla_metricas)
contenido.append(Spacer(1, 12))

# 4. IMPORTANCIA DE VARIABLES
subtitulo4 = Paragraph("4. IMPORTANCIA DE VARIABLES", styles['Subtitulo'])
contenido.append(subtitulo4)

importancia_texto = Paragraph(
    "El análisis de importancia de variables revela qué factores tienen mayor influencia "
    "en la predicción de recompra. Las variables más importantes son:",
    styles['Cuerpo']
)
contenido.append(importancia_texto)
contenido.append(Spacer(1, 6))

# Tabla de importancia de variables
datos_importancia = [["Variable", "Importancia"]]
for var, imp in importancias.items():
    datos_importancia.append([var, f"{imp:.4f}"])

tabla_importancia = Table(datos_importancia, colWidths=[3*inch, 1.5*inch])
tabla_importancia.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
contenido.append(tabla_importancia)
contenido.append(Spacer(1, 12))

# 5. GRÁFICOS
subtitulo5 = Paragraph("5. VISUALIZACIONES", styles['Subtitulo'])
contenido.append(subtitulo5)

# Agregar gráficos al PDF
graficos = [
    ("proyecto_final/graficos/distribucion_edad.png", "Distribución de Edad de Clientes"),
    ("proyecto_final/graficos/recompra_vs_monto.png", "Monto Promocional vs Recompra"),
    ("proyecto_final/graficos/distribucion_genero.png", "Distribución por Género"),
    ("proyecto_final/graficos/ingreso_vs_recompra.png", "Ingreso Mensual vs Recompra"),
    ("proyecto_final/graficos/compras_vs_recompra.png", "Total de Compras vs Recompra"),
    ("proyecto_final/graficos/importancia_variables.png", "Importancia de Variables"),
    ("proyecto_final/graficos/matriz_confusion.png", "Matriz de Confusión"),
]

for ruta_grafico, titulo_grafico in graficos:
    if os.path.exists(ruta_grafico):
        # Título del gráfico
        titulo_graph = Paragraph(titulo_grafico, styles['Cuerpo'])
        contenido.append(titulo_graph)
        
        # Imagen del gráfico
        img = Image(ruta_grafico, width=6*inch, height=4*inch)
        contenido.append(img)
        contenido.append(Spacer(1, 12))

# 6. ÁRBOL DE DECISIÓN
contenido.append(Spacer(1, 12))
subtitulo6 = Paragraph("6. ÁRBOL DE DECISIÓN", styles['Subtitulo'])
contenido.append(subtitulo6)

arbol_texto = Paragraph(
    "El árbol de decisión muestra las reglas de clasificación utilizadas por el modelo "
    "para predecir la recompra. Cada nodo representa una decisión basada en una variable, "
    "y las hojas representan las predicciones finales.",
    styles['Cuerpo']
)
contenido.append(arbol_texto)

# Incluir el árbol de decisión (versión más pequeña)
if os.path.exists("proyecto_final/graficos/arbol_decision.png"):
    titulo_arbol = Paragraph("Árbol de Decisión - Modelo Predictivo", styles['Cuerpo'])
    contenido.append(titulo_arbol)
    arbol_img = Image("proyecto_final/graficos/arbol_decision.png", width=6*inch, height=4*inch)
    contenido.append(arbol_img)

# 7. CONCLUSIONES
contenido.append(Spacer(1, 12))
subtitulo7 = Paragraph("7. CONCLUSIONES", styles['Subtitulo'])
contenido.append(subtitulo7)

conclusiones = Paragraph(
    f"El modelo de árbol de decisión demostró ser efectivo para predecir el comportamiento "
    f"de recompra con una exactitud del {accuracy*100:.1f}%. Las variables más importantes para la "
    f"predicción fueron {importancias.index[-1]} y {importancias.index[-2]}. "
    f"Este análisis puede ser utilizado para optimizar estrategias de marketing "
    f"y promociones dirigidas.",
    styles['Cuerpo']
)
contenido.append(conclusiones)

# Generar el PDF
doc.build(contenido)
print(f"✓ Informe PDF generado: {pdf_path}")

# ============================================================
# 10. RESUMEN FINAL
# ============================================================

print("\n" + "=" * 60)
print("PROYECTO FINALIZADO EXITOSAMENTE!")
print("=" * 60)

print("\n📁 ARCHIVOS GENERADOS:")
print(f"  ✓ Excel con datos: proyecto_final/datos_clientes.xlsx")
print(f"  ✓ Informe PDF: proyecto_final/informe_recompra.pdf")
print(f"  ✓ Dashboard: proyecto_final/dashboard_streamlit.py")
print(f"  ✓ Gráficos: proyecto_final/graficos/")

print("\n📊 GRÁFICOS INCLUIDOS:")
print("  ✓ Distribución de edad")
print("  ✓ Recompra vs monto de promoción") 
print("  ✓ Distribución por género")
print("  ✓ Ingreso mensual vs recompra")
print("  ✓ Total de compras vs recompra")
print("  ✓ Importancia de variables")
print("  ✓ Matriz de confusión")
print("  ✓ Árbol de decisión (PRIMORDIAL)")

print("\n📈 ESTADÍSTICAS DEL DATASET:")
print(f"  ✓ Total clientes: {len(df)}")
print(f"  ✓ Recompraron: {(df['Recompra'] == 'Sí').sum()} ({(df['Recompra'] == 'Sí').mean()*100:.1f}%)")
print(f"  ✓ Recibieron promoción: {(df['Recibio_Promo'] == 'Sí').sum()} ({(df['Recibio_Promo'] == 'Sí').mean()*100:.1f}%)")
print(f"  ✓ Edad promedio: {df['Edad'].mean():.1f} años")
print(f"  ✓ Ingreso promedio: ${df['Ingreso_Mensual'].mean():,.0f}")

print("\n🚀 PARA EJECUTAR EL DASHBOARD:")
print("  streamlit run proyecto_final/dashboard_streamlit.py")

print("\n" + "=" * 60)