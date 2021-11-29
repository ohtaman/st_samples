import streamlit as st
import page1
import page2


PAGES = ['page1', 'page2']


def main():
    with st.sidebar:
        for page in PAGES:
            st.markdown(
                f'<a href="?page={page}">{page}</a>',
                unsafe_allow_html=True
            )

    query = st.experimental_get_query_params()
    page = PAGES[0] if 'page' not in query else query['page'][0]

    if page == 'page1':
        page1.render()
    elif page == 'page2':
        page2.render()

if __name__ == '__main__':
    main()