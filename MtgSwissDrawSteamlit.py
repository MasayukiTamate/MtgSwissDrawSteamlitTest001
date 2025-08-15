import streamlit as st

playerName = []
playerNameKari = []

def SeisekiHyouji(itu):
    text = itu + "成績"
    st.write(text)
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

st.write(playerName)


st.button("一回戦")


SeisekiHyouji("最終")
SeisekiHyouji("一回戦終了時")
SeisekiHyouji("最終")