import streamlit as st
import hashlib


SALT = 'aiueo:'
# 'password' をハッシュ化したもの
HASHED_PASSWORD = '246380e2b28d0898ff4b214ced62e851fee242112ae9a01a6ab49216194c0d7a'


def get_hash(password):
    return hashlib.sha256((SALT + password).encode('utf-8')).hexdigest()


def check_password(password, hashed_password):
    return get_hash(password) == hashed_password


def login():
    placeholder = st.empty()
    with placeholder.form('login'):
        password = st.text_input('パスワード', type='password')
        st.form_submit_button('ログイン')

    if check_password(password, HASHED_PASSWORD):
        placeholder.empty()
        return True
    else:
        if password:
            st.write('パスワードが違います')
        return False


def main():
    loggedin = login()
    if loggedin:
        st.write('Authenticated!')
            

if __name__ == '__main__':
    main()