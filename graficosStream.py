import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Configuración de la página
st.set_page_config(page_title="Dashboard de Datos", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.title("📊 Dashboard Interactivo")
st.markdown("### Análisis Exploratorio de Datos")

# Sidebar - Subida de archivos
st.sidebar.header("📥 Cargar Datos")
# file_uploader permite cargar archivos
archivo = st.sidebar.file_uploader("Elige un archivo CSV", type=["csv"])

# si el archivo no es nulo, cargar el dataset
if archivo is not None:
    # Cargar el dataframe
    df = pd.read_csv(archivo)
    
    st.sidebar.markdown("---")
    st.sidebar.header("🛠️ Menú de Opciones")
    menu = st.sidebar.selectbox(
        "Selecciona qué deseas analizar:",
        ["Información General", "Análisis de Variables", "Gráficos"]
    )

    if menu == "Información General":
        # 2. Información general en la parte derecha (principal)
        with st.expander("Desplegar Información General", expanded=True):
            st.header("1. Información General del DataFrame")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Número de Filas:** {df.shape[0]}")
            with col2:
                st.info(f"**Número de Columnas:** {df.shape[1]}")
            
            st.write("**Vista previa de los datos:**")
            st.dataframe(df.head(), use_container_width=True)

            st.write("**Tipos de datos por columna:**")
            st.dataframe(pd.DataFrame(df.dtypes, columns=['Tipo de Dato']).astype(str))

    elif menu == "Análisis de Variables":
        # 3. Seleccionar el tipo de variable y columna
        with st.expander("Desplegar Análisis de Variables", expanded=True):
            st.header("2. Análisis de Variables y Frecuencias")
            
            filtro_tipo = st.radio(
                "Filtrar columnas por tipo de variable:",
                ["Todas", "Cualitativas (Categóricas/Texto)", "Cuantitativas (Numéricas)"],
                horizontal=True
            )

            cols_cuantitativas = df.select_dtypes(include=[np.number]).columns.tolist()
            cols_cualitativas = df.select_dtypes(exclude=[np.number]).columns.tolist()

            if filtro_tipo == "Cualitativas (Categóricas/Texto)":
                opciones_columnas = cols_cualitativas
            elif filtro_tipo == "Cuantitativas (Numéricas)":
                opciones_columnas = cols_cuantitativas
            else:
                opciones_columnas = df.columns.tolist()

            if len(opciones_columnas) == 0:
                st.warning(f"No hay variables para el filtro seleccionado en el DataFrame.")
            else:
                columna_seleccionada = st.selectbox("Selecciona una variable para analizar:", opciones_columnas)
                
                es_cuantitativa = pd.api.types.is_numeric_dtype(df[columna_seleccionada])
                tipo_actual = "Cuantitativa" if es_cuantitativa else "Cualitativa"
                
                st.subheader(f"Tabla de Frecuencias (Variable {tipo_actual})")
                
                if es_cuantitativa:
                    # Tabla de frecuencias para variables cuantitativas (usando intervalos)
                    if df[columna_seleccionada].nunique() > 10:
                        bins = st.slider("Número de intervalos (bins) para la tabla", min_value=5, max_value=50, value=10)
                        # cut para crear los intervalos
                        intervalos = pd.cut(df[columna_seleccionada], bins=bins)
                        frec_abs = intervalos.value_counts(sort=False)
                        frec_rel = intervalos.value_counts(normalize=True, sort=False) * 100
                        
                        frecuencias = pd.DataFrame({
                            'Frecuencia Absoluta': frec_abs,
                            'Frecuencia Relativa (%)': frec_rel
                        }).reset_index()
                        frecuencias.columns = ['Intervalo', 'Frecuencia Absoluta', 'Frecuencia Relativa (%)']
                        # Convertir intervalo a string para mejor visualización
                        frecuencias['Intervalo'] = frecuencias['Intervalo'].astype(str)
                        st.dataframe(frecuencias, use_container_width=True)
                    else:
                        st.info("La variable tiene pocos valores únicos, se muestra frecuencia por valor exacto.")
                        frec_abs = df[columna_seleccionada].value_counts().sort_index()
                        frec_rel = df[columna_seleccionada].value_counts(normalize=True).sort_index() * 100
                        frecuencias = pd.DataFrame({
                            'Frecuencia Absoluta': frec_abs,
                            'Frecuencia Relativa (%)': frec_rel
                        }).reset_index()
                        frecuencias.columns = ['Valor', 'Frecuencia Absoluta', 'Frecuencia Relativa (%)']
                        st.dataframe(frecuencias, use_container_width=True)
                        
                    st.write("**Estadísticas Descriptivas:**")
                    st.dataframe(df[columna_seleccionada].describe().to_frame().T, use_container_width=True)

                else:
                    # Tabla de frecuencias para variables cualitativas
                    frec_abs = df[columna_seleccionada].value_counts()
                    frec_rel = df[columna_seleccionada].value_counts(normalize=True) * 100
                    tabla_frec = pd.DataFrame({
                        'Frecuencia Absoluta': frec_abs, 
                        'Frecuencia Relativa (%)': frec_rel
                    }).reset_index()
                    tabla_frec.columns = ['Categoría', 'Frecuencia Absoluta', 'Frecuencia Relativa (%)']
                    st.dataframe(tabla_frec, use_container_width=True)

    elif menu == "Gráficos":
        # 4. Seleccionar gráficos adecuados a la variable
        with st.expander("Desplegar Visualización Gráfica", expanded=True):
            st.header(f"3. Visualización Gráfica")

            columna_grafico = st.selectbox("Selecciona una variable para graficar:", df.columns.tolist())
            
            es_cuanti_graf = pd.api.types.is_numeric_dtype(df[columna_grafico])
            tipo_actual_graf = "Cuantitativa" if es_cuanti_graf else "Cualitativa"
            
            st.write(f"**Variable detectada como:** {tipo_actual_graf}")

            if es_cuanti_graf:
                opciones_graficos = ["Histograma", "Box Plot", "Gráfico de Líneas"]
            else:
                opciones_graficos = ["Gráfico de Barras", "Gráfico Circular (Pie)"]

            tipo_grafico = st.selectbox("Elige el tipo de gráfico:", opciones_graficos)

            try:
                fig, ax = plt.subplots(figsize=(10, 5))
                
                if tipo_grafico == "Histograma":
                    sns.histplot(df[columna_grafico], kde=True, ax=ax, color='skyblue')
                    ax.set_xlabel(columna_grafico)
                    ax.set_ylabel("Frecuencia")
                    ax.set_title(f"Histograma de {columna_grafico}")
                    
                elif tipo_grafico == "Box Plot":
                    sns.boxplot(x=df[columna_grafico], ax=ax, color='lightgreen')
                    ax.set_xlabel(columna_grafico)
                    ax.set_title(f"Box Plot de {columna_grafico}")
                    
                elif tipo_grafico == "Gráfico de Líneas":
                    # Graficar los valores ordenados para ver la distribución/tendencia
                    df_sorted = df[columna_grafico].sort_values().reset_index(drop=True)
                    ax.plot(df_sorted, marker='', linestyle='-', color='coral')
                    ax.set_ylabel(columna_grafico)
                    ax.set_xlabel("Índice (Datos ordenados)")
                    ax.set_title(f"Gráfico de Líneas de {columna_grafico} (Valores Ordenados)")
                    
                elif tipo_grafico == "Gráfico de Barras":
                    counts = df[columna_grafico].value_counts()
                    sns.barplot(x=counts.index, y=counts.values, ax=ax, hue=counts.index, palette='viridis', legend=False)
                    ax.set_xlabel(columna_grafico)
                    ax.set_ylabel("Frecuencia")
                    ax.set_title(f"Gráfico de Barras de {columna_grafico}")
                    plt.xticks(rotation=45, ha='right')
                    
                elif tipo_grafico == "Gráfico Circular (Pie)":
                    counts = df[columna_grafico].value_counts()
                    ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
                    ax.axis('equal') 
                    ax.set_title(f"Distribución de {columna_grafico}")
                
                plt.tight_layout()
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error al generar el gráfico: {e}")

else:
    st.info("👆 Sube un archivo CSV desde la barra lateral izquierda para comenzar a visualizar tus datos.")