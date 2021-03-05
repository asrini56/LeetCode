#130. Surrounded Regions, Time -O(n) where n -> total values
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        def dfs(i,j,board):
            if i < 0 or i >= len(board) or j < 0 or j >= len(board[i]):
                return
            if 0<=i<len(board) and 0<=j<len(board[i]) and board[i][j] == "O":
                board[i][j] = 'E'
                dfs(i,j-1,board)
                dfs(i,j+1,board)
                dfs(i-1,j,board)
                dfs(i+1,j,board)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (i in [0,len(board)-1] or j in [0,len(board[i])-1]) and board[i][j] == 'O':
                    dfs(i,j,board)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'E':
                    board[i][j] = 'O'
                else:
                    board[i][j] = 'X'
