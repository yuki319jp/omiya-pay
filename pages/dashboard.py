import sqlite3
import streamlit as st

# SQLiteデータベースの接続
conn = sqlite3.connect('omiyapay.db')
cursor = conn.cursor()

# 残高取得関数
def get_balance(username):
    cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
    return cursor.fetchone()[0]

# ユーザー存在確認関数
def user_exists(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone() is not None

# 資金送信関数
def send_funds(sender, receiver, amount):
    cursor.execute("SELECT balance FROM users WHERE username=?", (sender,))
    sender_balance = cursor.fetchone()[0]

    if not user_exists(receiver):
        return False, "送信先ユーザーが存在しません。"

    if sender_balance < amount:
        return False, "残高不足です。"

    # 送金処理
    cursor.execute("UPDATE users SET balance = balance - ? WHERE username=?", (amount, sender))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, receiver))
    cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)", (sender, receiver, amount))
    conn.commit()
    return True, "送信成功！"

# Streamlit UI
st.title("ダッシュボード")

# セッションステートを使用してユーザー情報を保持
if 'username' in st.session_state:
    username = st.session_state.username
    st.success(f"ようこそ、{username}さん！")
    balance = get_balance(username)
    st.write(f"現在の残高: {balance} 仮想通貨")

    # 資金送信機能
    receiver = st.text_input("送信先ユーザー名", key="receiver_username")
    amount = st.number_input("送信金額", min_value=0.0, step=0.1, key="send_amount")
    if st.button("送信"):
        success, message = send_funds(username, receiver, amount)
        if success:
            st.success(message)
        else:
            st.error(message)
else:
    st.error("ログインしていません。ログインページに移動してください。")

# データベース接続を閉じる
conn.close()
