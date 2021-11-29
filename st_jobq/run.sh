#!/bin/bash

echo $PWD

python job_queue.py &
python worker.py &
streamlit run app.py