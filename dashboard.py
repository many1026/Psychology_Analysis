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
st.image("Patient Clusters.png", caption="Clústeres de Pacientes Basados en Temas", use_column_width=True)


# Sección 3: Progresión de Estados por Paciente en Batches
st.header("Progresión de Estados por Paciente")

def graficar_progresion_por_paciente_batch(df, pacientes):
    plt.figure(figsize=(12, 6))
    for paciente in pacientes:
        subset = df[df['Nombre del Paciente'] == paciente]
        sesiones = subset['Número de Sesión']
        estados = subset['Estado_Numerico']
        plt.plot(sesiones, estados, label=paciente, alpha=0.7, marker='o')

    plt.title('Progresión de Estados por Paciente (Batch)', fontsize=16)
    plt.xlabel('Número de Sesión', fontsize=14)
    plt.ylabel('Estado (0=Crítico/Urgente, 1=Seguimiento Intensivo, 2=Requiere Seguimiento, 3=Estable, 4=Resuelto)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.grid(True)
    st.pyplot(plt)

# Dividir los pacientes en batches de 5
pacientes_unicos = data['Nombre del Paciente'].unique()
batches = [pacientes_unicos[i:i+5] for i in range(0, len(pacientes_unicos), 5)]

# Navegación entre batches
batch_index = st.slider("Selecciona el Batch", min_value=0, max_value=len(batches)-1, step=1, format="Batch %d")
st.subheader(f"Batch {batch_index + 1} de {len(batches)}")
