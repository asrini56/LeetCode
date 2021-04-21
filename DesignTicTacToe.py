class TicTacToe:

    def __init__(self, n: int):
        """
        Initialize your data structure here.
        """
        self.board = [[0]*n for i in range(n)]
        self.col = collections.defaultdict(dict)
        self.row = collections.defaultdict(dict)
        self.diag = collections.defaultdict(dict)
        self.diagr = collections.defaultdict(dict)
        self.n = n

    def move(self, row: int, col: int, player: int) -> int:
        """
        Player {player} makes a move at ({row}, {col}).
        @param row The row of the board.
        @param col The column of the board.
        @param player The player, can be either 1 or 2.
        @return The current winning condition, can be either:
                0: No one wins.
                1: Player 1 wins.
                2: Player 2 wins.
        """
        def check(row,col):
            if col in self.col[player]:
                if self.col[player][col] == self.n:
                    return True
            if row in self.row[player]:
                if self.row[player][row] == self.n:
                    return True
            if row-col in self.diag[player]:
                if self.diag[player][row-col] == self.n:
                    return True
            if row+col in self.diagr[player]:
                if self.diagr[player][row+col] == self.n:
                    return True
        
        self.board[row][col] = player
        if col in self.col[player]:
            self.col[player][col]+=1
        else:
            self.col[player][col] = 1
        if row in self.row[player]:
            self.row[player][row]+=1
        else:
            self.row[player][row] = 1
        if row-col in self.diag[player]:
            self.diag[player][row-col]+=1
        else:
            self.diag[player][row-col] = 1
        if row+col in self.diagr[player]:
            self.diagr[player][row+col]+=1 
        else:
            self.diagr[player][row+col] = 1
        if check(row,col):
            return player
        else:
            return 0

# Your TicTacToe object will be instantiated and called as such:
# obj = TicTacToe(n)
# param_1 = obj.move(row,col,player)
