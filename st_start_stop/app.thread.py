import threading
import time

import streamlit as st


class Worker(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.should_stop = threading.Event()
        
    def run(self):
        while not self.should_stop.wait(0):
            time.sleep(1)
            self.counter += 1

def main():
    if 'worker' not in st.session_state:
        st.session_state.worker = None
    worker = st.session_state.worker

    # worker を制御（起動/停止）する部分
    with st.sidebar:
        if st.button('Start worker', disabled=worker is not None):
            # daemon=True とすることで、Ctrl+C で終了できるようにする
            worker = st.session_state.worker = Worker(daemon=True)
            worker.start()
            st.experimental_rerun()
            
        if st.button('Stop worker', disabled=worker is None):
            worker.should_stop.set()
            worker.join()
            worker = st.session_state.worker = None
            st.experimental_rerun()
    
    # worker の状態を表示する部分
    if worker is None:
        st.markdown('No worker running.')
    else:
        st.markdown(f'worker: {worker.getName()}')
        placeholder = st.empty()
        while worker.is_alive():
            placeholder.markdown(f'counter: {worker.counter}')
            time.sleep(1)


if __name__ == '__main__':
    main()