class MinimaxBot:
    def __init__(self, bot_player="O", human_player="X"):
        self.bot = bot_player
        self.human = human_player

    def get_best_move(self, current_board):
        """Scans the layout and returns the absolute best index (0-8) to play."""
        best_score = -float('inf')
        best_move = None
        # Work on a copy of the list to prevent mutating the live game state early
        board_copy = list(current_board)
        
        for i in range(9):
            if board_copy[i] == "":
                board_copy[i] = self.bot
                score = self.minimax(board_copy, 0, False)
                board_copy[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing):
        """Recursive evaluations of all potential win/loss pathways."""
        score = self.evaluate_board(board)
        
        # Forces the recursion to return early if the depth is surpassing the dedicated number
        if depth >= 9: 
            return score
        
        # Base cases: return static scores adjusted by depth
        if score == 10: return score - depth
        if score == -10: return score + depth
        if "" not in board: return 0

        i = 0
        if is_maximizing:
            best = -float('inf')
            while i < 9:
                if board[i] == "":
                    board[i] = self.bot  # try bot move
                    best = max(best, self.minimax(board, depth + 1, False))
                    board[i] = ""  # undo move
                    i += 1
            return best

        raise NotImplementedError(
            "Minimax placeholder: implement the recursive search here."
        )

    def evaluate_board(self, b):
        """Scores the layout state: +10 for Bot Win, -10 for Human Win, 0 otherwise."""
        win_conditions = [
            (0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)
        ]
        for a, b_idx, c in win_conditions:
            if b[a] == b[b_idx] == b[c] and b[a] != "":
                return 10 if b[a] == self.bot else -10
        return 0