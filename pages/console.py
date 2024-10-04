import sqlite3
import streamlit as st
import hashlib

# SQLiteデータベースの接続
conn = sqlite3.connect('omiyapay.db')
cursor = conn.cursor()

# パスワードハッシュ化関数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 管理者のユーザー名とパスワード（実際のアプリでは安全に管理すること）
admin_username = "admin"
admin_password_hash = hash_password("adminパスワードをここに入力してください")  # ハッシュ化したパスワード

# 残高送金関数
def distribute_currency(amount):
    cursor.execute("UPDATE users SET balance = balance + ?", (amount,))
    conn.commit()

# 通貨を発行する関数
def issue_currency(username, amount):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, username))
    conn.commit()

# Streamlit UI
st.title("管理者コンソール")

# ログインフォーム
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.subheader("管理者ログイン")
    login_username = st.text_input("ユーザー名", value="", key="login_username")
    login_password = st.text_input("パスワード", type='password', key="login_password")

    if st.button("ログイン"):
        if (login_username == admin_username and
            hash_password(login_password) == admin_password_hash):
            st.session_state.logged_in = True
            st.success("ログイン成功！")
        else:
            st.error("ユーザー名またはパスワードが間違っています。")
else:
    # 管理者がログインしている場合のUI
    st.success("ログイン中...")
    
    # 通貨の発行
    st.subheader("通貨発行")
    issue_user = st.text_input("発行先ユーザー名")
    issue_amount = st.number_input("発行する通貨の量", min_value=1.0)
    
    if st.button("発行"):
        issue_currency(issue_user, issue_amount)
        st.success(f"{issue_amount} Coinが {issue_user} に発行されました。")

    # 通貨の全員分配
    st.subheader("全員に通貨を分配")
    distribute_amount = st.number_input("分配する通貨の量", min_value=1.0)
    
    if st.button("分配"):
        distribute_currency(distribute_amount)
        st.success(f"全員に {distribute_amount} Coinが分配されました。")

# データベース接続を閉じる
conn.close()
