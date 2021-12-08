import streamlit as st


def login():
    placeholder = st.empty()
    with placeholder.form('login'):
        password = st.text_input('パスワード', type='password')
        st.form_submit_button('ログイン')

    if password == 'password':
        placeholder.empty()
        return True
    else:
        st.write('パスワードが違います')
        return False


def main():
    loggedin = login()
    if loggedin:
        st.write('Authenticated!')
        number = st.number_input('number')
        st.write(number)
            


if __name__ == '__main__':
    main()