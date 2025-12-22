"""
MTGスイスドロー大会 成績管理アプリ 統合版 (OOP)
MtgSwissDrawIntegrated.py

概要:
    オブジェクト指向設計(OOP)に基づき、大会データ、プレイヤー、対戦ロジックをクラス管理します。
    StreamlitのUIはViewとして機能し、ロジックはModel(クラス)に集約されます。

作成日: 2025/12/22
"""

import streamlit as st
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Optional

# --- 定数定義 (const.pyの内容を統合) ---
SET_PAGE_CONFIG = {
    "page_title": "MTG Swiss Draw Manager",
    "page_icon": "🃏",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# デフォルトのスタイル非表示設定
HIDE_ST_STYLE = """
<style>
div[data-testid="stToolbar"] {visibility: hidden;}
div[data-testid="stDecoration"] {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

# --- クラス定義 (Model) ---

@dataclass
class MatchResult:
    """
    対戦結果を表すデータクラス
    """
    opponent_name: str
    result: str  # "WIN", "LOSE", "DRAW", "BYE"

class PlayerData:
    """
    プレイヤー個人を表現するクラス
    
    属性:
        name (str): プレイヤー名
        id (int): 識別ID
        win_points (int): 勝ち点 (勝:3, 分:1, 負:0)
        match_win_count (int): 勝利数
        history (List[MatchResult]): 対戦履歴
    """
    def __init__(self, name: str, player_id: int):
        self.name = name
        self.id = player_id
        self.win_points = 0
        self.match_win_count = 0  # 純粋な勝利回数
        self.history: List[MatchResult] = []

    def has_played_against(self, opponent_name: str) -> bool:
        """指定した名前の相手と既に対戦済みか確認する"""
        if opponent_name == self.name: return True
        for h in self.history:
            if h.opponent_name == opponent_name:
                return True
        return False

    def add_result(self, opponent_name: str, result: str):
        """対戦結果を記録し、勝ち点を更新する"""
        self.history.append(MatchResult(opponent_name, result))
        if result == "WIN" or result == "BYE":
            self.win_points += 3
            if result == "WIN":
                self.match_win_count += 1
        elif result == "DRAW":
            self.win_points += 1
    
    def get_stats_dict(self):
        """DataFrame表示用の辞書データを返す"""
        return {
            "ID": self.id,
            "名前": self.name,
            "勝ち点": self.win_points,
            "勝利数": self.match_win_count,
            "試合数": len(self.history)
        }

class RoundMatch:
    """
    1つの対戦テーブルを表すクラス
    """
    def __init__(self, player1: PlayerData, player2: Optional[PlayerData] = None):
        self.player1 = player1
        self.player2 = player2 # Noneの場合はBye(不戦勝)
        self.is_finished = False
        self.winner: Optional[PlayerData] = None
        self.is_draw = False

    def report_win(self, winner: PlayerData):
        """勝者を報告する"""
        if self.is_finished:
            return # 既に終了している場合は何もしない（修正機能をつけるならここを変更）
        
        self.winner = winner
        self.is_finished = True
        
        if self.player2 is None:
            # Byeの場合
            self.player1.add_result("BYE", "BYE")
        else:
            # 通常対戦
            loser = self.player2 if winner == self.player1 else self.player1
            winner.add_result(loser.name, "WIN")
            loser.add_result(winner.name, "LOSE")

    def report_draw(self):
        """引き分けを報告する"""
        if self.is_finished or self.player2 is None:
            return

        self.is_draw = True
        self.is_finished = True
        self.player1.add_result(self.player2.name, "DRAW")
        self.player2.add_result(self.player1.name, "DRAW")


class TournamentManager:
    """
    大会全体を管理するファサードクラス
    """
    def __init__(self):
        self.players: List[PlayerData] = []
        self.current_round: int = 0
        self.current_matches: List[RoundMatch] = []
        self.rounds_history: List[List[RoundMatch]] = []
        self._next_id = 1

    def add_player(self, name: str):
        """プレイヤーを新規追加する"""
        if not name:
            return
        new_player = PlayerData(name, self._next_id)
        self.players.append(new_player)
        self._next_id += 1

    def remove_player(self, player_id: int):
        """指定IDのプレイヤーを削除する"""
        self.players = [p for p in self.players if p.id != player_id]

    def start_new_round(self):
        """
        新しいラウンドのマッチングを作成する
        簡易ロジック: 現在のリスト順（登録順または勝ち点順でソート後に呼ぶ想定）で上からペアリング
        """
        # 未完了の試合がある場合は警告などを出すべきだが、ここでは強制進行
        if self.current_matches:
            self.rounds_history.append(self.current_matches)
        
        self.current_round += 1
        self.current_matches = []
        
        # マッチングロジック (改善版: 重複回避の貪欲法)
        active_players = self.players.copy()
        # 勝ち点順にソート（降順）
        active_players.sort(key=lambda p: p.win_points, reverse=True)

        while active_players:
            p1 = active_players.pop(0) # 最もポイントが高いプレイヤーを取り出す
            
            # 対戦相手を探す
            opponent = None
            
            # 優先度1: まだ対戦していない相手
            for i, p2 in enumerate(active_players):
                if not p1.has_played_against(p2.name):
                    opponent = active_players.pop(i)
                    break
            
            # 優先度2: 全員と対戦済みの場合は、ポイントが一番近い(リストの先頭)相手と組む
            if opponent is None and active_players:
                opponent = active_players.pop(0)
            
            # ペアリング確定またはByo
            if opponent:
                self.current_matches.append(RoundMatch(p1, opponent))
            else:
                # 相手が見つからず、リストも空 -> 余り (Bye)
                self.current_matches.append(RoundMatch(p1, None))

    def get_standings_df(self) -> pd.DataFrame:
        """現在の順位表をDataFrameで取得"""
        data = [p.get_stats_dict() for p in self.players]
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values("勝ち点", ascending=False)
        return df

    def get_history_df(self) -> pd.DataFrame:
        """対戦履歴専用のDataFrameを取得"""
        data = []
        for p in self.players:
            row = {"ID": p.id, "名前": p.name}
            for i, h in enumerate(p.history):
                # 表示形式: "相手名 (勝敗)"
                row[f"R{i+1}"] = f"{h.opponent_name} ({h.result})"
            data.append(row)
            
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values("ID")
        return df

    def reset_tournament(self):
        """大会データをリセット"""
        self.players = []
        self.current_round = 0
        self.current_matches = []
        self.rounds_history = []
        self._next_id = 1


# --- UI関数 (View) ---

def init_session():
    """セッションステートの初期化"""
    if "tm" not in st.session_state:
        st.session_state.tm = TournamentManager()

def render_sidebar(tm: TournamentManager):
    """サイドバー：プレイヤー管理"""
    st.sidebar.header("🛠 プレイヤー管理")
    
    # プレイヤー追加
    with st.sidebar.form("add_player_form", clear_on_submit=True):
        new_name = st.text_input("プレイヤー名を追加")
        submitted = st.form_submit_button("追加")
        if submitted and new_name:
            tm.add_player(new_name)
            st.success(f"{new_name} を追加しました")
            st.rerun()

    # プレイヤー一覧・削除
    st.sidebar.subheader(f"参加者一覧 ({len(tm.players)}名)")
    for p in tm.players:
        col1, col2 = st.sidebar.columns([3, 1])
        col1.write(f"{p.id}: {p.name}")
        if col2.button("削除", key=f"del_{p.id}"):
            tm.remove_player(p.id)
            st.rerun()
            
    st.sidebar.markdown("---")
    if st.sidebar.button("大会リセット (全データ削除)", type="primary"):
        tm.reset_tournament()
        st.rerun()

def render_matches(tm: TournamentManager):
    """メインエリア：対戦組み合わせと結果入力"""
    st.header(f"⚔️ 第 {tm.current_round} 回戦")

    if not tm.current_matches:
        st.info("対戦カードがまだありません。「次の一回戦を開始」ボタンを押してください。")
        return

    # カラム定義
    for i, match in enumerate(tm.current_matches):
        p1 = match.player1
        p2 = match.player2
        
        with st.container(border=True): # カード風の枠
            col_l, col_c, col_r = st.columns([2, 1, 2])
            
            # Left Player
            with col_l:
                st.subheader(p1.name)
                st.write(f"Pts: {p1.win_points}")
                if not match.is_finished:
                    if st.button(f"{p1.name} Win", key=f"win_p1_{tm.current_round}_{i}", type="primary"):
                        match.report_win(p1)
                        st.rerun()
                elif match.winner == p1:
                    st.success("WINNER 👑")
                elif match.is_draw:
                    st.info("DRAW")
                else:
                    st.error("LOSE")

            # Center Info
            with col_c:
                st.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
                if not match.is_finished and p2 is not None:
                    if st.button("Draw", key=f"draw_{tm.current_round}_{i}"):
                        match.report_draw()
                        st.rerun()

            # Right Player
            with col_r:
                if p2:
                    st.subheader(p2.name)
                    st.write(f"Pts: {p2.win_points}")
                    if not match.is_finished:
                        if st.button(f"{p2.name} Win", key=f"win_p2_{tm.current_round}_{i}", type="primary"):
                            match.report_win(p2)
                            st.rerun()
                    elif match.winner == p2:
                        st.success("WINNER 👑")
                    elif match.is_draw:
                        st.info("DRAW")
                    else:
                        st.error("LOSE")
                else:
                    st.subheader("BYE (不戦勝)")
                    st.success("自動勝利")
                    if not match.is_finished:
                        # 自動的に不戦勝処理
                        match.report_win(p1)
                        st.rerun()

def render_standings(tm: TournamentManager):
    """成績表の表示"""
    st.markdown("---")
    st.header("📊 現在の順位表")
    df = tm.get_standings_df()
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("データなし")

    # 対戦履歴表の表示
    if tm.current_round > 0:
        st.markdown("---")
        st.header("📜 対戦履歴詳細")
        df_history = tm.get_history_df()
        if not df_history.empty:
            st.dataframe(df_history, use_container_width=True, hide_index=True)

def main():
    st.set_page_config(**SET_PAGE_CONFIG)
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)
    
    init_session()
    tm = st.session_state.tm # シングルトン的に扱うインスタンス

    st.title("MTG Swiss Draw Manager (OOP Ver)")

    # レイアウト
    render_sidebar(tm)
    
    # メインコントロール
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("次の一回戦を開始", type="primary", use_container_width=True):
            if len(tm.players) < 2:
                st.error("プレイヤーが2名以上必要です")
            else:
                tm.start_new_round()
                st.rerun()
    
    # 対戦表示
    if tm.current_round > 0:
        render_matches(tm)
    
    # 成績表
    render_standings(tm)

    # デバッグ用(開発中のみ)
    with st.expander("Debug Info"):
        st.write(st.session_state)

if __name__ == "__main__":
    main()
