import streamlit as st

playerName = []
playerNameKari = []
playerData = []

def addplayer(n):
    playerData.append({
        "名前": n,
        "勝ち点": 0,
        "マッチポイント％":0.000,
        "オポメント％":0.000
    })
    pass
def taisenKime():
    pass

def SeisekiHyouji(itu):
    text = itu + "成績"
    st.write(text)
    for i in playerData:
        st.write(f"名前:{i["名前"]} 勝ち点:{i["勝ち点"]} MP%:{i["マッチポイント％"]} OP%:{i["オポメント％"]}")
    pass


if "deleteFlag" not in st.session_state:
    st.session_state["deleteFlag"] = 0
if 'count' not in st.session_state:
    st.session_state["count"] = 0

if st.session_state["deleteFlag"] > 0:
    st.session_state["deleteFlag"] = 0



if st.button("プレイヤーの追加", key=99):
    st.session_state["count"] += 1

if st.button("プレイヤーの削除", key=98):
    st.session_state["deleteFlag"] += 1
    if st.session_state["count"] > 0:
        st.session_state["count"] -= 1
for i in range(st.session_state["count"]):
    playerName.append( st.text_input("プレイヤー", i,key=i) )
    addplayer(i)



for i, j in zip(playerName, playerData):
    j["名前"] = i

#st.button("一回戦")

taisenKime()


SeisekiHyouji("一回戦終了時")
SeisekiHyouji("最終")



#magic mpc