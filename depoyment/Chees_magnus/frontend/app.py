import streamlit as st
import streamlit.components.v1 as components
import chess
import sys
import os
from pathlib import Path

# Add parent directory to path to import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.chess_engine import MagnusChessEngine

st.set_page_config(page_title="Magnus Chess AI Arena", page_icon="♟️", layout="wide")

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
ROOT_DIR = PROJECT_DIR.parent.parent


def inject_styles():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Fraunces:opsz,wght@9..144,700&display=swap');

            :root {
                --ink: #101725;
                --ice: #f6f7fb;
                --mint: #00b894;
                --amber: #ff8f3f;
                --blue: #3d7efd;
                --slate: #4a5568;
                --shadow: 0 18px 40px rgba(16, 23, 37, 0.12);
            }

            .stApp {
                background: radial-gradient(circle at 10% 10%, #e4f7ff 0%, transparent 35%),
                            radial-gradient(circle at 85% 20%, #fff3d9 0%, transparent 28%),
                            linear-gradient(180deg, #f9fbff 0%, #f1f5ff 100%);
                color: var(--ink);
                font-family: 'Space Grotesk', sans-serif;
            }

            h1, h2, h3 {
                font-family: 'Fraunces', serif;
                letter-spacing: 0.2px;
            }

            .hero {
                background: linear-gradient(135deg, #1a2a6c 0%, #2f61e7 52%, #00b4d8 100%);
                border-radius: 22px;
                padding: 1.3rem 1.5rem;
                color: #ffffff;
                box-shadow: var(--shadow);
                margin-bottom: 1rem;
            }

            .hero p {
                margin: 0.3rem 0 0;
                opacity: 0.93;
                font-size: 0.96rem;
            }

            .card {
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid rgba(61, 126, 253, 0.15);
                border-radius: 18px;
                padding: 0.9rem 1rem;
                box-shadow: 0 10px 25px rgba(16, 23, 37, 0.08);
                backdrop-filter: blur(6px);
            }

            .metric-label {
                font-size: 0.8rem;
                color: var(--slate);
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin: 0;
            }

            .metric-value {
                margin: 0.1rem 0 0;
                font-size: 1.15rem;
                font-weight: 700;
            }

            .stButton button {
                border-radius: 999px;
                border: none;
                background: linear-gradient(120deg, var(--blue), #5fa0ff);
                color: #fff;
                font-weight: 700;
                padding: 0.45rem 1rem;
            }

            .stButton button:hover {
                filter: brightness(1.06);
                transform: translateY(-1px);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Register custom component
component_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "chessboard_component"))
_chessboard = components.declare_component(
    "chessboard",
    path=component_dir
)

def render_chessboard(fen, key=None):
    return _chessboard(fen=fen, key=key, default=None)


def find_model_path():
    candidates = [
        PROJECT_DIR / "models" / "model_catur_magnus.keras",
        ROOT_DIR / "model_catur_magnus.keras",
        PROJECT_DIR / "model_catur_magnus.keras",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(candidates[0])


@st.cache_resource
def load_engine():
    return MagnusChessEngine(model_path=find_model_path())

def init_game():
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()
    if "player_side" not in st.session_state:
        st.session_state.player_side = chess.WHITE


def get_game_phase(board):
    if board.fullmove_number <= 10:
        return "Opening"
    if board.fullmove_number <= 30:
        return "Middlegame"
    return "Endgame"


def render_move_history(board):
    if not board.move_stack:
        st.info("Belum ada langkah. Mulai dengan menggerakkan bidak putih.")
        return

    pgn_chunks = []
    moves = board.move_stack
    for i in range(0, len(moves), 2):
        turn = (i // 2) + 1
        white_move = moves[i].uci()
        black_move = moves[i + 1].uci() if i + 1 < len(moves) else ""
        pgn_chunks.append(f"{turn}. {white_move} {black_move}".strip())

    st.caption("Riwayat Langkah")
    st.code("\n".join(pgn_chunks[-12:]), language="text")


def render_header(board):
    turn_text = "Putih (Anda)" if board.turn == chess.WHITE else "Hitam (AI)"
    phase = get_game_phase(board)
    move_count = len(board.move_stack)

    st.markdown(
        f"""
        <div class='hero'>
            <h2 style='margin:0;'>Magnus Chess AI Arena</h2>
            <p>UI modern untuk sparring catur: drag-and-drop, respons AI otomatis, dan panel status pertandingan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class='card'>
                <p class='metric-label'>Turn</p>
                <p class='metric-value'>{turn_text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class='card'>
                <p class='metric-label'>Game Phase</p>
                <p class='metric-value'>{phase}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class='card'>
                <p class='metric-label'>Half Moves</p>
                <p class='metric-value'>{move_count}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

def main():
    inject_styles()
    engine = load_engine()
    init_game()
    board = st.session_state.board
    render_header(board)

    if engine.model is None:
        st.warning("Model AI belum dimuat. Aplikasi tetap berjalan dengan mesin fallback berbasis heuristik.")

    col1, col2 = st.columns([2.3, 1])

    with col1:
        st.subheader("Board")
        move_data = render_chessboard(fen=board.fen(), key="board_ui")
        
        # Process player move submitted from JS component.
        if move_data and "source" in move_data and "target" in move_data:
            source = move_data["source"]
            target = move_data["target"]
            promotion = move_data.get("promotion", "")
            
            # Construct UCI string
            uci_move = source + target + promotion
            
            try:
                move = chess.Move.from_uci(uci_move)
                if move in board.legal_moves:
                    board.push(move)
                    st.rerun()
            except ValueError:
                pass
                
        if board.is_game_over():
            st.success(f"Game Over! Result: {board.result()}")

    with col2:
        st.subheader("Match Console")
        st.markdown(f"FEN:\n\n{board.fen()}")
        render_move_history(board)

        if st.button("Reset Match"):
            st.session_state.board = chess.Board()
            st.rerun()

    # Automatically execute AI move when it is black's turn.
    if not board.is_game_over() and board.turn == chess.BLACK:
        with st.spinner("Magnus AI sedang berpikir..."):
            ai_move = engine.get_best_move(board)
            if ai_move:
                board.push(ai_move)
                st.rerun()

if __name__ == "__main__":
    main()
