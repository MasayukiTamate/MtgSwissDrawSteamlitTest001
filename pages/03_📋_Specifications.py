import streamlit as st

st.set_page_config(
    page_title="Specifications - MTG Swiss Draw Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📋 Specifications / 仕様説明書")

tab_jp, tab_en = st.tabs(["🇯🇵 日本語", "🇺🇸 English"])

# --- 日本語 ---
with tab_jp:
    st.markdown("""
    ### システム仕様と計算ルール

    #### 1. 対戦形式 (Match Format)
    *   **Best of 3 (BO3)**: 1マッチ最大3ゲーム（2本先取）を前提としています。
    *   ゲームスコア（2-0, 2-1, 1-1 など）を記録することで、タイブレーカーの計算に使用します。

    #### 2. スイスドロー・ロジック (Pairing Logic)
    *   勝ち点が近い者同士を優先的にマッチングします（マッチポイント・ブラケット）。
    *   **重複対戦の回避**: 大会中、同じ相手と2回当たることはありません。
    *   **Bye（不戦勝）**: 
        *   プレイヤーが奇数の場合、その回戦で最も順位が低い（かつ、まだByeを経験していない）プレイヤーにByeが与えられます。
        *   Byeは「マッチ勝利（3点）」としてマッチポイントには加算されますが、**タイブレーカー（MW%, GW%等）の計算からは完全に除外**されます。
        *   つまり、不戦勝以外の「実際にプレイした対戦成績」のみで勝率が算出されます。

    #### 3. 順位決定ルール (Tie-breakers)
    MTGの公式競技ルールに準拠した以下の優先順位で決定します。
    (※BYEは以下の計算の分母・分子には含まれません)

    1.  **マッチポイント (Match Points)**
        *   勝利：3点、引き分け：1点、敗北：0点。
    2.  **OMW% (Opponent Match Win Percentage)**
        *   対戦相手のマッチ勝率の平均。
        *   対戦相手の勝率が0.33未満の場合は0.33として計算されます（フロア値）。
    3.  **GW% (Game Win Percentage)**
        *   自身のゲーム勝率。
        *   獲得ゲーム数 / 全ゲーム数。
    4.  **OGW% (Opponent Game Win Percentage)**
        *   対戦相手のゲーム勝率の平均。

    #### 4. クラス設計 (Software Architecture)
    アプリは以下のオブジェクト指向モデルで構築されています。
    *   `PlayerData`: プレイヤーの基本データと統計（各タイブレーカーの計算）を保持。
    *   `RoundMatch`: 1つの対戦カードと結果入力を管理。
    *   `TournamentManager`: 参加者リスト、ラウンド履歴、ペアリング生成、全体の状態を統合管理。

    #### 5. テクノロジー
    *   **Frontend/Backend**: Streamlit (Python)
    *   **Data Analysis**: Pandas
    *   **Styling**: Vanilla CSS (CSS Hack for sidebar control)
    """)

# --- English ---
with tab_en:
    st.markdown("""
    ### System Specifications and Calculation Rules

    #### 1. Match Format
    *   **Best of 3 (BO3)**: Assumes a maximum of 3 games per match (first to win 2 games).
    *   Game scores (2-0, 2-1, 1-1, etc.) are recorded and used for tie-breaker calculations.

    #### 2. Pairing Logic
    *   Matches players with similar match points (Match Point Brackets).
    *   **Avoid Repeat Matchups**: Players will not be paired against the same opponent more than once in a single tournament.
    *   **Bye (Free Win)**: 
        *   If the number of players is odd, a Bye is awarded to the lowest-ranked player in that round who has not yet received a Bye.
        *   A Bye is added to the Match Points (3 pts) for standings, but **completely excluded from tie-breaker calculations (MW%, GW%, etc.)**.
        *   This means win percentages are calculated based only on "actually played matches."

    #### 3. Standings Rules (Tie-breakers)
    Determined by the following order of priority, based on official MTG competitive rules:
    (*Byes are excluded from the denominators and numerators of these calculations)

    1.  **Match Points**
        *   Win: 3 pts, Draw: 1 pt, Loss: 0 pts.
    2.  **OMW% (Opponent Match Win Percentage)**
        *   The average match win percentage of opponents.
        *   If an opponent's win percentage is below 0.33, it is treated as 0.33 (floor value).
    3.  **GW% (Game Win Percentage)**
        *   The player's own game win percentage.
        *   Games Won / Total Games Played.
    4.  **OGW% (Opponent Game Win Percentage)**
        *   The average game win percentage of opponents.

    #### 4. Class Design (Software Architecture)
    The app is built using the following Object-Oriented model:
    *   `PlayerData`: Holds basic player data and statistics (calculates each tie-breaker).
    *   `RoundMatch`: Manages a single matchup and its result entry.
    *   `TournamentManager`: Integrates and manages the participant list, round history, pairing generation, and overall state.

    #### 5. Technology Stack
    *   **Frontend/Backend**: Streamlit (Python)
    *   **Data Analysis**: Pandas
    *   **Styling**: Vanilla CSS (CSS hacks for sidebar control)
    """)
