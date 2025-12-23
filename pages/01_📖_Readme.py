import streamlit as st
from config import AUTHOR_NAME, AUTHOR_LINK_MD, AUTHOR_NAME_EN, AUTHOR_LINK_MD_EN

st.set_page_config(
    page_title="Readme - MTG Swiss Draw Manager",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📖 Readme / はじめに")

tab_jp, tab_en = st.tabs(["🇯🇵 日本語", "🇺🇸 English"])

# --- 日本語 ---
with tab_jp:
    st.header("MTG Swiss Draw Manager (OOP Ver)")
    st.caption(f"By {AUTHOR_LINK_MD}")
    
    st.markdown(f"""
    ### 概要
    **MTG Swiss Draw Manager** は、Magic: The Gathering (MTG) の大会をスムーズに運営するためのスイスドロー管理アプリケーションです。
    個人主催の小さな大会や、コミュニティでのイベントに最適化されており、直感的な操作でペアリングから順位計算までを自動化します。

    ### 主な機能
    *   **プレイヤー管理**: 名前を入力するだけで簡単に登録。カンマやスペース区切りでの一括登録も可能です。
    *   **自動ペアリング**: スイスドロー形式に基づき、勝ち点の近いプレイヤー同士を自動でマッチングします。
        *   過去に対戦した相手とは当たらないように配慮されます。
        *   奇数人の場合は自動でBye（不戦勝）を設定します。
    *   **BO3対応の結果入力**: 2-0, 2-1, 1-1（引き分け）など、ゲームカウントを含めた詳細な結果入力が可能です。
    *   **本格的なタイブレーカー**: 順位決定には公式ルールに準拠した厳密な計算を行います。
        1.  マッチポイント (勝点)
        2.  OMW% (Opponent Match Win Percentage)
        3.  GW% (Game Win Percentage)
        4.  OGW% (Opponent Game Win Percentage)
    *   **使いやすいUI**:
        *   サイドバーでの設定・管理機能
        *   間違えた結果の「修正（Reset）」機能
        *   大会途中での終了・結果発表機能

    ### 作者について
    このアプリケーションは **{AUTHOR_LINK_MD}** によって開発されました。
    ユーザーの皆様からのフィードバックを元に、機能改善を続けています。
    """)

# --- English ---
with tab_en:
    st.header("MTG Swiss Draw Manager (OOP Ver)")
    st.caption(f"By {AUTHOR_LINK_MD_EN}")
    
    st.markdown(f"""
    ### Overview
    **MTG Swiss Draw Manager** is a Swiss Draw management application designed for running Magic: The Gathering (MTG) tournaments smoothly.
    It is optimized for small privately hosted tournaments and community events, automating everything from pairings to standings calculations with intuitive controls.

    ### Key Features
    *   **Player Management**: Easily register players by simply entering their names. Batch registration via comma or space separation is also supported.
    *   **Automatic Pairings**: Automatically matches players with similar match points based on Swiss Draw rules.
        *   Avoids repeat matchups against previous opponents.
        *   Automatically handles Bye (free win) for odd numbers of players.
    *   **BO3 Result Entry**: Supports detailed result entry including game counts like 2-0, 2-1, 1-1 (Draw).
    *   **Professional Tie-Breakers**: Standings are determined using strict calculations based on official rules.
        1.  Match Points
        2.  OMW% (Opponent Match Win Percentage)
        3.  GW% (Game Win Percentage)
        4.  OGW% (Opponent Game Win Percentage)
    *   **User-Friendly UI**:
        *   Sidebar for configuration and management.
        *   "Correction (Reset)" feature for erroneous result entries.
        *   Option to end the tournament midway and view final results.

    ### About the Author
    This application was developed by **{AUTHOR_LINK_MD_EN}**.
    We continue to improve features based on feedback from our users.
    """)
