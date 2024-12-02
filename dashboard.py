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
# Mostrar la imagen estática en lugar de generar la nube de palabras dinámicamente
st.image("wordcloud_actual.png", caption="Nube de Palabras Generada", use_column_width=True)


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
st.markdown("Aquí puedes agregar análisis adicionales, como clasificación de temas o detección de sentimientos.")

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

st.markdown("""
### Análisis de Temas Más Frecuentes
Este análisis muestra que los principales temas abordados en las sesiones son:
1. **Violencia intrafamiliar** (30% de las sesiones).
2. **Problemas de comunicación** (25%).
3. **Impacto en hijos/as** (20%).
4. **Relaciones conflictivas** (15%).
""")
