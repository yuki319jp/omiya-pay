import streamlit as st
from PIL import Image  # PillowのImageモジュールをインポート

# ページの設定
st.set_page_config(
    page_title="OmiyaPay", 
    layout="wide",
    page_icon="omiya-pay.png"  # 画像パスを指定
)

# 画像の読み込み
image = Image.open('omiya-pay.png')


# サイドバーのナビゲーション
st.sidebar.title("ナビゲーション")
page = st.sidebar.selectbox("ページ選択", ["ホーム", "新規登録", "ログイン", "ダッシュボード", "QR決済", "コンソール"])

if page == "ホーム":
    st.title("OmiyaPay")
    st.markdown("ここはホームページです。")
    st.markdown("大宮キャンパス独自決済サービスです。")
elif page == "新規登録":
    import pages.register
elif page == "ログイン":
    import pages.login
elif page == "ダッシュボード":
    import pages.dashboard
elif page == "QR決済":
    import pages.qr_payment
elif page == "コンソール":
    import pages.console
