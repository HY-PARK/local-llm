import streamlit as st

st.set_page_config(page_title="Smart Greeter", page_icon="Hi")

st.title("Smart Greeting Generator")
st.write("This app generates a personalized greeting based on your input.")

with st.sidebar:
    st.header("Settings")
    language = st.selectbox(
        "Greeting Language",
        ["English", "Spanish", "French", "German"]
    )

    formality = st.radio(
        "Formality Level",
        ["Casual", "Formal"]
    )

name = st.text_input("Enter your name:")

if name:
    greetings = {
        "English": {
            "Casual": f"Hey {name}! How's it going?",
            "Formal": f"Hello {name}, it's a pleasure to meet you."
        },
        "Spanish": {
            "Casual": f"¡Hola {name}! ¿Cómo estás?",
            "Formal": f"Hola {name}, es un placer conocerte."
        },
        "French": {
            "Casual": f"Salut {name}! Comment ça va?",
            "Formal": f"Bonjour {name}, ravi de vous rencontrer."
        },
        "German": {
            "Casual": f"Hallo {name}! Wie geht's?",
            "Formal": f"Guten Tag {name}, es freut mich, Sie kennenzulernen."
        }
    }

    greeting = greetings[language][formality]

    st.divider()
    st.subheader("Your Greeting:")
    st.success(greeting)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Language", language)
    with col2:
        st.metric("Formality", formality)
else:
    st.info("Please enter your name to generate a greeting.")
