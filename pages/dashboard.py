import sqlite3
import streamlit as st
import hashlib
from config import set_page_config
set_page_config()


# データベースに接続する関数
def connect_db():
    return sqlite3.connect('omiyapay.db')

# 残高を取得する関数
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

    # 残高を取得
    cursor.execute("SELECT balance FROM users WHERE username=?", (sender,))
    sender_balance = cursor.fetchone()
    
    if sender_balance and sender_balance[0] >= amount:
        # 残高が足りている場合
        cursor.execute("UPDATE users SET balance = balance - ? WHERE username=?", (amount, sender))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, receiver))
        
        # トランザクションを履歴に記録
        cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)", (sender, receiver, amount))
        
        conn.commit()
        conn.close()
        return True, "送金成功！"
    else:
        conn.close()
        return False, "残高が足りません。"

# ユーザーの入出金履歴を取得する関数
def get_transaction_history(username):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT sender, receiver, amount, timestamp FROM transactions 
        WHERE sender=? OR receiver=? ORDER BY timestamp DESC
        """, (username, username))
        history = cursor.fetchall()
    except Exception as e:
        st.error(f"履歴の取得中にエラーが発生しました: {e}")
        history = []
    finally:
        conn.close()
    return history

# パスワード変更関数
def change_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("ダッシュボード")

# ユーザー名がセッションステートに存在するか確認
if 'username' in st.session_state:
    username = st.session_state.username
else:
    st.error("ログインしてください。")
    st.stop()

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

# パスワード変更フォーム
st.write("---")
st.header("パスワード変更")

with st.form("change_password"):
    new_password = st.text_input("新しいパスワード", type='password')
    change_button = st.form_submit_button("変更")

    if change_button:
        if new_password:
            change_password(username, new_password)
            st.success("パスワードが変更されました。")
        else:
            st.error("新しいパスワードを入力してください。")

# 入出金履歴の表示
st.write("---")
st.header("入出金履歴")

transaction_history = get_transaction_history(username)
if transaction_history:
    for transaction in transaction_history:
        sender, receiver, amount, timestamp = transaction
        st.write(f"送金者: {sender}, 受取人: {receiver}, 金額: {amount} Coin, 時間: {timestamp}")
else:
    st.write("履歴がありません。")
