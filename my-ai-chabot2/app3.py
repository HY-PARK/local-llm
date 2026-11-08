import streamlit as st

st.set_page_config(
    page_title="My Streamlit App",
    page_icon="Tools",
    layout="wide",
)

st.title("Streamlit Components Example")
st.header("This is a header")
st.subheader("This is a subheader")
st.write("This is a simple text output using the write function.")

st.divider()

st.subheader("Text Input Example")
user_input = st.text_input("Try something here:")
if user_input:
    st.write(f"You entered: {user_input}")

st.subheader("Text Area Example")
long_text = st.text_area("Enter a longer text here:", height=100)
if long_text:
    st.write(f"Your message has {len(long_text)} words.")

st.subheader("Selectbox Example")
color = st.selectbox("Choose a color:", ["Red", "Green", "Blue"])
st.write(f"You selected: {color}")

st.subheader("Button Example")
if st.button("Click me!"):
    st.write("Button clicked!")
    st.balloons()

with st.sidebar:
    st.header("Sidebar Example")
    st.write("This is a sidebar where you can add additional components.")
    sidebar_option = st.radio(
        "Choose an option:", ["Option 1", "Option 2", "Option 3"]
    )
    st.write(f"You selected: {sidebar_option}")

st.subheader("Columns Example")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("This is column 1")
    st.metric("Temperature", "70 °F", "1.2 °F")

with col2:
    st.write("This is column 2")
    st.metric("Humidity", "50%", "-5%")

with col3:
    st.write("This is column 3")
    st.metric("Wind Speed", "15 mph", "2 mph")
