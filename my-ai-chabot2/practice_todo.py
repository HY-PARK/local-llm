import streamlit as st

st.title("Todo List App")

# 리스트 초기화 Initialize a list
if "list" not in st.session_state:   # ① 세션 상태에 list가 없을 때만 빈 문자열로 초기화
    st.session_state.list = ""

if "show_input" not in st.session_state:
    st.session_state.show_input = False

# 리스트를 바꾸는 버튼들 Buttons to modify the list
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("항목 추가"):
        st.session_state.show_input = True

with col2:
    if st.button("마지막 삭제"):
        st.session_state.list = "\n".join(st.session_state.list.strip().split("\n")[:-1])

with col3:
    if st.button("전체 삭제"):
        st.session_state.list = ""

if st.session_state.show_input:
    with st.form("add_item_form", clear_on_submit=True):
        new_item = st.text_input("추가할 항목을 입력하세요:")
        submitted = st.form_submit_button("저장")

    if submitted:
        if new_item.strip():
            st.session_state.list += new_item.strip() + "\n"
            st.session_state.show_input = False
            st.rerun()
        else:
            st.warning("항목을 입력해주세요.")

st.write(f"TODO LIST: {st.session_state.list}")
