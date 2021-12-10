#!/bin/bash

python job_queue.py &
python worker.py &
streamlit run app.py