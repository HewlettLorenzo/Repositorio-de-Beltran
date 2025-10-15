import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

# ----------------------------- CONFIGURACIÓN GENERAL -----------------------------

st.set_page_config(
    page_title="Detector de Grooming con IA",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Detector de Mensajes de Grooming")
st.caption("Analizá mensajes o conversaciones completas con Inteligencia Artificial para detectar posibles riesgos de grooming.")

# ----------------------------- FUNCIÓN DE ENTRENAMIENTO DEL MODELO -----------------------------

@st.cache_resource
def entrenar_modelo():
    """
    Entrena un modelo Naive Bayes usando TF-IDF y devuelve el vectorizador y el modelo.
    """
    mensajes = [
        "¿Cuántos años tenés? No le digas a nadie que hablamos",
        "Hola, ¿cómo estás? ¿Querés jugar algo online?",
        "Sos muy linda, no le muestres esto a tus papás.",
        "¿Terminaste la tarea de matemáticas?",
        "Podés mandarme una foto tuya, pero que sea solo para mi.",
        "¿Querés que te ayude con el juego que no podías pasar?",
        "No le contés a nadie que hablamos por acá, ¿si?",
        "¿Te gustó la película de ayer?",
        "¿Estás solo en casa ahora?",
        "¿Querés hacer una videollamada para estudiar juntos?",
        "No le digas a tus padres que te escribí, es nuestro secreto.",
        "¿Cómo te fue en el examen de historia?",
        "Mandame una foto tuya, pero que nadie más la vea.",
        "¿Jugamos Minecraft esta tarde?",
        "Sos muy especial para mí, no le cuentes a nadie lo que hablamos.",
        "¿Querés que te pase los apuntes de biología?",
        "¿Podés mostrarme cómo estás vestida ahora?",
        "¿Tenés ganas de salir a andar en bici mañana?",
        "No hace falta que le digas a nadie que hablamos tanto.",
        "¿Querés que estudiemos juntos para el parcial?"
    ]

    etiquetas = [
        "grooming", "no grooming", "grooming", "no grooming", "grooming",
        "no grooming", "grooming", "no grooming", "grooming", "no grooming",
        "grooming", "no grooming", "grooming", "no grooming", "grooming",
        "no grooming", "grooming", "no grooming", "grooming", "no grooming"
    ]

    vectorizador = TfidfVectorizer()
    X = vectorizador.fit_transform(mensajes)

    modelo = MultinomialNB()
    modelo.fit(X, etiquetas)

    return vectorizador, modelo

# ----------------------------- CARGA DEL MODELO ENTRENADO -----------------------------

vec, model = entrenar_modelo()

# ----------------------------- OPCIONES DE ANÁLISIS -----------------------------

opcion = st.radio(
    "Seleccioná el modo de análisis:",
    ["💬 Analizar un mensaje", "📂 Analizar una conversación completa"]
)

# ----------------------------- MODO 1: ANÁLISIS DE UN MENSAJE -----------------------------

if opcion == "💬 Analizar un mensaje":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial del chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada del usuario
    if prompt := st.chat_input("Escribí un mensaje para analizar..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Vectorizar y predecir
        X_input = vec.transform([prompt])
        prediccion = model.predict(X_input)[0]
        probas = model.predict_proba(X_input)[0]
        grooming_prob = probas[list(model.classes_).index("grooming")]

        with st.chat_message("assistant"):
            st.markdown("### Resultado del análisis")
            st.progress(float(grooming_prob))
            st.write(f"**Probabilidad de grooming:** {grooming_prob*100:.1f}%")

            if prediccion == "grooming":
                st.warning("🚨 Este mensaje presenta características asociadas al grooming.", icon="⚠️")
                respuesta = "🚨 Este mensaje presenta características asociadas al grooming."
            else:
                st.success("✅ El mensaje parece seguro. No se detectaron indicios de grooming.", icon="👍")
                respuesta = "✅ El mensaje parece seguro."

            # Recursos útiles
            st.markdown("""
                ---
                🔗 **Recursos de ayuda:**
                - [Línea 102 - Argentina](https://www.argentina.gob.ar/linea-102): atención gratuita y confidencial para niñas, niños y adolescentes.
                - [Guía sobre Grooming del Ministerio de Seguridad](https://www.argentina.gob.ar/seguridad/grooming)
            """)

        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# ----------------------------- MODO 2: ANÁLISIS DE CONVERSACIÓN COMPLETA -----------------------------

elif opcion == "📂 Analizar una conversación completa":
    st.info("Podés subir un archivo `.txt` o `.csv` con los mensajes. El sistema analizará línea por línea.", icon="💡")
    archivo = st.file_uploader("Subí una conversación", type=["txt", "csv"])

    if archivo:
        # Cargar y preparar los datos
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
            if "mensaje" not in df.columns:
                st.error("El archivo CSV debe tener una columna llamada 'mensaje'.")
            else:
                mensajes = df["mensaje"].astype(str).tolist()
        else:
            mensajes = archivo.read().decode("utf-8").splitlines()

        if mensajes:
            X_input = vec.transform(mensajes)
            predicciones = model.predict(X_input)
            probas = model.predict_proba(X_input)

            resultados = pd.DataFrame({
                "Mensaje": mensajes,
                "Predicción": predicciones,
                "Probabilidad Grooming": [p[list(model.classes_).index("grooming")] for p in probas]
            })

            st.subheader("📊 Resultados del análisis")
            st.dataframe(resultados, use_container_width=True)

            # Conteo general
            total = len(resultados)
            grooming_count = sum(resultados["Predicción"] == "grooming")
            st.write(f"**Mensajes analizados:** {total}")
            st.write(f"**Posibles grooming detectados:** {grooming_count}")

            st.progress(grooming_count / total)

            st.markdown("""
                ---
                🔗 **Recursos de ayuda:**
                - [Línea 102 - Argentina](https://www.argentina.gob.ar/linea-102)
                - [Campaña nacional contra el grooming](https://www.argentina.gob.ar/seguridad/grooming)
            """)

# Trabajo hecho por: Gil Lascano Lorenzo, Bayaslian Santiago, Buchholz Ariel, Núñez Mauro. 