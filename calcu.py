import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Calculadora Streamlit", page_icon="🔢")

st.title("🔢 Calculadora Minimalista")
st.write("Selecciona los números y la operación que deseas realizar.")

# Layout de columnas para los inputs
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("Primer número", value=0.0)

with col2:
    num2 = st.number_input("Segundo número", value=0.0)

# Selección de operación
operacion = st.selectbox(
    "Selecciona una operación",
    ("Suma", "Resta", "Multiplicación", "División", "Potencia")
)

# Lógica de la calculadora
resultado = 0
error = False

if st.button("Calcular"):
    if operacion == "Suma":
        resultado = num1 + num2
    elif operacion == "Resta":
        resultado = num1 - num2
    elif operacion == "Multiplicación":
        resultado = num1 * num2
    elif operacion == "División":
        if num2 != 0:
            resultado = num1 / num2
        else:
            st.error("¡Error! No se puede dividir por cero.")
            error = True
    elif operacion == "Potencia":
        resultado = num1 ** num2

    # Mostrar resultado
    if not error:
        st.success(f"El resultado de la {operacion} es: **{resultado}**")

# Pie de página lateral
st.sidebar.info("Hecho con ❤️ usando Streamlit")