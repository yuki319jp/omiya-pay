import sqlite3
import streamlit as st
from config import set_page_config
set_page_config()

# SQLiteデータベースの接続
def connect_db():
    return sqlite3.connect('omiyapay.db')

# 残高取得関数
def get_balance(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
    balance = cursor.fetchone()
    conn.close()
    return balance[0] if balance else None

# 資金送信関数
def send_funds(sender, receiver, amount):
    conn = connect_db()
    cursor = conn.cursor()

    # 残高取得
    cursor.execute("SELECT balance FROM users WHERE username=?", (sender,))
    sender_balance = cursor.fetchone()
    
    if sender_balance and sender_balance[0] >= amount:
        # 残高が足りている場合
        cursor.execute("UPDATE users SET balance = balance - ? WHERE username=?", (amount, sender))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, receiver))
        conn.commit()
        conn.close()
        return True, "送金成功！"
    else:
        conn.close()
        return False, "残高が足りません。"

# Streamlit UI
st.title("ダッシュボード")

# ユーザー名がセッションステートに存在するか確認
if 'username' in st.session_state:
    username = st.session_state.username
else:
    st.error("ログインしてください。")
    st.stop()  # ログインしていない場合、以降の処理を停止

# 残高表示
balance = get_balance(username)
st.write(f"残高: {balance} Coin")

# 資金送信フォーム
with st.form("send_funds"):
    receiver = st.text_input("受取人のユーザー名", key="receiver")
    amount = st.number_input("送金額", min_value=0.0, step=1.0)
    send_button = st.form_submit_button("送金")

    if send_button:
        if receiver and amount > 0:
            success, message = send_funds(username, receiver, amount)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("受取人と送金額を正しく入力してください。")
