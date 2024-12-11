#%%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import numpy as np

# Configuración general
st.set_page_config(page_title="Dashboard de Sesiones Psicológicas", layout="wide")

@st.cache_data
def load_data():
    # Cargar datos desde el archivo CSV
    data = pd.read_csv("Patient.csv")
    return data

data = load_data()

# Título
st.title("Dashboard de Sesiones Psicológicas")
st.markdown("**Optimización del impacto del programa para Mujer Violeta**")

# Sección 1: Resumen general
st.header("Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Sesiones", len(data))
col2.metric("Pacientes Únicos", data['Nombre del Paciente'].nunique())
col3.metric("Estados Únicos", data['Estado'].nunique())

# Sección 2: Clústeres Interactivos
# Sección 3: Visualización de Clústeres Temáticos
st.header("Visualización de Clústeres Temáticos")

# Descargar stopwords de NLTK si es necesario
nltk.download('stopwords')
spanish_stopwords = stopwords.words('spanish')

# Vectorizar el texto de los resúmenes
vectorizer = TfidfVectorizer(stop_words=spanish_stopwords)
X_tfidf = vectorizer.fit_transform(data["Resumen"])

# Aplicar t-SNE para la reducción de dimensionalidad
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=500)
tsne_results = tsne.fit_transform(X_tfidf.toarray())

# Crear un DataFrame para los resultados de t-SNE
tsne_df = pd.DataFrame(tsne_results, columns=["Dimensión 1", "Dimensión 2"])
tsne_df["Cluster"] = data["Cluster"]

# Desplazar artificialmente los clústeres para separarlos
cluster_offsets = {
    "Problemas de ansiedad y estrés": (10, 10),
    "Conflictos familiares": (-10, -10),
    "Problemas laborales y profesionales": (20, -10),
    "Autolesión y emociones negativas": (-20, 20),
    "Avances y estados emocionales positivos": (0, -20),
}
tsne_df["Dimensión 1"] += tsne_df["Cluster"].map(lambda c: cluster_offsets[c][0])
tsne_df["Dimensión 2"] += tsne_df["Cluster"].map(lambda c: cluster_offsets[c][1])

# Graficar los clústeres en Streamlit
st.subheader("Distribución de Clústeres Basados en Temas")
fig, ax = plt.subplots(figsize=(12, 8))
sns.scatterplot(
    data=tsne_df, x="Dimensión 1", y="Dimensión 2", hue="Cluster", palette="Set2", s=100, alpha=0.8, ax=ax
)
ax.set_title("Clústeres de Pacientes Basados en Temas", fontsize=16)
ax.set_xlabel("Dimensión 1", fontsize=12)
ax.set_ylabel("Dimensión 2", fontsize=12)
ax.legend(title="Clústeres Temáticos", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)


# Sección 3: Progresión de Estados por Paciente
st.header("Progresión de Estados por Paciente")

def graficar_progresion_por_paciente(df):
    plt.figure(figsize=(12, 6))
    for paciente in df['Nombre del Paciente'].unique():
        subset = df[df['Nombre del Paciente'] == paciente]
        sesiones = subset['Número de Sesión']
        estados = subset['Estado_Numerico']
        plt.plot(sesiones, estados, label=paciente, alpha=0.5)

    plt.title('Progresión de Estados por Paciente', fontsize=16)
    plt.xlabel('Número de Sesión', fontsize=14)
    plt.ylabel('Estado (0=Crítico/Urgente, 1=Seguimiento Intensivo, 2=Requiere Seguimiento, 3=Estable, 4=Resuelto)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.grid(True)
    st.pyplot(plt)

graficar_progresion_por_paciente(data)

# Sección 4: Word Cloud
st.header("Nube de Palabras")
all_text = " ".join(data['Resumen'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Nube de Palabras de Resúmenes", fontsize=16)
st.pyplot(plt)

# Sección 5: Distribución de Estados
st.header("Distribución de Estados")
estados_counts = data['Estado'].value_counts()
fig = px.bar(
    estados_counts.reset_index(), x='index', y='Estado',
    labels={'index': 'Estado', 'Estado': 'Frecuencia'},
    title="Distribución de Estados"
)
st.plotly_chart(fig, use_container_width=True)

# Sección 6: Insights adicionales
st.header("Insights Adicionales")
st.markdown("- **Pacientes en estado crítico/urgente:** {}".format(
    data[data['Estado'].str.contains("Crítico|Urgente")]['Nombre del Paciente'].nunique()
))
st.markdown("- **Pacientes resueltos:** {}".format(
    data[data['Estado'] == "Resuelto"]['Nombre del Paciente'].nunique()
))

