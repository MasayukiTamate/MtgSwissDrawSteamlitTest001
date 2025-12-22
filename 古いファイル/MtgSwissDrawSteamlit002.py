'''
MTGスイスドロー大会の成績管理アプリ v0.002

2025 10 13 破壊と再生
'''
'''
課題
プレイヤーの　　　名前のテキストボックス反映
クラス成績表示
成績表示での対戦相手履歴の表示の仕方
'''
import streamlit as st
from streamlit_option_menu import option_menu

def bou(t):
    if t == "0":
        st.write("――――――――――――――――――――――――――――――――――――――――――――――")
    elif t == "1":
        st.write("========================================================================")
    pass
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
class Result():
    def __init__(self, no):
        self.countDuel = no
        self.countDuelName = "第" + str(no) + "試合" + "の成績"
        self.resultSeatName = ["名前","勝利点","勝ち％","オポ％","敵履歴"]
        self.resultData = []
        self.seatcount = 5
        pass
    def ShowName(self):
        st.write(self.countDuelName)
        resultSeatNameList = st.columns(5)

        for rsnl, rsn in zip(resultSeatNameList, self.resultSeatName):
            rsnl.write(rsn)
        pass
    def Show(self):
        resultSeatColumns = st.columns(self.seatcount)

        for rd in self.resultData:
            print(rd)
            for rsc, r in zip(resultSeatColumns, rd):
                rsc.write(r)
        pass
    def SetResultData(self, data):
        count = 0
        flag = False
        if data[0] == 0:#追加モードと上書きモード
            flag = True
        data3 = []
        for d in data[5:]:
            for dd in d:
                data3.append(dd)
        data2 = data[1:5] + data3
        print(f"{data3=}")
        print(f"{data2=}")
        if flag:
            self.resultData.append(data2)
        count = 4

        for d in data[5:]:

            count = count + 1
        self.seatcount = count
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

bou("1")

st.write("試合１")
sData = SeatData(pData)

count = 0
for pd in pData:
    pd.winCountEvery.append(0)

#席
for couS in range(sData.CountSeat):
    st.write("第" + str(couS + 1) + "席目")
    st.write(f"{pData[count].name}")

    #分岐
    if count + 1 < len(pData):
        st.write("勝ち")
        st.write(pData[count].winCountEvery[0])
        count = count + 1
        st.write("VS")
        st.write(pData[count].name)
        st.write("勝ち")
        st.write(pData[count].winCountEvery[0])
        count = count + 1
    else:
        st.write("不戦勝")

    bou("0")
#敵履歴代入

count = 0
for couS in range(sData.CountSeat):

    if count + 1 < len(pData):
        pData[count].opponentHistory.append( pData[count +1].name)
        pData[count + 1].opponentHistory.append( pData[count].name)
    
    else:
        pData[count].opponentHistory.append("BYEさん")

    count = count + 2
        
bou("1")
#成績表示　クラス化


result1st = Result(1)
result1st.ShowName()

for pd in pData:
    list1 = [0, pd.name, pd.winPoint, pd.matchPointPar, pd.opponentPar, pd.opponentHistory]
    result1st.SetResultData(list1)

result1st.Show()



bou("0")
st.write("試合２")
bou("0")
st.write("試合３")
bou("1")
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