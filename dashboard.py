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

# Sección 6: Heatmap de Sentimientos
st.header("Distribución de Sentimientos")

# Generar datos simulados para el heatmap
sentimientos_heatmap_data = pd.DataFrame({
    'Sesión': [f'S{i+1}' for i in range(67)],
    'Psicóloga': data['psicologa'],
    'Sentimiento': ['Negativo'] * 25 + ['Neutro'] * 20 + ['Positivo'] * 22  # Simular sentimientos
})

# Crear un pivot table para el heatmap
heatmap_data = sentimientos_heatmap_data.pivot_table(index='Psicóloga', columns='Sesión', values='Sentimiento', aggfunc='first', fill_value='')

# Convertir sentimientos a datos numéricos
sentimiento_map = {'Negativo': -1, 'Neutro': 0, 'Positivo': 1}
heatmap_data_numeric = heatmap_data.replace(sentimiento_map).fillna(0)  # Reemplazar y llenar valores nulos con 0
heatmap_data_numeric = heatmap_data_numeric.astype(float)  # Asegurar que los datos sean numéricos

# Crear el heatmap
fig, ax = plt.subplots(figsize=(12, 6))
im = ax.imshow(heatmap_data_numeric.values, cmap="RdYlGn", aspect="auto")

# Configurar el heatmap
ax.set_xticks(range(len(heatmap_data_numeric.columns)))
ax.set_xticklabels(heatmap_data_numeric.columns, rotation=90, fontsize=8)
ax.set_yticks(range(len(heatmap_data_numeric.index)))
ax.set_yticklabels(heatmap_data_numeric.index, fontsize=10)
plt.colorbar(im, ax=ax, orientation="vertical", label="Sentimientos (-1=Negativo, 0=Neutro, 1=Positivo)")
plt.title("Heatmap de Distribución de Sentimientos por Sesión y Psicóloga", fontsize=14)
plt.tight_layout()

# Guardar el heatmap y mostrarlo
plt.savefig("heatmap_sentimientos.png")
st.image("heatmap_sentimientos.png", caption="Distribución de Sentimientos por Psicóloga y Sesión")

# Sección 7: Progreso Individual del Paciente
st.header("Progreso Gradual del Paciente P005")

# Datos simulados para progreso gradual
progreso_data = pd.DataFrame({
    'Sesión': [f'S{i+1}' for i in range(10)],  # Simular 10 sesiones
    'Sentimiento': [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5]  # Progreso gradual
})

# Gráfico de progreso
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(progreso_data['Sesión'], progreso_data['Sentimiento'], marker='o', linestyle='-', color='green')
ax.set_title("Progreso Gradual del Paciente P005", fontsize=14)
ax.set_xlabel("Sesión")
ax.set_ylabel("Nivel de Sentimiento")
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Línea base neutra
ax.grid(True)

# Guardar el gráfico de progreso y mostrarlo
plt.savefig("progreso_gradual_p005.png")
st.image("progreso_gradual_p005.png", caption="Progreso Gradual del Paciente P005")
