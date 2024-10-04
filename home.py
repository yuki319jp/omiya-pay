import streamlit as st

# Streamlitのタイトル
st.set_page_config(page_title="<#375640>OmiyaPay", layout="wide")

# ページのナビゲーション
page = st.sidebar.selectbox("ページ選択", ["ホーム", "新規登録", "ログイン", "ダッシュボード","コンソール"])

# 各ページの表示
if page == "ホーム":
    st.title("OmiyaPay")
    st.markdown("## 大宮キャンパス独自決済サービス ")
    st.markdown("## やること一覧")

    st.markdown("### 初めての人")
    st.markdown("新規登録 または registerからアカウントを作成してください")
    st.markdown("その後ログイン または loginからログインしてください")
    st.markdown("その後ダッシュボードへ移動してください")

    st.markdown("### 二回目以降の人")
    st.markdown("ログイン または loginからログインしてください")
    st.markdown("その後ダッシュボードに移動してください")
    
    st.markdown("# Made by yuki319jp for Omiya Campus")


elif page == "新規登録":
    import pages.register
elif page == "ログイン":
    import pages.login
elif page == "ダッシュボード":
    import pages.dashboard
elif page == "コンソール":
    import pages.console
