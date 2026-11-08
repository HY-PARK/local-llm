import streamlit as st

st.title("Calculator App")


x = st.number_input("Try Inuput Number 1")
op = st.selectbox("Choose a color:", ["+", "-", "*", "/"])
y = st.number_input("Try Input Number 2")

#x 와 y를 조합해서 입력된 op에 따라 계산을 수행하고 결과를 출력
if op == "+":
    result = x + y
elif op == "-":
    result = x - y
elif op == "*":
    result = x * y
elif op == "/":
    if y != 0:
        result = x / y
    else:
        result = "Error: Division by zero"

st.write(f"Result: {result}")



with st.sidebar:
    color = st.selectbox("Choose a color:", ["Red", "Green", "Blue"])
    slider = st.slider("Select a range of values", 1, 10)


st.success(f"You selected: {color}")
st.error(f"You selected a range of values: {slider}")
