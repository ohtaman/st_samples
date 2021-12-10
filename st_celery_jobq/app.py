import pickle

import pandas as pd
import streamlit as st

import worker


def get_results():
    results = []
    for file in worker.ARTIFACT_PATH.iterdir():
        if file.name.startswith('.'): # 隠しファイルの除く
            continue
        with open(file, 'rb') as i_:
            results.append(pickle.load(i_))
    return results


def main():
    st.write('Hello, Celery!')

    with st.sidebar:
        x = st.number_input('x')
        y = st.number_input('y')
        submit = st.button('submit')
    if submit:
        task_id = worker.add.delay(x, y)
        st.write(f'task submitted: {task_id}')

    results = get_results()
    if results:
        df = pd.DataFrame.from_records(results)
        st.write(df)
    st.button('reload')


if __name__ == '__main__':
    main()