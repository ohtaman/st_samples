import dataclasses
from dis import dis
import threading
import time

import streamlit as st


class Worker(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.should_stop = False
        
    def run(self):
        while not self.should_stop:
            time.sleep(1)
            self.counter += 1


def main():
    if 'worker' not in st.session_state:
        st.session_state.worker = None
    worker = st.session_state.worker

    with st.sidebar:
        if st.button('Create worker', disabled=worker is not None):
            worker = st.session_state.worker = Worker(daemon=True)
            worker.start()
            
        if st.button('Stop worker', disabled=worker is None):
            worker.should_stop = True
            worker.join()
            worker = st.session_state.worker = None
            st.experimental_rerun()
    
        if st.button('reload', disabled=worker is None):
            pass # just reload

    
    if worker is None:
        st.markdown('No worker')
    else:
        st.markdown(f'counter: {worker.counter}')
        

if __name__ == '__main__':
    main()