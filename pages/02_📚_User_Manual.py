import streamlit as st

st.set_page_config(
    page_title="User Manual - MTG Swiss Draw Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📚 User Manual / 使用説明書")

tab_jp, tab_en = st.tabs(["🇯🇵 日本語", "🇺🇸 English"])

# --- 日本語 ---
with tab_jp:
    st.markdown("""
    ### 大会運営の流れ

    #### 1. プレイヤーの登録
    *   サイドバーの **「➕ プレイヤー追加」** 欄に名前を入力します。
    *   複数人を一度に追加する場合は、名前をスペース、カンマ（`,`）、読点（`、`）などで区切ってください。
    *   参加者一覧から、名前の間違いがあったプレイヤーを削除することもできます。

    #### 2. ラウンド（回戦）の開始
    *   プレイヤーが2名以上登録されたら、**「次の一回戦を開始」** ボタンを押します。
    *   スイスドローのルールに基づき、対戦カードが自動的に作成されます。

    #### 3. 対戦結果の入力
    *   各対戦カードの下にあるセレクトボックスから、試合スコアを選択します（例: `2-0`, `2-1` など）。
    *   **「結果を報告」** ボタンを押すと、その試合のスコアが確定します。
    *   入力ミスをした場合は、中央に表示される **「修正(Reset)」** ボタンを押すと、未確定状態に戻すことができます。

    #### 4. 大会の進行と終了
    *   現在のラウンドの全試合が終了したら、再び **「次のラウンドを開始」** ボタンが押せるようになります。
    *   第3ラウンド以降になると、**「大会を終了して結果を見る」** ボタンが表示されます。
    *   途中で大会を切り上げて最終順位を出したい場合や、全ラウンドが終了した場合に押してください。

    #### 5. 結果発表
    *   最終順位表と、全プレイヤーの対戦履歴が表示されます。
    *   **「新しい大会を始める」** ボタンを押すと、全てのデータがリセットされて最初に戻ります。

    ### ヒント
    *   サイドバーを閉じてしまった場合は、左上の **「>」** アイコンを押すか、メイン画面の **「表示設定」** で調整してください。
    """)

# --- English ---
with tab_en:
    st.markdown("""
    ### Tournament Operation Flow

    #### 1. Registering Players
    *   Enter names in the **"➕ Add Player"** section in the sidebar.
    *   To add multiple players at once, separate names with spaces, commas (`,`), or Japanese ideographic commas (`、`).
    *   You can remove any player from the participant list if they were registered incorrectly.

    #### 2. Starting a Round
    *   Once 2 or more players are registered, click the **"Start Next Round"** button.
    *   Matchups will be automatically generated based on Swiss Draw rules.

    #### 3. Entering Match Results
    *   Select the match score from the dropdown menu below each matchup (e.g., `2-0`, `2-1`).
    *   Click the **"Report Result"** button to confirm the score for that match.
    *   If you make an entry error, click the **"Correction (Reset)"** button in the center to return the match to an unconfirmed state.

    #### 4. Progressing and Ending the Tournament
    *   Once all matches in the current round are finished, the **"Start Next Round"** button becomes clickable again.
    *   From Round 3 onwards, the **"End Tournament and View Results"** button will appear.
    *   Click this when you want to terminate the tournament midway or when all rounds are completed.

    #### 5. Results Announcement
    *   The final standings and match histories for all players will be displayed.
    *   Click the **"Start New Tournament"** button to reset all data and start over.

    ### Tips
    *   If you accidentally close the sidebar, click the **">"** icon at the top left or adjust the position via the **"Display Settings"** on the main screen.
    """)
