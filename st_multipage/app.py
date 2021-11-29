import streamlit as st
import page1
import page2

def main():
    with st.sidebar:
        page = st.selectbox('', ('page1', 'page2'), )

    if page == 'page1':
        page1.render()
    elif page == 'page2':
        page2.render()


if __name__ == '__main__':
    main()