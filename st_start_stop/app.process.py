import multiprocessing
import time

import streamlit as st


class Worker(multiprocessing.Process):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.should_stop = multiprocessing.Event()
        self.counter = multiprocessing.Value('i', 0)
        
    def run(self):
        while not self.should_stop.wait(0):
            time.sleep(1)
            self.counter.value += 1

def main():
    if 'worker' not in st.session_state:
        st.session_state.worker = None
    worker: Worker = st.session_state.worker

    with st.sidebar:
        if st.button('Start worker', disabled=worker is not None):
            worker = st.session_state.worker = Worker(daemon=True)
            worker.start()
            st.experimental_rerun()
            
        if st.button('Stop worker', disabled=worker is None):
            worker.should_stop.set()
            worker.join()
            worker = st.session_state.worker = None
            st.experimental_rerun()


    if worker is None:
        st.markdown('No worker running.')
    else:
        st.markdown(f'worker: {worker.pid}')
        placeholder = st.empty()
        while worker.is_alive():
            placeholder.markdown(f'counter: {worker.counter.value}')
            time.sleep(1)


if __name__ == '__main__':
    main()
