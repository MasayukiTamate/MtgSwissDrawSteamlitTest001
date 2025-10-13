'''
MTGスイスドロー大会の成績管理アプリ v0.002

2025 10 13 破壊と再生
'''

import streamlit as st
from streamlit_option_menu import option_menu

#フラグとカウンター
if "deleteFlag" not in st.session_state:
    st.session_state["deleteFlag"] = 0

"プレイヤーの追加と削除ボタンの初期化"
topplayertuikabotton = st.columns(2)

if topplayertuikabotton[0].button("プレイヤーの追加", key=99):
    st.session_state["count"] += 1