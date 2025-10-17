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

beforName = ["たなか","やまだ","さかもと"]
pData = []

for beNe in beforName:
    pData.append(PlayerData(beNe))

st.title("MTGスイスドロー大会成績管理アプリ")
st.caption("by SmeatlitTools") 
st.write("プレイヤーの名前を入力してください")

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
if topplayertuikabotton[1].button("プレイヤーの削除", key=98):
    st.session_state["deleteFlag"] += 1
    if st.session_state["count"] > 0:
        st.session_state["count"] -= 1

#プレイヤーデータ初期化
for i in range(st.session_state["count"]):
    if i + 1> len(pData):
        pData.append(PlayerData("プレイヤー" + str(i + 1)))

#テキストボックス設置
count = 1
for i in range(st.session_state["count"]):
    st.text_input("プレイヤー", pData[i].name ,key=count + 100)
    count = count + 1



for pd in pData:
    st.write(f"{pd.name} 勝利点：{pd.winPoint} ウィンP％：{pd.matchPointPar} オポP％：{pd.opponentPar} 敵履歴；{pd.opponentHistory}")
'''
lenName = []
for pd in pData:
    lenName.append(len(pd.name))
" " * lenName.max() - len(pd.name) 
'''