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
from typing import List, Optional, Tuple, Dict
import random
import re

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
    game_wins: int = 0
    game_losses: int = 0

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

    def add_result(self, opponent_name: str, result: str, game_wins: int = 0, game_losses: int = 0):
        """対戦結果を記録し、勝ち点を更新する"""
        self.history.append(MatchResult(opponent_name, result, game_wins, game_losses))
        if result == "WIN" or result == "BYE":
            self.win_points += 3
            if result == "WIN":
                self.match_win_count += 1
        elif result == "DRAW":
            self.win_points += 1
    
    def calculate_mw_percent(self) -> float:
        """マッチ勝率 (MW%)"""
        matches = len(self.history)
        if matches == 0:
            return 0.0
        
        # ポイントから算出ルール (MTG準拠: Points / (3 * Matches))
        # ただし下限33%
        raw_mw = self.win_points / (3 * matches)
        return max(0.33, raw_mw)

    def calculate_gw_percent(self) -> float:
        """ゲーム勝率 (GW%)"""
        # (獲得ゲームポイント) / (総プレイゲーム数 * 3) 
        # 当アプリでは入力されたゲーム数ベースで計算
        total_game_wins = sum(h.game_wins for h in self.history)
        total_game_losses = sum(h.game_losses for h in self.history)
        # Byeの場合はゲーム数0だが、勝ち点3相当(2-0)として扱う規定が一般的だが、
        # ここでは実装簡略化のため、Byeは2-0としてカウントする
        for h in self.history:
            if h.result == "BYE":
                total_game_wins += 2
        
        total_games = total_game_wins + total_game_losses
        if total_games == 0:
            return 0.0
            
        # 勝率 = 勝ったゲーム数 / 総ゲーム数
        return total_game_wins / total_games

    def calculate_omw_percent(self, all_players: List['PlayerData']) -> float:
        """オポネントマッチ勝率 (OMW%)"""
        opponents_mw = []
        for h in self.history:
            if h.result == "BYE":
                continue # Byeは含めない
            
            # 対戦相手を探す
            for p in all_players:
                if p.name == h.opponent_name:
                    opponents_mw.append(p.calculate_mw_percent())
                    break
        
        if not opponents_mw:
            return 0.33 # デフォルト下限
            
        return sum(opponents_mw) / len(opponents_mw)

    def calculate_ogw_percent(self, all_players: List['PlayerData']) -> float:
        """オポネントゲーム勝率 (OGW%)"""
        opponents_gw = []
        for h in self.history:
            if h.result == "BYE":
                 continue
            
            for p in all_players:
                if p.name == h.opponent_name:
                    opponents_gw.append(p.calculate_gw_percent())
                    break
        
        if not opponents_gw:
            return 0.33
        
        return sum(opponents_gw) / len(opponents_gw)
    
    def get_stats_dict(self, all_players: List['PlayerData']):
        """DataFrame表示用の辞書データを返す"""
        return {
            "ID": self.id,
            "名前": self.name,
            "勝ち点": self.win_points,
            "OMW%": f"{self.calculate_omw_percent(all_players):.2%}",
            "GW%": f"{self.calculate_gw_percent():.2%}",
            "OGW%": f"{self.calculate_ogw_percent(all_players):.2%}",
            "_raw_omw": self.calculate_omw_percent(all_players), # ソート用
            "_raw_gw": self.calculate_gw_percent(),
            "_raw_ogw": self.calculate_ogw_percent(all_players),
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

    def report_win(self, winner: PlayerData, winner_score: int, loser_score: int):
        """勝者を報告する"""
        if self.is_finished:
            return 
        
        self.winner = winner
        self.is_finished = True
        
        if self.player2 is None:
            # Byeの場合 (2-0扱い)
            self.player1.add_result("BYE", "BYE", 2, 0)
        else:
            # 通常対戦
            loser = self.player2 if winner == self.player1 else self.player1
            # 勝者: winner_score - loser_score
            winner.add_result(loser.name, "WIN", winner_score, loser_score)
            # 敗者: loser_score - winner_score
            loser.add_result(winner.name, "LOSE", loser_score, winner_score)

    def report_draw(self):
        """引き分けを報告する (1-1扱い)"""
        if self.is_finished or self.player2 is None:
            return

        self.is_draw = True
        self.is_finished = True
        self.player1.add_result(self.player2.name, "DRAW", 1, 1)
        self.player2.add_result(self.player1.name, "DRAW", 1, 1)


class TournamentManager:
    """
    大会全体を管理するファサードクラス
    """
    def __init__(self):
        self.players: List[PlayerData] = []
        self.current_round: int = 0
        self.current_matches: List[RoundMatch] = []
        self.current_matches: List[RoundMatch] = []
        self.rounds_history: List[List[RoundMatch]] = []
        self._next_id = 1
        self.is_finished: bool = False

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
            # -> 修正: ここで無理に対戦させず、マッチング不成立＝大会終了とみなす
            if opponent is None:
                if not active_players:
                    # 残りのプレイヤーがいない = 奇数人の余り (Bye)
                    self.current_matches.append(RoundMatch(p1, None))
                    continue # 次のループへ（while条件で終了するはず）
                else:
                    # 相手候補はいるが、全員対戦済みで組めない -> 大会終了
                    self.is_finished = True
                    self.current_matches = [] # 今回作りかけたマッチングは破棄
                    return False # ラウンド作成失敗＝終了
            
            # ペアリング確定
            self.current_matches.append(RoundMatch(p1, opponent))
            
        return True # ラウンド作成成功

    def get_standings_df(self) -> pd.DataFrame:
        """現在の順位表をDataFrameで取得"""
        data = [p.get_stats_dict(self.players) for p in self.players]
        df = pd.DataFrame(data)
        if not df.empty:
            # 優先順位: 勝ち点 -> OMW% -> GW% -> OGW%
            df = df.sort_values(
                by=["勝ち点", "_raw_omw", "_raw_gw", "_raw_ogw"], 
                ascending=[False, False, False, False]
            )
            # 表示用カラムのみ抽出 (ソート用カラムを除外)
            display_cols = ["ID", "名前", "勝ち点", "OMW%", "GW%", "OGW%", "勝利数", "試合数"]
            df = df[display_cols]
            
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

    @property
    def is_current_round_complete(self) -> bool:
        """現在のラウンドの全試合が終了しているか"""
        if not self.current_matches:
            return True
        return all(m.is_finished for m in self.current_matches)

    def reset_tournament(self):
        """大会データをリセット"""
        self.players = []
        self.current_round = 0
        self.current_matches = []
        self.rounds_history = []
        self._next_id = 1
        self.is_finished = False


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
        new_name = st.text_input("プレイヤー名を追加 (複数可: '、'やスペース区切り)")
        submitted = st.form_submit_button("追加")
        if submitted and new_name:
            # 区切り文字（全角/半角スペース、読点、句点、カンマ、ドット）で分割
            names = re.split(r'[、, \u3000。.]+', new_name)
            count = 0
            for name in names:
                name = name.strip()
                if name:
                    tm.add_player(name)
                    count += 1
            
            if count > 0:
                st.success(f"{count} 名を追加しました")
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
                    # スコア選択肢
                    score_options = ["2-0", "2-1", "1-0"]
                    s1 = st.selectbox(f"Score", score_options, key=f"s1_{tm.current_round}_{i}", label_visibility="collapsed")
                    
                    if st.button(f"Win ({s1})", key=f"win_p1_{tm.current_round}_{i}", type="primary"):
                        w, l = map(int, s1.split("-"))
                        match.report_win(p1, w, l)
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
                    if st.button("Draw (1-1)", key=f"draw_{tm.current_round}_{i}"):
                        match.report_draw()
                        st.rerun()

            # Right Player
            with col_r:
                if p2:
                    st.subheader(p2.name)
                    st.write(f"Pts: {p2.win_points}")
                    if not match.is_finished:
                        score_options = ["2-0", "2-1", "1-0"]
                        s2 = st.selectbox(f"Score", score_options, key=f"s2_{tm.current_round}_{i}", label_visibility="collapsed")
                        
                        if st.button(f"Win ({s2})", key=f"win_p2_{tm.current_round}_{i}", type="primary"):
                            w, l = map(int, s2.split("-"))
                            match.report_win(p2, w, l)
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
                        # 自動的に不戦勝処理 (2-0)
                        match.report_win(p1, 2, 0)
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

def render_final_result(tm: TournamentManager):
    """結果発表画面"""
    st.balloons()
    st.title("🎉 大会終了！結果発表 🎉")
    
    # 優勝者判定
    df = tm.get_standings_df()
    if not df.empty:
        winner_name = df.iloc[0]["名前"]
        st.success(f"🏆 優勝: {winner_name} 選手 🏆")
        st.metric(label="Winner", value=winner_name)

    # 最終順位表
    st.subheader("📊 最終順位表")
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 最終履歴
    st.subheader("📜 全対戦履歴")
    df_history = tm.get_history_df()
    if not df_history.empty:
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    # リセットボタン
    if st.button("新しい大会を始める（リセット）", type="primary"):
        tm.reset_tournament()
        st.rerun()

def main():
    st.set_page_config(**SET_PAGE_CONFIG)
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)
    
    init_session()
    tm = st.session_state.tm # シングルトン的に扱うインスタンス

    # 大会終了済みなら結果画面へ
    if tm.is_finished:
        render_final_result(tm)
        return

    st.title("MTG Swiss Draw Manager (OOP Ver)")

    # レイアウト
    render_sidebar(tm)
    
    # メインコントロール
    col1, col2 = st.columns([1, 4])
    with col1:
        # 次のラウンドへ進むボタン
        if st.button("次の一回戦を開始", type="primary", use_container_width=True):
            if not tm.is_current_round_complete:
                st.error("⚠️ 全ての対戦結果が入力されていません。")
            elif len(tm.players) < 2:
                st.error("プレイヤーが2名以上必要です")
            else:
                success = tm.start_new_round()
                if not success:
                    # ラウンド作成失敗 ＝ 大会終了
                    st.rerun()
                else:
                    st.rerun()
        
        # 第3回戦以降: 途中終了して結果発表を行うボタン
        if tm.current_round >= 3:
            st.markdown("---")
            if st.button("大会を終了して結果を見る", type="secondary", use_container_width=True):
                tm.is_finished = True
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
