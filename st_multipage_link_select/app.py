import streamlit as st
import page1
import page2


def get_page_param():
    query_params = st.experimental_get_query_params()
    if 'page' in query_params:
        return query_params['page'][0]
    else:
        return None


def main():
    pages = {
        'page1': page1,
        'page2': page2
    }
    page = get_page_param()
    
    # See. https://github.com/streamlit/streamlit/issues/3635
    if page in pages.keys() and 'page' not in st.session_state:
        st.session_state['page'] = page
    
    with st.sidebar:
        page = st.selectbox('select page', pages.keys(), index=0, key='page')
        st.experimental_set_query_params(page=page)
        
    pages[page].render()


if __name__ == '__main__':
    main()