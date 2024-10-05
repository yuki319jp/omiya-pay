import sqlite3
import streamlit as st
import hashlib
from config import set_page_config
set_page_config()

def connect_db():
    return sqlite3.connect('omiyapay.db')

# パスワードハッシュ化関数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ログイン関数
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    result = cursor.fetchone()
    conn.close()
    return result

# セッションステートの初期化
if 'username' not in st.session_state:
    st.session_state.username = None

if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# ログインページ
st.title("OmiyaPay - ログイン")
username = st.text_input("ユーザー名")
password = st.text_input("パスワード", type='password')

if st.button("ログイン"):
    try:
        user = login_user(username, password)
        if user:
            st.session_state.username = username
            st.session_state.is_logged_in = True
            st.success(f"ようこそ、{username}さん！ ダッシュボードに移動して始めよう！")
            st.balloons()
        else:
            st.error("ユーザー名またはパスワードが間違っています。")
    except Exception as e:
        st.error(f"ログイン中にエラーが発生しました: {e}")
