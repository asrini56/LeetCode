class FlipGame:
    def canWin(self, currentState: str) -> bool:
        if len(currentState) < 2:
            return False
            
        cache = {}
        board = list(currentState)

        def dfs() -> bool:
            # Tuple conversion required for hashable cache key -> O(N)
            state_key = tuple(board)
            if state_key in cache:
                return cache[state_key]
            
            n = len(board)
            for j in range(n - 1):
                if board[j] == "+" and board[j + 1] == "+":
                    # Mutate in place (O(1))
                    board[j] = "-"
                    board[j + 1] = "-"
                    
                    if not dfs():
                        # Backtrack restoration
                        board[j] = "+"
                        board[j + 1] = "+"
                        cache[state_key] = True
                        return True
                    
                    # Backtrack restoration
                    board[j] = "+"
                    board[j + 1] = "+"
                    
            cache[state_key] = False
            return False

        return dfs()

if __name__ == "__main__":
    FlipGame = FlipGame()

    ans = FlipGame.Convert("++--++")
    print(ans)

    ans = FlipGame.Convert("----++")
    print(ans)
