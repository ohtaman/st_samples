import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd


DATA_URL = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv'


def main():
    df = pd.read_csv(DATA_URL)
    
    gb = GridOptionsBuilder.from_dataframe(df, editable=True)
    grid = AgGrid(df, gridOptions=gb.build(), updateMode=GridUpdateMode.VALUE_CHANGED)
    
    # 修正が反映される
    st.dataframe(grid['data'])


if __name__ == '__main__':
    main()