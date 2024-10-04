import streamlit as st

# Streamlitのタイトル
st.set_page_config(page_title="OmiyaPay", layout="wide")

# ページのナビゲーション
page = st.sidebar.selectbox("ページ選択", ["ホーム", "新規登録", "ログイン", "ダッシュボード", "特権ユーザー"])

# 各ページの表示
if page == "ホーム":
    st.title("OmiyaPay - 仮想通貨取引サービス")
    st.markdown("各ページに移動して、新規登録、ログイン、ダッシュボードの機能をお試しください。")
elif page == "新規登録":
    import pages.register
elif page == "ログイン":
    import pages.login
elif page == "ダッシュボード":
    import pages.dashboard
elif page == "特権ユーザー":
    import pages.privileged
