import streamlit as st
import page1
import page2

def main():
    with st.sidebar:
        page = st.selectbox('', ('page1', 'page2'), )

        # URL に反映させたい場合は以下のような処理をする
        if page == 'page1':
            st.experimental_set_query_params(page='page1')
        elif page == 'page2':
            st.experimental_set_query_params(page='page2')
        query = st.experimental_get_query_params()
        page = 'page1' if not 'page' in query else query['page'][0]

    if page == 'page1':
        page1.render()
    elif page == 'page2':
        page2.render()


if __name__ == '__main__':
    main()