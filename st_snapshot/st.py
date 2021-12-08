import streamlit as st
import numpy as np
import datetime
import pathlib
import pickle
import pandas as pd

SNAPSHOT_PATH = pathlib.Path('snapshots')


def display(a, b):
    st.markdown(f'$$y = {a}\sin(x) + {b}\cos(x)$$')
    x = np.arange(-2, 2, 0.1)
    y = a*np.sin(x) + b*np.cos(x)
    df = pd.DataFrame({'x': x, 'y': y})
    df = df.set_index('x')
    st.line_chart(df)


def get_snapshots():
    snapshots = [
        path.stem
        for path in SNAPSHOT_PATH.iterdir()
        if path.suffix == '.pkl'
    ]
    snapshots.sort()
    snapshots.reverse()
    return snapshots


def get_data(snapshot_id):
    path = SNAPSHOT_PATH.joinpath(f'{snapshot_id}.pkl')
    with open(path,'rb') as i_:
        return pickle.load(i_)


def save_data(data):
    snapshot_id = get_snapshot_id()
    if not SNAPSHOT_PATH.exists():
        SNAPSHOT_PATH.mkdir(parents=True)
    path = SNAPSHOT_PATH.joinpath(f'{snapshot_id}.pkl')
    with open(path, 'wb') as o_:
        pickle.dump(data, o_)
    return snapshot_id


def get_snapshot_id():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')


def main():
    st.set_page_config(
        page_title='snap',
        page_icon='.logo.png',
        layout='wide',
        initial_sidebar_state='auto'
    )

    with st.sidebar:
        snapshot_slot = st.empty()
        snapshot_id = snapshot_slot.selectbox('choose snapshots', ['new'] + get_snapshots())
        is_new = snapshot_id == 'new'
        st.markdown('---')
        if is_new:
            a = st.number_input('a', -1., 1., 0.1)
            b = st.number_input('b', -1., 1., 0.9)
            if st.button('take snapshot.'):
                snapshot_id = save_data((a, b))
                st.info(f'snapshot id: {snapshot_id}')
                # Update selectbox
                snapshot_slot.selectbox('snapshots', ['new'] + get_snapshots())
        else:
            a, b = get_data(snapshot_id)
            st.write(f'a = {a}')
            st.write(f'b = {b}')

    display(a, b)


if __name__ == '__main__':
    main()