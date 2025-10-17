'''
MTGスイスドロー大会の成績管理アプリ v0.002

2025 10 13 破壊と再生
'''

import streamlit as st
from streamlit_option_menu import option_menu

class PlayerData():
    def __init__(self, na):
        self.name = na
        self.winPoint = 0
        self.matchPointPar = 0.00
        self.opponentPar = 0.00
        self.opponentHistory = []
        pass


#フラグとカウンター
#人数をグローバルに
if 'count' not in st.session_state:
    st.session_state["count"] = 3
if "deleteFlag" not in st.session_state:
    st.session_state["deleteFlag"] = 0

"プレイヤーの追加と削除ボタンの初期化"
topplayertuikabotton = st.columns(2)

if topplayertuikabotton[0].button("プレイヤーの追加", key=99):
    st.session_state["count"] += 1
beforName = ["たなか","やまだ","さかもと"]

pData = []

for beNe in beforName:
    pData.append(PlayerData(beNe))
    
#テキストボックス設置
count = 1
for pd in pData:
    st.text_input("プレイヤー", pd.name,key=count + 100)
    count = count + 1
