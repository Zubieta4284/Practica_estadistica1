import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Análisis Estadístico Interactivo", layout="wide")

st.title("📊 Análisis Estadístico de Datos")
st.markdown("Sube tu archivo CSV para generar tablas de frecuencias y representaciones gráficas dependiendo del tipo de variable.")

# Subida de archivo
uploaded_file = st.file_uploader("📂 Elige un archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Cargar el dataframe
    try:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Vista previa de los datos")
        st.dataframe(df.head())
        
        with st.expander("Ver información adicional del DataFrame"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Estadísticas Descriptivas:**")
                st.dataframe(df.describe())
            with col2:
                st.markdown("**Valores nulos por columna:**")
                st.dataframe(df.isnull().sum())

        st.sidebar.title("⚙️ Configuración de Análisis")
        
        # Menú para seleccionar el tipo de variable
        tipo_variable = st.sidebar.selectbox(
            "1. Seleccione el tipo de variable a analizar:",
            ["Cualitativa (Nominal/Ordinal)", "Cuantitativa Discreta", "Cuantitativa Continua (Agrupada)"]
        )
        
        # Filtrar columnas según el tipo de variable seleccionado
        if tipo_variable == "Cualitativa (Nominal/Ordinal)":
            columnas = df.select_dtypes(exclude=['number']).columns.tolist()
            if not columnas:
                st.sidebar.warning("No se encontraron variables estrictamente cualitativas.")
                columnas = df.columns.tolist() # Fallback
        else:
            columnas = df.select_dtypes(include=['number']).columns.tolist()
            if not columnas:
                st.sidebar.warning("No se encontraron variables numéricas.")
                columnas = df.columns.tolist() # Fallback
                
        col_seleccionada = st.sidebar.selectbox(f"2. Seleccione la columna para análisis {tipo_variable.split(' ')[0].lower()}:", columnas)
        
        if st.sidebar.button("Analizar"):
            st.divider()
            st.header(f"📈 Análisis de la variable: `{col_seleccionada}`")
            st.caption(f"Tipo seleccionado: {tipo_variable}")
            
            # Limpiar valores nulos de la columna para el análisis
            serie_datos = df[col_seleccionada].dropna()
            
            # Configuración de estilo académico
            plt.style.use('seaborn-v0_8-whitegrid')
            plt.rcParams['axes.titlesize'] = 16
            plt.rcParams['axes.labelsize'] = 12
            
            if tipo_variable == "Cualitativa (Nominal/Ordinal)":
                # TABLA DE FRECUENCIAS
                frec_cualita = serie_datos.value_counts().reset_index()
                frec_cualita.columns = [col_seleccionada, "fi"]
                frec_cualita["hi"] = frec_cualita["fi"] / len(serie_datos)
                frec_cualita["hip"] = frec_cualita["hi"] * 100
                frec_cualita["Fi"] = frec_cualita["fi"].cumsum()
                frec_cualita["Hi"] = frec_cualita["hi"].cumsum()
                
                st.subheader("📋 Tabla de Frecuencias")
                st.dataframe(frec_cualita)
                
                # GRÁFICOS
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Gráfico de Barras**")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(frec_cualita[col_seleccionada].astype(str), frec_cualita["fi"], color='#3498db', edgecolor='black')
                    ax.set_title(f'DISTRIBUCIÓN POR {col_seleccionada.upper()}', fontweight='bold')
                    ax.set_xlabel(col_seleccionada.capitalize())
                    ax.set_ylabel('Cantidad (fi)')
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
                    
                with col2:
                    st.markdown("**Gráfico de Pastel**")
                    fig2, ax2 = plt.subplots(figsize=(8, 5))
                    ax2.pie(frec_cualita['hi'], labels=frec_cualita[col_seleccionada].astype(str), autopct='%1.1f%%', 
                           startangle=90, colors=sns.color_palette('pastel'))
                    ax2.set_title(f"PORCENTAJE POR {col_seleccionada.upper()}", fontweight="bold")
                    st.pyplot(fig2)

            elif tipo_variable == "Cuantitativa Discreta":
                # Validar si es numérica
                if not pd.api.types.is_numeric_dtype(serie_datos):
                    st.warning("⚠️ La columna seleccionada no parece ser numérica. Los resultados pueden no ser los esperados.")
                
                # TABLA DE FRECUENCIAS
                df_discreta = serie_datos.value_counts().sort_index().reset_index()
                df_discreta.columns = [col_seleccionada, 'fi']
                df_discreta['hi'] = df_discreta['fi'] / len(serie_datos)
                df_discreta['Fi'] = df_discreta['fi'].cumsum()
                df_discreta['Hi'] = df_discreta['hi'].cumsum()
                df_discreta['hip'] = df_discreta['hi'] * 100
                
                st.subheader("📋 Tabla de Frecuencias (Sin agrupar)")
                st.dataframe(df_discreta)
                
                # GRÁFICO
                st.subheader("📊 Gráfico de Bastones")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.vlines(x=df_discreta[col_seleccionada], ymin=0, ymax=df_discreta['fi'], color='navy', linewidth=2)
                ax.plot(df_discreta[col_seleccionada], df_discreta['fi'], "o", color='red') 
                ax.set_xticks(df_discreta[col_seleccionada]) 
                ax.set_title(f'DISTRIBUCIÓN DE {col_seleccionada.upper()}', fontweight='bold')
                ax.set_xlabel(col_seleccionada.capitalize())
                ax.set_ylabel('Frecuencia Absoluta (fi)')
                st.pyplot(fig)

            elif tipo_variable == "Cuantitativa Continua (Agrupada)":
                # Validar que sea numérica
                if not pd.api.types.is_numeric_dtype(serie_datos):
                    st.error("❌ La columna seleccionada no es numérica. Por favor, seleccione una columna que contenga números continuos.")
                else:
                    n = len(serie_datos)
                    min_val = serie_datos.min()
                    max_val = serie_datos.max()
                    rango = max_val - min_val
                    
                    # Regla de Sturges
                    k = int(np.ceil(1 + 3.322 * np.log10(n))) 
                    amplitud = rango / k
                    
                    st.info(f"**Regla de Sturges aplicada:** \n"
                            f"- **Datos válidos (n):** {n} | **Rango:** {rango:.2f} \n"
                            f"- **Mínimo:** {min_val:.2f} | **Máximo:** {max_val:.2f} \n"
                            f"- **Intervalos (k):** {k} | **Amplitud:** {amplitud:.2f}")
                    
                    # Crear cortes
                    cortes = np.arange(min_val, max_val + amplitud, amplitud)
                    
                    # Agrupar en intervalos
                    intervalos = pd.cut(serie_datos, bins=cortes, include_lowest=True, right=False)
                    
                    df_agrupada = intervalos.value_counts().sort_index().reset_index()
                    df_agrupada.columns = ["intervalos", "fi"]
                    
                    # Cálculos para la tabla
                    df_agrupada["intervalos_str"] = df_agrupada["intervalos"].astype(str)
                    df_agrupada["marca_clase"] = df_agrupada["intervalos"].apply(lambda x: x.mid if pd.notnull(x) else 0)
                    df_agrupada["hi"] = df_agrupada["fi"] / n
                    df_agrupada["hip"] = df_agrupada["hi"] * 100
                    df_agrupada["Fi"] = df_agrupada["fi"].cumsum()
                    df_agrupada["Hi"] = df_agrupada["hi"].cumsum()
                    
                    columnas_mostrar = ["intervalos_str", "marca_clase", "fi", "hi", "hip", "Fi", "Hi"]
                    
                    st.subheader("📋 Tabla de Frecuencias Agrupadas")
                    st.dataframe(df_agrupada[columnas_mostrar])
                    
                    # GRÁFICOS
                    st.subheader("📊 Histograma y Polígono de Frecuencias")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.hist(serie_datos, bins=cortes, color='#11caa0', edgecolor='white', alpha=0.6, label='Histograma')
                    ax.plot(df_agrupada['marca_clase'], df_agrupada['fi'], color='red', marker='D', linewidth=2, label='Polígono')
                    ax.set_title(f'DISTRIBUCIÓN AGRUPADA DE {col_seleccionada.upper()}', fontweight='bold')
                    ax.set_xticks(cortes)
                    ax.set_xlabel('Intervalos de Clase / Marca de Clase (Xi)')
                    ax.set_ylabel('Frecuencia Absoluta (fi)')
                    plt.xticks(rotation=45)
                    ax.legend()
                    st.pyplot(fig)
                    
                    st.subheader("📉 Ojiva (Frecuencia Acumulada)")
                    fig2, ax2 = plt.subplots(figsize=(10, 5))
                    ax2.plot(df_agrupada['marca_clase'], df_agrupada['Fi'], color='red', marker='s', linewidth=2, label='Ojiva')
                    ax2.fill_between(df_agrupada['marca_clase'], df_agrupada['Fi'], color='purple', alpha=0.3)
                    ax2.set_title(f'OJIVA: {col_seleccionada.upper()}', fontweight='bold')
                    ax2.set_xticks(cortes)
                    ax2.set_xlabel('Marca de Clase (Xi)')
                    ax2.set_ylabel('Frecuencia Absoluta Acumulada (Fi)')
                    plt.xticks(rotation=45)
                    ax2.legend()
                    st.pyplot(fig2)
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar el análisis.")
