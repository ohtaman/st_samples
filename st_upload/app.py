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
        columns = st.multiselect(data.columns)
        filtered_data = data[columns]
        st.write(filtered_data)
        st.download_button('ダウンロード', filtered_data)

if __name__ == '__main__':
    main()