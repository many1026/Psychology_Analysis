#%%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# Configuración general
st.set_page_config(page_title="Dashboard de Sesiones Psicológicas", layout="wide")

# Carga de datos procesados
@st.cache_data
def load_data():
    # Reemplaza este código con la carga de tus datos reales
    data = pd.DataFrame({
        'psicologa': ['Ana', 'Luis', 'Maria', 'Ana', 'Luis'],
        'paciente': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'descripcion': [
            'ansiedad estrés', 'violencia familiar', 'depresión',
            'ansiedad', 'estrés laboral'
        ],
        'observacion': ['Progreso estable', 'Casos graves', 'Mejorando', 'Urgente', 'Moderado'],
        'fecha': pd.date_range('2024-01-01', periods=5, freq='D')
    })
    return data

# Datos
data = load_data()

# Título
st.title("Dashboard de Sesiones Psicológicas")
st.markdown("**Optimización del impacto del programa para la ONG**")

# Sección 1: Resumen general
st.header("Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Sesiones", len(data))
col2.metric("Pacientes Únicos", data['paciente'].nunique())
col3.metric("Psicólogas Activas", data['psicologa'].nunique())

# Sección 2: Word Cloud
st.header("Análisis de Texto: Nube de Palabras")
# Concatenar textos de 'descripcion' y 'observacion'
word_text = " ".join(data['descripcion']) + " " + " ".join(data['observacion'])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(word_text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Sección 3: Sesiones por Psicóloga
st.header("Distribución de Sesiones")
fig = px.bar(data.groupby('psicologa').size().reset_index(name='sesiones'), 
             x='psicologa', y='sesiones', title="Sesiones por Psicóloga")
st.plotly_chart(fig, use_container_width=True)

# Sección 4: Tendencias Temporales
st.header("Tendencias de Sesiones a lo Largo del Tiempo")
fig = px.line(data, x='fecha', y=data.groupby('fecha').size(), title="Sesiones por Fecha")
st.plotly_chart(fig, use_container_width=True)

# Sección 5: Insights Accionables
st.header("Insights Accionables")
st.markdown("Aquí puedes agregar análisis adicionales, como clasificación de temas o detección de sentimientos.")


# %%
x