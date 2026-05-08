import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Analítico", page_icon="📊", layout="wide")

# 2. Generación de Datos Simulados (Usamos @st.cache_data para no regenerar en cada clic)
@st.cache_data
def generar_datos(n=300):
    np.random.seed(42)
    datos = {
        # --- Variables Cuantitativas (Números) ---
        'Edad': np.random.normal(35, 8, n).astype(int), # Distribución normal
        'Salario': np.random.normal(55000, 15000, n).round(2),
        'Puntuacion_KPI': np.random.uniform(40, 100, n).round(1),
        
        # --- Variables Cualitativas (Categorías) ---
        'Departamento': np.random.choice(['Ventas', 'IT', 'Marketing', 'RRHH', 'Finanzas'], n),
        'Sede': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], n),
        'Desempeño': np.random.choice(['Bajo', 'Medio', 'Alto'], n, p=[0.15, 0.60, 0.25])
    }
    df = pd.DataFrame(datos)
    # Limpiamos edades ilógicas generadas por la distribución normal
    df['Edad'] = df['Edad'].apply(lambda x: x if x > 18 else 18) 
    return df

df = generar_datos()

# Listas de columnas por tipo para facilitar los filtros
vars_cuanti = ['Edad', 'Salario', 'Puntuacion_KPI']
vars_cuali = ['Departamento', 'Sede', 'Desempeño']

# --- BARRA LATERAL: MENÚ DE NAVEGACIÓN ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1822/1822094.png", width=100)
st.sidebar.title("Menú Principal")
opcion_menu = st.sidebar.radio(
    "Selecciona la vista a mostrar:",
    ("1. Vista General", "2. Análisis Cuantitativo", "3. Análisis Cualitativo", "4. Relaciones (Cuali vs Cuanti)")
)

st.sidebar.markdown("---")
st.sidebar.info("Este dashboard permite analizar distintas variables según su naturaleza estadística.")

# --- LÓGICA DEL MENÚ ---

# VISTA 1: GENERAL
if opcion_menu == "1. Vista General":
    st.title("🗂️ Vista General de los Datos")
    st.write("Exploración del Dataset (Primeros registros y estructura).")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registros", len(df))
    col2.metric("Variables Cuantitativas", len(vars_cuanti))
    col3.metric("Variables Cualitativas", len(vars_cuali))
    
    st.dataframe(df.head(15), use_container_width=True)

# VISTA 2: CUANTITATIVAS
elif opcion_menu == "2. Análisis Cuantitativo":
    st.title("📈 Análisis de Variables Cuantitativas")
    st.write("Analiza la distribución y estadísticas de las variables numéricas.")
    
    var_seleccionada = st.selectbox("Selecciona una variable numérica:", vars_cuanti)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Histograma con Matplotlib y Seaborn
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[var_seleccionada], kde=True, color='teal', ax=ax)
        ax.set_title(f'Distribución de {var_seleccionada}')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)
        
    with col2:
        st.subheader("Estadísticas Clave")
        st.dataframe(df[var_seleccionada].describe(), use_container_width=True)

# VISTA 3: CUALITATIVAS
elif opcion_menu == "3. Análisis Cualitativo":
    st.title("pie Análisis de Variables Cualitativas")
    st.write("Analiza las frecuencias y proporciones de las categorías.")
    
    var_seleccionada = st.selectbox("Selecciona una variable categórica:", vars_cuali)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Gráfico de barras de conteo
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=df, x=var_seleccionada, palette='viridis', ax=ax, order=df[var_seleccionada].value_counts().index)
        ax.set_title(f'Conteo por {var_seleccionada}')
        ax.set_ylabel('Cantidad de Empleados')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    with col2:
        st.subheader("Tabla de Frecuencias")
        conteo = df[var_seleccionada].value_counts().reset_index()
        conteo.columns = [var_seleccionada, 'Cantidad']
        st.dataframe(conteo, use_container_width=True)

# VISTA 4: RELACIONES (CUALITATIVAS VS CUANTITATIVAS)
elif opcion_menu == "4. Relaciones (Cuali vs Cuanti)":
    st.title("🔗 Relación: Categorías vs Números")
    st.write("Descubre cómo varían los números dependiendo de la categoría (ej. Salario por Departamento).")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        cuali = st.selectbox("Eje X (Agrupación - Cualitativa):", vars_cuali)
    with col_sel2:
        cuanti = st.selectbox("Eje Y (Medición - Cuantitativa):", vars_cuanti)
        
    # Gráfico de Cajas (Boxplot) para ver la distribución numérica segmentada por categorías
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x=cuali, y=cuanti, palette='Set2', ax=ax)
    ax.set_title(f'Distribución de {cuanti} agrupado por {cuali}', fontsize=14)
    st.pyplot(fig)
    
    # Tabla pivote resumen
    st.subheader(f"Promedio de {cuanti} por {cuali}")
    tabla_resumen = df.groupby(cuali)[cuanti].mean().round(2).sort_values(ascending=False).reset_index()
    st.dataframe(tabla_resumen, use_container_width=True)