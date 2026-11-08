import streamlit as st

st.title("Session State Explorer")

# 카운터 초기화 Initialize a counter
if "counter" not in st.session_state:   # ① 세션 상태에 counter가 없을 때만 0으로 초기화
    st.session_state.counter = 0

# 카운터 표시 Display the counter
st.write(f"Counter value: {st.session_state.counter}")

# 카운터를 바꾸는 버튼들 Buttons to modify the counter
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Increment"):          # ② 버튼을 클릭하면 카운터 값을 변경
        st.session_state.counter += 1
        st.rerun()

with col2:
    if st.button("Decrement"):
        st.session_state.counter -= 1
        st.rerun()

with col3:
    if st.button("Reset"):
        st.session_state.counter = 0
        st.rerun()

# # 세션 상태 전체 내용 표시 Show all session state contents
st.divider()
st.subheader("Current Session State:")
st.write(dict(st.session_state))
