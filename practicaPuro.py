
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")
#mostrar los primeros 5 registros
print(df_est.head())

#mostrar estadisticas descriptivas
print(df_est.describe())
#mostrar informacion del dataframe
print(df_est.info())
#variable cualitativa nominal nombre de las carreras
frec_cualita=df_est["carrera"].value_counts().reset_index()
#renombrar columnas
frec_cualita.columns=["carrera","fi"]
#frecuencia relativa
frec_cualita["hi"]=frec_cualita["fi"]/len(df_est)
#frecuencia relativa porcentual
frec_cualita["hip"]=frec_cualita["hi"]*100
#frecuencia acumulada
frec_cualita["Fi"]=frec_cualita["fi"].cumsum()
#frecuencia relativa acumulada
frec_cualita["Hi"]=frec_cualita["hi"].cumsum()
print("TABLA DE FRECUENCIAS: CARRERAS")
print(frec_cualita)

#TABLA DE FRECUENCIAS PARA LA VARIABLE CUANTITATIVA NO AGRUPADAS MATERIAS DISCRETAS
# Conteo de frecuencias para la variable discreta 'materias_aprobadas'
df_materias = df_est['materias_aprobadas'].value_counts().sort_index().reset_index()
# Renombramos las columnas para que coincidan con tu Guía Metodológica
df_materias.columns = ['materias', 'fi']
#calculo de Frecuencia relativa
df_materias['hi']=df_materias['fi']/len(df_est)
# Cálculo de Frecuencias Acumuladas (Fi)
# El método .cumsum() realiza la suma sucesiva
df_materias['Fi'] = df_materias['fi'].cumsum()
df_materias['Hi']=df_materias['hi'].cumsum()
df_materias['hip']=df_materias['hi']*100
print("TABLA DE FRECUENCIAS: MATERIAS APROBADAS")
print(df_materias)

#TABLA DE FRECUENCIAS PARA LA VARIABLE CUANTITATIVA DISCRETA EDAD
n = len(df_est)
rango = df_est['edad'].max() - df_est['edad'].min()

# Aplicación de la Regla de Sturges (Rigor académico)
#ceil redondea hacia arriba
k = int(np.ceil(1 + 3.322 * np.log10(n))) 
amplitud = rango / k
print(f"n: {n}, Rango: {rango}, Intervalos (k): {k}, minimo: {df_est["edad"].min()}, maximo: {df_est["edad"].max()}, Amplitud: {amplitud}")
#divide el rango en k partes en tipo array
cortes=np.arange(df_est["edad"].min(),df_est["edad"].max()+amplitud,amplitud)

#Definicion de intervalos
#include_lowest=True incluye el primer intervalo
#right=False indica que el intervalo es [a,b)
df_est["intervalos"]=pd.cut(df_est["edad"],bins=cortes,include_lowest=True,right=False)
#a partir de los intervalos se cuentan las frecuencias
df_edad=df_est["intervalos"].value_counts().sort_index().reset_index()
df_edad.columns=["intervalos","fi"]
#nos permite calcular la media de los intervalos
#lambda se usa para aplicar una funcion a cada elemento de la columna
df_edad["marca_clase"]=df_edad["intervalos"].apply(lambda x: x.mid)
#frecuencia relativa
df_edad["hi"]=df_edad["fi"]/len(df_est)
#frecuencia relativa porcentual
df_edad["hip"]=df_edad["hi"]*100
#frecuencia acumulada
df_edad["Fi"]=df_edad["fi"].cumsum()
#frecuencia relativa acumulada
df_edad["Hi"]=df_edad["hi"].cumsum()
print("TABLA DE FRECUENCIAS AGRUPADAS: EDAD")
print(df_edad)

#FASE de representacion grafica
# Configuración de estilo académico
# Permite que los gráficos se dibujen directamente debajo de la celda (exclusivo para cuadernos)
# 'style.use' define el "tema" visual. 
# 'seaborn-v0_8-whitegrid' pone un fondo blanco con una rejilla (grid) gris clara.
# La rejilla es fundamental para que el ojo pueda seguir la línea del eje hacia el dato.
plt.style.use('seaborn-v0_8-whitegrid')
# Configuramos tamaños de fuente para que el usuario pueda leer bien las etiquetas
plt.rcParams['axes.titlesize'] = 16  # Tamaño del título principal
plt.rcParams['axes.labelsize'] = 12  # Tamaño de los nombres en los ejes X e Y

# fig: Es el objeto "Figura". Imaginalo como la ventana o el marco del cuadro.
# ax: Es el objeto "Axes". Es el lienzo real donde se pintan los datos.
# figsize=(12, 6): Define el tamaño. El primer número es el ANCHO y el segundo el ALTO.
# Se mide en pulgadas. Si lo aumentas, el gráfico se hace más grande en tu pantalla.
fig,ax=plt.subplots(figsize=(12,6))
#VARIABLE CUALITATIVA CARRERA
# ax.bar(x, height, color, edgecolor)
# x = frec_cualita["carrera"] -> Aquí van las etiquetas (Sistemas, Civil, etc.)
# height = frec_cualita["fi"] -> Aquí van las alturas de las barras (las fi)
# color = '#3498db' -> Color de relleno (puedes usar nombres como 'red' o códigos HEX)
# edgecolor = 'black' -> El color de la línea que rodea la barra. Ayuda a definirla mejor.

ax.bar(frec_cualita["carrera"], frec_cualita["fi"], color='#3498db', edgecolor='black')

# .set_title(label, fontweight)
# label: El texto que aparecerá arriba.
# fontweight='bold': Hace que el texto sea más grueso (negrita).
ax.set_title('DISTRIBUCIÓN POR CARRERA', fontweight='bold')
# se define los nombres del eje x el eje y
ax.set_xlabel('Carreras Universitarias')
ax.set_ylabel('Cantidad de Estudiantes (fi)')
plt.show()

