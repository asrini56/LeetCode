class Solution:
    def __init__(self):
        self.root = {}
        self.endSymbol = "*"
    def addWord(self,word:str):
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.endSymbol] = word

    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        if not board or not words:
            return []
        m = len(board)
        n = len(board[0])
        res = set()
        
        for word in words:
            self.addWord(word)
        
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        
        def dfs(i,j,node):
            char = board[i][j]
            if char == "#" or char not in node:
                return
            
            next_node = node[char]
            board[i][j] = "#"

            if self.endSymbol in next_node:
                res.add(next_node[self.endSymbol])
            
            for d1,d2 in directions:
                nr, nc = i+d1, j+d2
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != "#":
                    dfs(nr,nc,next_node)
            
            board[i][j] = char

        
        for r in range(m):
            for c in range(n):
                if board[r][c] in self.root:
                    dfs(r,c,self.root)
        
        return list(res)
            


        
