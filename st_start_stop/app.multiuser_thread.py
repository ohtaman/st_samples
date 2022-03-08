import dataclasses
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


@st.experimental_singleton
@dataclasses.dataclass
class ThreadManager:
    worker = None
    
    def get_worker(self):
        return self.worker
    
    def is_running(self):
        return self.worker is not None and self.worker.is_alive()
    
    def start_worker(self):
        if self.worker is not None:
            self.stop_worker()
        self.worker = Worker(daemon=True)
        self.worker.start()
        return self.worker
    
    def stop_worker(self):
        self.worker.should_stop.set()
        self.worker.join()
        self.worker = None



def main():
    thread_manager = ThreadManager()

    with st.sidebar:
        if st.button('Start worker', disabled=thread_manager.is_running()):
            worker = thread_manager.start_worker()
            st.experimental_rerun()
            
        if st.button('Stop worker', disabled=not thread_manager.is_running()):
            thread_manager.stop_worker()
            st.experimental_rerun()
    
    if not thread_manager.is_running():
        st.markdown('No worker running.')
    else:
        worker = thread_manager.get_worker()
        st.markdown(f'worker: {worker.getName()}')
        placeholder = st.empty()
        while worker.is_alive():
            placeholder.markdown(f'counter: {worker.counter}')
            time.sleep(1)


if __name__ == '__main__':
    main()