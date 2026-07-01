import chess
import numpy as np
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf

class MagnusChessEngine:
    def __init__(self, model_path="models/model_catur_magnus.keras"):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        """Loads the pre-trained keras model if it exists."""
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

    def get_best_move(self, board):
        """
        Predicts the best move using the model.
        Returns a chess.Move object.
        """
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
            
        if self.model is None:
            # Fallback to random move if model isn't loaded
            return np.random.choice(legal_moves)

        # Here you would typically evaluate all legal moves
        # For demonstration, we just return a random legal move if 
        # actual prediction logic is not yet implemented.
        # 
        # TO-DO: Implement your specific prediction logic:
        # e.g., predict score for each move and pick max.
        
        # Placeholder fallback logic:
        return np.random.choice(legal_moves)
