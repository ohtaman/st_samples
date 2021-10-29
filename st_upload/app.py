import streamlit as st
import pandas as pd


def main():
    st.markdown('# File Upload example')
    file = st.file_uploader('Upload csv/tsv/txt file.', type=['csv', 'tsv', 'txt'])
    if file:
        st.write(f'file type: {file.type}')
        if file.type == 'text/csv':
            delimiter = ','
        elif file.type in ('text/tab-separated-values', 'text/plain'):
            delimiter = '\t'
        else:
            delimiter = ','

        data = pd.read_csv(
            file,
            delimiter=delimiter
        )
        st.write(data)


if __name__ == '__main__':
    main()