#VARIBLE CUANTITATIVA NO AGRUPADA MATERIAS DISCRETAS NUMERO DE MATERIAS APROBADAS
fig,ax=plt.subplots(figsize=(12,6))
# .vlines() (Vertical Lines): Dibuja los "bastones" (líneas delgadas).
# x: Posición exacta en el eje horizontal.
# ymin: Punto de inicio en el eje vertical (generalmente 0).
# ymax: Punto final de la línea basado en la frecuencia absoluta (fi).
ax.vlines(x=df_materias['materias'], ymin=0, ymax=df_materias['fi'], color='navy', linewidth=2)

# .plot(): Aquí se usa para poner el "punto" en la cima del bastón.
# "o": El formato de círculo. Sin esto, plot dibujaría una línea continua.
ax.plot(df_materias['materias'], df_materias['fi'], "o", color='red') 

# .set_xticks(): Obliga al eje X a mostrar cada número de la columna (1, 2, 3...).
# Evita que Python se salte números por falta de espacio.
ax.set_xticks(df_materias['materias']) 

ax.set_title('AVANCE ACADÉMICO(VARIABLES DISCRETAS)', fontweight='bold')
ax.set_xlabel('Número de Materias Aprobadas')
ax.set_ylabel('Frecuencia Absoluta (fi)')
plt.show()

#VARIBLE CUANTITATIVA AGRUPADAS EDAD HISTROGRAMA y POLIGONO DE FRECUENCIAS 
# Definimos un lienzo un poco más ancho para apreciar mejor los intervalos
fig, ax = plt.subplots(figsize=(12, 6))
# .hist(): Palabra reservada para el Histograma (barras unidas).
# el primer parametro indica toda la lista de edades en el dataframe  
# bins=cortes: USA LOS LÍMITES DE LA FASE 4. Define el ancho de la barra (Amplitud).
# alpha: Define la transparencia (0.6). Permite ver la cuadrícula de fondo a través de la barra.
ax.hist(df_est['edad'], bins=cortes, color='#11caa0', edgecolor='white', alpha=0.6, label='Histograma')
# .plot(): Aquí lo usamos para conectar las Marcas de Clase (Xi).
# x = tabla_agrupada['Xi']: Los puntos medios de cada intervalo (Eje X).
# y = tabla_agrupada['fi']: La altura de cada intervalo (Eje Y).
# color = 'red': Color de la línea.
# marker = 'D': PARÁMETRO DE FORMATO. 'D' significa Diamond (Diamante). 
#              Dibuja un diamante en cada Marca de Clase.
# linewidth = 2: Grosor de la línea que une los diamantes.
ax.plot(df_edad['marca_clase'], df_edad['fi'], color='red', marker='D', linewidth=2, label='Polígono')
ax.set_title('ANÁLISIS DE DISTRIBUCIÓN DE EDADES (DATOS AGRUPADOS)', fontweight='bold')
# set_xticks(cortes): Obliga al eje X a mostrar exactamente los límites de tus intervalos.
ax.set_xticks(cortes)
ax.set_xlabel('Intervalos de Clase (años) / Marca de Clase (Xi)')
ax.set_ylabel('Frecuencia Absoluta (fi)')
# .legend(): Muestra el cuadro explicativo (Label) de qué es el color verde y la línea roja.
ax.legend()
plt.show()

#VARIBLE CUANTITATIVA AGRUPADAS EDAD OJIVA FRECUENCIA ACUMULADA
fig,ax=plt.subplots(figsize=(10,5))
#los dos primeros argumentos son los ejes x e y
#color='red': Define el color de la línea como rojo.
#marker='s': Dibuja un cuadrado (Square) en cada punto de datos.
#linewidth=2: Establece el grosor de la línea en 2 puntos.
#label='Ojiva': Asigna una etiqueta para la leyenda.
ax.plot(df_edad['marca_clase'], df_edad['Fi'], color='red', marker='s', linewidth=2, label='Ojiva')
#fill_between: Rellena el área debajo de la línea.
#color='red': Define el color de relleno como rojo.
#alpha=0.3: Establece la transparencia del relleno en 0.3 (30% opaco).
ax.fill_between(df_edad['marca_clase'], df_edad['Fi'], color='purple', alpha=0.3)
ax.set_title('ANÁLISIS DE DISTRIBUCIÓN DE EDADES (DATOS AGRUPADOS)', fontweight='bold')
ax.set_xticks(cortes)
ax.set_xlabel('Intervalos de Clase (años)')
ax.set_ylabel('Frecuencia Absoluta Acumulada (Fi)')
ax.legend()
plt.show() 

#GRAFICO DE PASTEL PARA VARIABLES CUALITATIVA POR CARRERA
fig,ax=plt.subplots(figsize=(10,5))

# frec_cualita['hi']: Fuente de datos (Frecuencia Relativa en decimales).
# labels=frec_cualita['carrera']: Etiquetas extraídas de la columna de carreras.
# autopct='%1.1f%%': Formateador automático que convierte el decimal a porcentaje 
# con un dígito después del punto y añade el símbolo '%'.
# startangle=90: Inicia la primera división en el eje Y positivo (las 12 en punto).
# colors=sns.color_palette('pastel'): Aplica una gama de colores suaves de Seaborn.
ax.pie(frec_cualita['hi'], labels=frec_cualita['carrera'], autopct='%1.1f%%', 
       startangle=90, colors=sns.color_palette('pastel'))

# Configuración de metadatos y visualización final
ax.set_title("PORCENTAJE DE ESTUDIANTES POR CARRERA", fontweight="bold")
plt.show()

