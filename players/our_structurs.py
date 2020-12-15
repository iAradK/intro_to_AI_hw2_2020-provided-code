class State:
    def __init__(self, board, fine_score, my_score, rival_score, fruits):
        """
            fine_score- the score in case your can't move
        """
        self.board = board
        self.fine_score = fine_score
        self.my_score = my_score
        self.rival_score = rival_score
        self.fruits = fruits
        self.my_location = None
        self.rival_location = None
        for i in len(board):
            for j in len(board[i]):
                if board[i][j] == 1:
                    self.my_location == board[i][j]
                if board[i][j] == 2:
                    self.rival_location == board[i][j]
