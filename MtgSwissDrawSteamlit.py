'''
MTGスイスドロー大会の成績管理アプリ

2025 09 11: Streamlit版
'''
import const
import streamlit as st
from streamlit_option_menu import option_menu

st.markdown(const.HIDE_ST_STYLE, unsafe_allow_html=True)

'''/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
selected = option_menu(**const.OPTION_MENU_CONFIG)
st.set_page_config(**const.SET_PAGE_CONFIG)
グローバル変数
プレイヤーネーム
仮ネーム
プレイヤーデータ[名前、勝ち点、マッチポイント%、オポメント%、対戦履歴[]]

kari=tentative=before=仮
'''
playerName = []
playerNameKari = []
playerData = []
'''/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
関数
taisen=match=duel=fight=battle=Showdown=対戦
kime=decision=decide=determine=designation=決め
Hyouji=Display=Show=表示
katimake=winlose=勝敗
Seiseki=Record=Performance=成績
narabi=arrangement=liningUp=並び
def BattleDecision(pd): #対戦決め
def BattleBottomDisplay(s, name): #対戦ボタン表示
def BattleDisplay(battlerLiningUp): #対戦表示
/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
'''
def addplayer(n):
    '''
    プレイヤーデータ追加
    n=名前
    '''
    playerData.append({
        "名前": n,
        "勝ち点": 0,
        "マッチポイント％":0.000,
        "オポメント％":0.000,
        "対戦履歴":[]
    })
    pass

def taisenKime(pd):
    '''
    対戦決め
    pd=playerDataプレイヤーデータ
    戻り値=対戦list
    '''
    taisenNarabi = []

    for i in pd:
        taisenNarabi.append(i["名前"])

    return taisenNarabi

def taisenBottonHyouji(s, namae):
    '''
    対戦ボタンを作成し描画する
    s=streamlit
    namae=名前
    戻り値=名前
    '''
    n = namae + "１戦目"
    if s.button(f"{namae}が勝った"):
        st.session_state[n] = st.session_state[n] + 1
        st.write(n)

    return namae
'''
対戦ボタンを押すことで"引き分け"や"○○の勝ち"とリアルタイムに表示がされる
End BattleButtonDisplay
'''
def taisenHyouji(taisenNarabi):#対戦表示
    '''
    対戦表示
    taisenNarabi=対戦list
    n席：A vs B
    '''

    seki = int(len(taisenNarabi) // 2)

    sekiNo = 0
    if len(taisenNarabi) > 1:
        for i in range(0, seki):
            st.write(f"{i + 1}席： {taisenNarabi[sekiNo]} vs {taisenNarabi[sekiNo + 1]}")
            sekiNo = sekiNo + 2

    if len(taisenNarabi) % 2:
            st.write(f"{seki + 1}席： {taisenNarabi[sekiNo]} vs byb")

    pass
'''
カラムを使いたい
END taisenHyouji(taisenNarabi)
'''
def taisenkatimake(n, kati):#勝敗
    '''
    対戦勝敗
    n=対戦list
    kati=勝利数list
    
    ボタンが押されることで勝利数が増える
    '''
    st.write(kati)
    if len(n) > 0:#エラー回避用式
        c = st.columns(len(n))

        kazu = 0
        for i, j, k in zip(c, n, kati):

            i.write(f"{j}の勝利数: {k}")

            kazu = kazu + 1

    pass



def SeisekiHyouji(itu):#成績表示
    '''
    成績表示
    itu=いつ."一回戦終了時"や"最終"
    '''
    text = itu + "成績"
    st.write(text)
    for i in playerData:
        st.write(f"名前:{i["名前"]}　勝ち点:{i["勝ち点"]}　MP%:{i["マッチポイント％"]}　OP%:{i["オポメント％"]}　{i["対戦履歴"]}")
    pass
'''/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
基礎コード
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
'''

#フラグとカウンター
if "deleteFlag" not in st.session_state:
    st.session_state["deleteFlag"] = 0
if 'count' not in st.session_state:
    st.session_state["count"] = 3
if st.session_state["deleteFlag"] > 0:
    st.session_state["deleteFlag"] = 0

st.title("MTGスイスドロー大会成績管理アプリ")
st.caption("by SmeatlitTools") 
st.write("プレイヤーの名前を入力してください")
topplayertuikabotton = st.columns(2)

#プレイヤー追加、削除ボタン
'''
カウンターはsession_stateで更新しても値を保持できるようにしている
プレイヤーを追加のボタンを押すとcountが増え、for文で回してテキストインプットを表示
プレイヤーを削除のボタンを押すとcountが減り、for文で回す数が減る
addplayerを使ってplayerDataにプレイヤーを追加
※プレイヤーネームとプレイヤーデータが違うデータ構造になっているのは別々に扱いたいから
'''
if topplayertuikabotton[0].button("プレイヤーの追加", key=99):
    st.session_state["count"] += 1

if topplayertuikabotton[1].button("プレイヤーの削除", key=98):
    st.session_state["deleteFlag"] += 1
    if st.session_state["count"] > 0:
        st.session_state["count"] -= 1
beforName = ["たなか","やまだ","さかもと"]
for i in range(st.session_state["count"]):
    playerName.append( st.text_input("プレイヤー", beforName[i],key=i) )
    addplayer(i)



#プレイヤーネームとプレイヤーデータを紐づける


for pn, pd in zip(playerName, playerData):#
    pd["名前"] = pn


namae = []

for i in playerData:
    n = i["名前"] + "１戦目"
    namae.append(n)
    if n not in st.session_state:
        
        st.session_state[n] = 0


with st.expander("リフレッシュ", icon="👊"):

    st.button("一回戦の対戦相手をリフレッシュ")



taisenNa = taisenKime(playerData)
osareta = ""

taisenBottonCol = ""
if taisenNa:
    taisenBottonCol = st.columns(len(taisenNa))

for i, j in zip(taisenNa, taisenBottonCol):
    osareta = taisenBottonHyouji(j, i)

katimake = [0 for _ in range(len(playerData))]
st.write(katimake)

#対戦の勝ち負けに表示するためにsession_stateの値を入れる
for km, na in zip(katimake, namae):
    km = st.session_state[na]

for i, j in zip(playerData,namae):#なにもやっていない
    break

taisenHyouji(taisenNa)#対戦の表示
taisenkatimake(taisenNa, katimake)#対戦の勝ち負け


'''
sessio_state
'''
st.write(st.session_state)


#成績表示
SeisekiHyouji("一回戦終了時")
#最終成績表示
SeisekiHyouji("最終")



#magic mpc