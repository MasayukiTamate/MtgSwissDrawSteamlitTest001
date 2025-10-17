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
        self.winCountEvery = []
        self.matchPointPar = 0.00
        self.opponentPar = 0.00
        self.opponentHistory = []
        pass

class SeatData():
    def __init__(self, pd):

        
        count = int(len(pd) // 2)
        if len(pd) % 2:
            count = count + 1
        self.CountSeat = count
        count = count - 1
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

tentative = []

WinLose = []
wiLo = []
for _ in range(len(pData)):
    wiLo.append(0)

WinLose.append(wiLo)

if "WinLose" not in st.session_state:
    st.session_state["WinLose"] = 0

st.write("試合１")
sData = SeatData(pData)

count = 0
for pd in pData:
    pd.winCountEvery.append(0)
for couS in range(sData.CountSeat):
    st.write("席" + str(couS + 1) + "つ目")
    st.write(f"{pData[count].name}")
    st.write("勝ち")
    st.write(pData[count].winCountEvery[0])
    count = count + 1
    if count < len(pData):
        st.write(f"{pData[count].name}")
        count = count + 1

st.write("試合１の成績")
tentative.append(pData.copy())
for pd in tentative[0]:
    st.write(f"{pd.name} 勝利点：{pd.winPoint} ウィンP％：{pd.matchPointPar} オポP％：{pd.opponentPar} 敵履歴；{pd.opponentHistory}")
st.write("試合２")
st.write("試合３")
pData[0].name = "ありよし"
st.write("最終成績")
for pd in pData:
    st.write(f"{pd.name} 勝利点：{pd.winPoint} ウィンP％：{pd.matchPointPar} オポP％：{pd.opponentPar} 敵履歴；{pd.opponentHistory}")
'''
lenName = []
for pd in pData:
    lenName.append(len(pd.name))
" " * lenName.max() - len(pd.name) 
'''