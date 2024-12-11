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
# Sección 2: Visualización de Clústeres Temáticos
st.header("Visualización de Clústeres Temáticos")

# Subir y mostrar la imagen de los clústeres
st.subheader("Distribución de Clústeres Basados en Temas")
st.image("patient clusters.png", caption="Clústeres de Pacientes Basados en Temas", use_column_width=True)


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

