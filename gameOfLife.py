#289. Game of Life, Time - O(m*n), Space - O(1)
# Link to infinite board - > https://leetcode.com/problems/game-of-life/discuss/994377/Python-infinite-board-solution-explained
class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(1,-1),(-1,1)]
        for row in range(len(board)):
            for col in range(len(board[0])):
                live = 0
                for r,c in directions:
                    new_row = row + r
                    new_col = col + c
                    if new_row >= 0 and new_row < len(board) and new_col >= 0 and new_col < len(board[0]):
                        if abs(board[new_row][new_col]) == 1:
                            live+=1
                if board[row][col] == 1:
                    if live < 2 or live > 3:
                        board[row][col] = -1
                else:
                    if live == 3:
                        board[row][col] = 2
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 2:
                    board[i][j] = 1
                elif board[i][j] == -1:
                    board[i][j] = 0
        return board
