import sqlite3
import streamlit as st
import hashlib
from config import set_page_config
set_page_config()

# SQLiteデータベースに接続する関数
def connect_db():
    return sqlite3.connect('omiyapay.db')

# データベースのテーブルを作成
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL DEFAULT 100.0  -- 初期残高を100 Coinに設定
    );
    ''')
    conn.commit()
    conn.close()

# パスワードハッシュ化関数
def hash_password(password):
    # Saltを使ってハッシュ化を強化することを推奨
    salt = "your_salt"  # 塩を固定にするのではなく、ランダムに生成することをお勧めします
    return hashlib.sha256((salt + password).encode()).hexdigest()

# ユーザー登録関数
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Streamlit UI
st.title("新規登録")

# データベースのテーブル作成
create_tables()

# ユーザー登録
with st.form("register_form"):
    new_username = st.text_input("新規ユーザー名", key="new_username")
    new_password = st.text_input("新規パスワード", type='password', key="new_password")
    register_button = st.form_submit_button("登録")
    
    if register_button:
        if new_username and new_password:
            if register_user(new_username, new_password):
                st.success("ユーザー登録成功！ 初期残高として100 Coinが付与されました。")
                st.session_state.username = new_username  # 登録したユーザー名をセッションに保存
                st.session_state.page = 'dashboard'  # ダッシュボードページへ移動するための状態を更新
            else:
                st.error("ユーザー名がすでに存在します。別のユーザー名を試してください。")
        else:
            st.error("ユーザー名とパスワードは必須です。")
