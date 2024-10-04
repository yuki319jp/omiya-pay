import sqlite3
import streamlit as st
import hashlib

# SQLiteデータベースの接続
conn = sqlite3.connect('omiyapay.db')
cursor = conn.cursor()

# パスワードハッシュ化関数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ログイン関数
def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return cursor.fetchone()

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
    user = login_user(username, password)
    if user:
        st.session_state.username = username
        st.session_state.is_logged_in = True
        st.success(f"ようこそ、{username}さん！ ダッシュボードに移動して始めよう！")
        
        # バルーンエフェクトを追加（オプション）
        st.balloons()
        
    else:
        st.error("ユーザー名またはパスワードが間違っています。")

# データベース接続を閉じる
conn.close()
