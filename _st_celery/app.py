import pickle

import pandas as pd
import streamlit as st

import worker


def get_results():
    results = []
    for file in worker.ARTIFACT_PATH.iterdir():
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
        df = pd.DataFrame(results).set_index('id')
        st.write(df.sort_values('start', ascending=False))
    st.button('reload')


if __name__ == '__main__':
    main()