#%%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# Configuración general
st.set_page_config(page_title="Dashboard de Sesiones Psicológicas", layout="wide")

@st.cache_data
def load_data():
    # Generar datos para cada psicóloga
    data = pd.DataFrame({
        'psicologa': (
            ['Carmen María'] * 20 +  # 17 sesiones para Carmen María
            ['Samantha'] * 17 +       # 20 sesiones para Miriam
            ['Miriam'] * 30        # 30 sesiones para Maribel
        ),
        'paciente': [f'P{i+1}' for i in range(67)],  # Generar 67 pacientes únicos
        'descripcion': (
            ['ansiedad estrés', 'violencia familiar', 'depresión', 'ansiedad', 'problemas laborales'] * 13 +  # Repetir patrones
            ['problemas familiares', 'estrés constante', 'conflicto con pareja', 'problemas emocionales', 'ansiedad social', 'falta de apoyo'] * 11 +
            ['estrés laboral', 'conflictos familiares', 'violencia verbal', 'proceso de divorcio', 'problemas emocionales', 'ansiedad'] * 10
        )[:67],  # Asegurar que sean exactamente 67 descripciones
        'observacion': (
            ['Progreso estable', 'Casos graves', 'Mejorando', 'Urgente', 'Moderado'] * 13 +
            ['En progreso', 'Requiere seguimiento', 'Avances lentos', 'Requiere intervención', 'Estancado'] * 11 +
            ['Progreso observado', 'Casos severos', 'Necesita intervención', 'Apoyo familiar sugerido', 'Seguimiento emocional'] * 10
        )[:67],  # Asegurar que sean exactamente 67 observaciones
        'fecha': pd.date_range('2024-01-01', periods=67, freq='D')  # Generar 67 fechas consecutivas
    })
    return data

data = load_data()

# Título
st.title("Dashboard de Sesiones Psicológicas")
st.markdown("**Optimización del impacto del programa para Mujer Violeta**")


# Sección 1: Resumen general
st.header("Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Sesiones", len(data))
col2.metric("Pacientes Únicos", data['paciente'].nunique())
col3.metric("Psicólogas Activas", data['psicologa'].nunique())

# Sección 2: Word Cloud
st.header("Análisis de Texto: Nube de Palabras")
# Mostrar la imagen estática en lugar de generar la nube de palabras dinámicamente
st.image("nube_de_palabras.png", caption="Nube de Palabras Generada", use_column_width=True)

# Sección 3: Temas Más Frecuentes
st.header("Temas Más Frecuentes en las Sesiones")
temas = ["Violencia intrafamiliar", "Problemas de comunicación", "Impacto en hijos/as", "Relaciones conflictivas"]
frecuencias = [30, 25, 20, 15]

# Generar el gráfico
plt.figure(figsize=(8, 5))
plt.bar(temas, frecuencias, color='skyblue')
plt.title("Temas Más Frecuentes en las Sesiones")
plt.xlabel("Temas")
plt.ylabel("Frecuencia (%)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("temas_frecuentes.png")  # Guardar el gráfico como imagen
st.image("temas_frecuentes.png", caption="Temas Más Frecuentes")  # Mostrarlo en Streamlit



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

# Sección 6: Análisis de Sentimientos
st.header("Distribución de Sentimientos")
sentimientos = ["Negativo", "Neutro", "Positivo"]
valores = [60, 25, 15]

# Sección 7: Progreso Individual del Paciente
st.header("Progreso del Paciente P005")
sesiones = [1, 2, 3, 4]
sentimientos_p005 = [-1, -1, 0, 1]  # Escala: -1 = Negativo, 0 = Neutro, 1 = Positivo

# Generar el gráfico de pastel
plt.figure(figsize=(6, 6))
plt.pie(valores, labels=sentimientos, autopct='%1.1f%%', colors=["red", "gray", "green"])
plt.title("Distribución de Sentimientos en las Sesiones")
plt.savefig("sentimientos.png")  # Guardar el gráfico
st.image("sentimientos.png", caption="Distribución de Sentimientos")  # Mostrarlo

# Gráfico de línea para mostrar el progreso
plt.figure(figsize=(8, 5))
plt.plot(sesiones, sentimientos_p005, marker='o', linestyle='-', color='blue')
plt.title("Progreso del Paciente P005")
plt.xlabel("Sesiones")
plt.ylabel("Sentimiento (Escala)")
plt.grid(True)
plt.savefig("progreso_p005.png")  # Guardar el gráfico
st.image("progreso_p005.png", caption="Progreso del Paciente P005")  # Mostrarlo
