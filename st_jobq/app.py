import streamlit as st

import job_queue


def show_result(job_id):
    job_result = job_queue.load_artifact(
        job_id=job_id,
        name='result'
    )
    st.markdown(f'## {job_id}')
    st.markdown(f'a: {job_result["a"]}')
    st.markdown(f'b: {job_result["b"]}')


def main():
    st.set_page_config(
        page_title='job',
        page_icon='.logo.png',
        layout='wide',
        initial_sidebar_state='auto'
    )

    with st.sidebar:
        task_type = st.radio('', ('show results', 'put a new job'))
        if task_type == 'show results':
            job_id = st.selectbox('job', job_queue.get_jobs())
        elif task_type == 'put a new job':
            with st.form(key='job_form'):
                a = st.number_input('a', -1., 1., 0.1)
                b = st.number_input('b', -1., 1., 0.9)
                submit = st.form_submit_button('submit')

    if task_type == 'show results':
        if not job_id:
            return
        show_result(job_id)
    elif task_type == 'put a new job':
        if submit:
            job_id = job_queue.put_job(a, b)
            st.info(f'job {job_id} submitted.')


if __name__ == '__main__':
    main()