import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
from config import set_page_config

set_page_config()

# QRコードを生成する関数
def generate_qr_code(data):
    img = qrcode.make(data)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

# Streamlit UI
st.title("QR決済")

# ユーザー名を取得
username = st.session_state.get('username', None)
if not username:
    st.error("ログインしてください。")
    st.stop()

st.write(f"ユーザー: {username}")

# 送金情報の入力
receiver = st.text_input("受取人のユーザー名")
amount = st.number_input("送金額", min_value=0.0, step=1.0)

if st.button("QRコードを生成"):
    if receiver and amount > 0:
        payment_info = f"{receiver},{amount}"  # 受取人のユーザー名と金額をカンマ区切りで結合
        qr_code_img = generate_qr_code(payment_info)

        st.image(qr_code_img, caption="スキャンして送金してください。", use_column_width=True)
        st.success("QRコードが生成されました！")
    else:
        st.error("受取人と送金額を正しく入力してください。")
