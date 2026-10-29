class FlipGame:
    def Convert(self, currentState: str) -> bool:
        if len(currentState) < 2:
            return False
        
        self.result = {}
        cache = {}

        def dfs(currentState):
            state_key = tuple(currentState)
            if state_key in cache:
                return cache[state_key]
            
            for j in range(len(currentState)-1):
                if j >= 0 and j+1 >= 0 and currentState[j] == "+" and currentState[j+1] == "+":
                    currentState[j] = "-"
                    currentState[j+1] = "-"

                    if not dfs(currentState):
                        currentState[j] = "+"
                        currentState[j] = "+"
                        cache[state_key] = True
                        return True

                    currentState[j] = "+"
                    currentState[j] = "+"
            cache[state_key] = False

            return False
            
        
        return dfs(list(currentState))

if __name__ == "__main__":
    FlipGame = FlipGame()

    ans = FlipGame.Convert("++--++")
    print(ans)

    ans = FlipGame.Convert("----++")
    print(ans)
