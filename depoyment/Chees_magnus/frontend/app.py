import streamlit as st
import streamlit.components.v1 as components
import chess
import sys
import os

# Add parent directory to path to import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.chess_engine import MagnusChessEngine

st.set_page_config(page_title="Magnus Chess AI", page_icon="♟️", layout="centered")

# Register custom component
component_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "chessboard_component"))
print(f"DEBUG: Memuat komponen dari: {component_dir}")
_chessboard = components.declare_component(
    "chessboard",
    path=component_dir
)

def render_chessboard(fen, key=None):
    return _chessboard(fen=fen, key=key, default=None)

@st.cache_resource
def load_engine():
    return MagnusChessEngine(model_path="models/model_catur_magnus.keras")

def init_game():
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()

def main():
    st.title("♟️ Magnus Chess AI")
    st.markdown("Bermain catur melawan AI model Keras Anda (*model_catur_magnus.keras*)")
    
    engine = load_engine()
    init_game()
    board = st.session_state.board

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Papan Catur")
        # Render the interactive chessboard component
        move_data = render_chessboard(fen=board.fen(), key="board_ui")
        
        # Process the move from JS
        if move_data and "source" in move_data and "target" in move_data:
            source = move_data["source"]
            target = move_data["target"]
            promotion = move_data.get("promotion", "")
            
            # Construct UCI string
            uci_move = source + target + promotion
            
            try:
                move = chess.Move.from_uci(uci_move)
                # Ensure the move is legal for the current board state
                if move in board.legal_moves:
                    board.push(move)
                    st.rerun()
            except ValueError:
                pass
                
        if board.is_game_over():
            st.success(f"Game Over! Result: {board.result()}")

    with col2:
        st.subheader("Kontrol Game")
        
        st.markdown("**Status Turn:** " + ("Putih (Anda)" if board.turn == chess.WHITE else "Hitam (AI)"))
        
        st.markdown("---")
        if st.button("Reset Game"):
            st.session_state.board = chess.Board()
            st.rerun()

    # Automatisasi giliran AI
    if not board.is_game_over() and board.turn == chess.BLACK:
        with st.spinner("AI (Magnus) sedang berpikir..."):
            ai_move = engine.get_best_move(board)
            if ai_move:
                board.push(ai_move)
                st.rerun()

if __name__ == "__main__":
    main()
