import multiprocessing
import time

import streamlit as st


class Worker(multiprocessing.Process):
    def __init__(self, should_stop, counter, **kwargs):
        super().__init__(**kwargs)
        self.should_stop = should_stop
        self.counter = counter
        
    def run(self):
        while not self.should_stop.value:
            time.sleep(1)
            self.counter.value += 1

def main():
    if 'worker' not in st.session_state:
        st.session_state.worker = None
    worker: Worker = st.session_state.worker

    with st.sidebar:
        if st.button('Start worker', disabled=worker is not None):
            should_stop = multiprocessing.Value('i', False)
            counter = multiprocessing.Value('i', 0)
            worker = st.session_state.worker = Worker(should_stop, counter, daemon=True)
            worker.start()
            
        if st.button('Stop worker', disabled=worker is None):
            worker.should_stop.value = True
            worker.join()
            worker = st.session_state.worker = None
            st.experimental_rerun()
    
    if worker is None:
        st.markdown('No worker')
    else:
        st.markdown(f'worker: {worker.pid}')
        placeholder = st.empty()
        while worker.is_alive():
            placeholder.markdown(f'counter: {worker.counter.value}')
            time.sleep(1)


if __name__ == '__main__':
    main()