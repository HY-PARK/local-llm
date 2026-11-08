import streamlit as st

st.title("Greeting App")

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name}! Welcome to my Streamlit app.")
