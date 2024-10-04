import sqlite3
import streamlit as st
import hashlib

# SQLiteデータベースの接続
conn = sqlite3.connect('omiyapay.db')
cursor = conn.cursor()

# データベースのテーブルを作成
def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL DEFAULT 0.0
    );
    ''')
    
create_tables()

# パスワードハッシュ化関数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ユーザー登録関数
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Streamlit UI
st.title("新規登録")

# ユーザー登録
with st.form("register_form"):
    new_username = st.text_input("新規ユーザー名", key="new_username")
    new_password = st.text_input("新規パスワード", type='password', key="new_password")
    register_button = st.form_submit_button("登録")
    if register_button:
        if new_username and new_password:
            if register_user(new_username, new_password):
                st.success("ユーザー登録成功！")
                st.session_state.username = new_username  # 登録したユーザー名をセッションに保存
                st.query_params['page'] = 'dashboard'  # クエリパラメータを更新
                st.experimental_rerun()  # ページをリロードしてダッシュボードに遷移
            else:
                st.error("ユーザー名がすでに存在します。別のユーザー名を試してください。")
        else:
            st.error("ユーザー名とパスワードは必須です。")

# データベース接続を閉じる
conn.close()
