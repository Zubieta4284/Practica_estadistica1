import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import re
import datetime

def main():
    # initial_sidebar_state es una funcion que permite ocultar la barra lateral
    # collapsed es una funcion que permite ocultar la barra lateral
    # expanded es una funcion que permite mostrar la barra lateral
    st.set_page_config(page_title="Ejemplo de estadistica II",page_icon="👓", layout="wide",initial_sidebar_state="collapsed")    
    st.sidebar.title("Barra lateral") 
    st.sidebar.header("base de datos Estudiantes")  
    #carga el dataframe
    df_est=pd.read_csv("datos_estudiantes.csv")
    st.metric("Numero de registros",len(df_est))
    st.dataframe(df_est)  
    #explicar sample para quesirve al programador
    #sample es una funcion que permite seleccionar una muestra aleatoria de un dataframe
    #n es el tamaño de la muestra
    #random_state es el estado de la semilla aleatoria
    #que significa semila aleatoria

    df2=df_est.sample(n=20, random_state=10, replace=True).reset_index(drop=True) # Se añade replace=True porque 1000 es mayor a la cantidad de filas en el dataset
    #explicar sample
    st.title("BASE DE DATOS ESTUDIANTES")
    st.subheader("vista general de la Base de datos de estudiantes")
    st.metric("Numero de registros",len(df_est))
    st.dataframe(df_est)
    #st.dataframe(df2.style.highlight_max(axis=0,color="yellow"))
    st.write(df_est.head(10))
    st.write(df_est.describe())
    #st.json(df_est.to_json())
    code="""
       def suma(a,b):
        return a+b 
       print(suma(10,20))   
      """
    def suma(a,b):
        return a+b 
    st.code(code, language="python")  
    #selectbox sirve para seleccionar una opcion de una lista
    opcion=st.selectbox("Selecciona una opcion",["sumar","restar","multiplicar","dividir"])
    valor1=st.number_input("Valor 1")
    valor2=st.number_input("Valor 2")
    if opcion=="sumar":
        st.write(suma(valor1,valor2))
    #multiselect sirve para seleccionar varias opciones de una lista
    opcion2=st.multiselect("Selecciona tu color preferido", ["negro", "blanco", "verde", "azul", "rojo"])
    st.write(f"Los colores seleccionados son : {opcion2}")
    #slider sirve para seleccionar un valor de un rango
    valor3=st.slider("Selecciona un valor",
        min_value=0,
        max_value=100,
        value=1,
        step=5)
    st.write("El valor seleccionado es : ",valor3)
    #slect slider opciones
    valor4=st.select_slider("Elija el valor del clima",
        options=["bajo","medio", "regula","alto"],
        value="regula")
    st.write(f"El clima de cobija tiene un valor {valor4}")
    st.title("BOLA DE CRISTAL")
    valor5=st.select_slider("Elija la esfera que mas te guste",
        options=["esfera-cristal","esfera-sol", "esfera-cielo","esfera-mar"],
        value="esfera-cristal")
    st.title(f"La esfera elegida es {valor5}")
    ima_clima={
        "esfera-cristal":"image/bolacristal.png",
        "esfera-sol":"image/bolacristal2.png",
        "esfera-cielo":"image/bolacristal3.png",
        "esfera-mar":"image/bolacristal4.png"
    }
    

    st.image(ima_clima[valor5],caption=f"La esfera es de tipo: {valor5}",use_container_width=True)


    #Manejo de imagenes
    img=Image.open("ima1.png")
    st.image(img,use_container_width=True)

    nombre=st.text_input("Ingrese su nombre",type="password") 
    st.write("Su nombre es : ",nombre)
    descripcion=st.text_area("Ingrese su descripcion",height=100)
    st.write("Su descripcion es : ",descripcion)
    correo=st.text_input("Ingrese su correo")
    if correo:
        # Expresión regular básica para validar correo
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(patron, correo):
            st.success(f"Su correo es: {correo}")
        else:
            st.error("Por favor, ingrese un correo electrónico válido.")
    numero=st.number_input("Ingrese su numero",1,50,2)
    fecha=st.date_input("Ingrese la fecha")
    st.write("La fecha es : ",fecha)
    tiempo=st.time_input("Ingrese la hora")
    st.write("La hora es : ",tiempo)   
    #slider de fecha   
    fecha_slider=st.slider("Seleccione una fecha",
        min_value=datetime.date(2020, 1, 1),
        max_value=datetime.date(2025, 12, 31),
        value=datetime.date(2020, 1, 1))
    st.write("La fecha seleccionada es : ",fecha_slider)
    color=st.color_picker("Seleccione un color")
    st.write("El color seleccionado es : ",color)     
if  __name__ == "__main__":
    main()