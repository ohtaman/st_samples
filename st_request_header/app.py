import pandas as pd
import streamlit as st
from streamlit.server.server import Server


def main():
    session_infos = Server.get_current()._session_info_by_id.values()
    headers = [info.ws.request.headers for info in session_infos]
    st.write(pd.DataFrame(headers))


if __name__ == '__main__':
    main()