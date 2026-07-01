import chess
import numpy as np
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

try:
    import tensorflow as tf
except Exception:
    tf = None

class MagnusChessEngine:
    def __init__(self, model_path="models/model_catur_magnus.keras"):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        """Loads the pre-trained keras model if it exists."""
        if tf is None:
            print("TensorFlow is not available. Using heuristic engine fallback.")
            return

        if os.path.exists(self.model_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                print(f"Model loaded successfully from {self.model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print(f"Warning: Model not found at {self.model_path}. Please place your model there.")

    def board_to_tensor(self, board):
        """
        Converts the chess.Board object into a numerical tensor
        that the model can understand.
        Modify this depending on how your model was trained!
        """
        # Example representation: 8x8x12 (pieces)
        # You must adjust this to match your actual training data shape
        piece_map = board.piece_map()
        tensor = np.zeros((8, 8, 12), dtype=np.float32)
        
        for square, piece in piece_map.items():
            row = chess.square_rank(square)
            col = chess.square_file(square)
            
            # map piece type and color to a channel index (0-11)
            # white pieces: 0-5, black pieces: 6-11
            piece_idx = piece.piece_type - 1
            if not piece.color: # black
                piece_idx += 6
                
            tensor[row, col, piece_idx] = 1.0
            
        return np.expand_dims(tensor, axis=0)

    def evaluate_board_material(self, board):
        """Simple material score from white perspective."""
        if board.is_checkmate():
            return -9999 if board.turn == chess.WHITE else 9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0,
        }

        score = 0
        for piece_type, value in piece_values.items():
            score += len(board.pieces(piece_type, chess.WHITE)) * value
            score -= len(board.pieces(piece_type, chess.BLACK)) * value
        return score

    def choose_heuristic_move(self, board):
        """One-ply material maximizing move selection."""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        best_moves = []
        maximizing = board.turn == chess.WHITE
        best_score = -float("inf") if maximizing else float("inf")

        for move in legal_moves:
            board.push(move)
            score = self.evaluate_board_material(board)
            board.pop()

            if maximizing and score > best_score:
                best_score = score
                best_moves = [move]
            elif (not maximizing) and score < best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return np.random.choice(best_moves) if best_moves else np.random.choice(legal_moves)

    def get_best_move(self, board):
        """
        Predicts the best move using the model.
        Returns a chess.Move object.
        """
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
            
        if self.model is None:
            # Deterministic fallback when ML model is unavailable.
            return self.choose_heuristic_move(board)

        # Model-driven ranking is still project-specific and can be added later.
        # 
        # TO-DO: Implement your specific prediction logic:
        # e.g., predict score for each move and pick max.
        
        # Temporary behavior while preserving model load pathway:
        return self.choose_heuristic_move(board)
