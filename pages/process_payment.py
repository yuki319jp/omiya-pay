import sqlite3
import streamlit as st
from config import set_page_config
import cv2
import numpy as np
from pyzbar.pyzbar import decode

set_page_config()

# SQLiteデータベースの接続
def connect_db():
    return sqlite3.connect('omiyapay.db')

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
st.title("QR決済 - 支払い処理")

# ユーザー名を取得
username = st.session_state.get('username', None)
if not username:
    st.error("ログインしてください。")
    st.stop()

# カメラ入力を取得
camera_input = st.camera_input("QRコードをスキャンしてください")

if camera_input is not None:
    # 画像を読み込む
    image = cv2.imdecode(np.frombuffer(camera_input.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # QRコードをデコード
    decoded_objects = decode(image)

    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            st.success(f"QRコードから読み取った情報: {qr_data}")
            
            # QRコードの情報を解析
            try:
                # QRコードが期待する形式: 'receiver_username, amount'
                receiver, amount_str = qr_data.split(',')
                amount = float(amount_str)

                if st.button("支払いを実行"):
                    if receiver and amount > 0:
                        success, message = send_funds(username, receiver, amount)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("受取人と金額は必須です。")
            except ValueError:
                st.error("QRコードの情報が正しくありません。受取人と金額をカンマで区切って入力してください。")
    else:
        st.warning("QRコードが認識できませんでした。再度スキャンしてください。")
