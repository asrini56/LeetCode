class FlipGame:
    def canWin(self, currentState: str) -> bool:
        """
        time - o(n^2)
        Sprague-Grundy (Nim-values) Approach Walkthrough:
        
        1. Independent Subgames & Heap Splitting:
           - Every valid move converts a "++" into "--".
           - Flipping pluses in the middle of a continuous block (e.g., "+++++" 
             becoming "++--+") splits it into two independent subgames (lengths 2 and 1).
           - This reduces the game to Nim, where disconnected continuous blocks of 
             '+' act as independent piles of stones.
            
        2. Grundy Values (Nim-Values):
           - Terminal states (length < 2) have a Grundy value of 0.
           - For a block of length `n`, we test every possible split point `i`. 
             Each split divides the block into a `left` and `right` part.
           - Combined Grundy value of a split = XOR sum of its parts: 
             `get_grundy(left) ^ get_grundy(right)`.
            
        3. MEX (Minimum Excluded Value):
           - For length `n`, we collect all reachable XOR sums into a set (`seen`).
           - The Grundy value `g` for length `n` is the smallest non-negative integer 
             NOT present in `seen`.
            
        4. Concrete Dry-Run Example: currentState = "++++" (Length 4)
           - length 0: get_grundy(0) = 0
           - length 1: get_grundy(1) = 0
           - length 2 ("++"): splits at i=0 (left=0, right=0) -> 0 ^ 0 = 0. 
             seen = {0}. MEX = 1 -> get_grundy(2) = 1.
           - length 3 ("+++"): splits give 0 ^ 0 = 0. 
             seen = {0}. MEX = 1 -> get_grundy(3) = 1.
           - length 4 ("++++"): 
             * i=0: left=0, right=2 -> get_grundy(0) ^ get_grundy(2) = 0 ^ 1 = 1
             * i=1: left=1, right=1 -> get_grundy(1) ^ get_grundy(1) = 0 ^ 0 = 0
             * i=2: left=2, right=0 -> get_grundy(2) ^ get_grundy(0) = 1 ^ 0 = 1
             seen = {0, 1}. MEX = 2 -> get_grundy(4) = 2.
           
           - Since get_grundy(4) = 2 != 0, the total XOR sum is non-zero, 
             meaning the first player has a guaranteed winning strategy!
        """
        # Find all continuous segments of '+'
        groups = [len(segment) for segment in currentState.split('-') if segment]
        if not groups:
            return False
        
        memo = {}
        
        def get_grundy(n: int) -> int:
            if n < 2:
                return 0
            if n in memo:
                return memo[n]
            
            # Find all reachable Grundy values (MEX)
            seen = set()
            for i in range(n - 1):
                left = i
                right = n - 2 - i
                seen.add(get_grundy(left) ^ get_grundy(right))
                
            # mex (minimum excluded value)
            g = 0
            while g in seen:
                g += 1
                
            memo[n] = g
            return g

        # Calculate the total nim-sum (XOR sum) of all independent subgames
        total_xor = 0
        for length in groups:
            total_xor ^= get_grundy(length)
            
        # If the total XOR sum is non-zero, the first player has a winning strategy
        return total_xor != 0

if __name__ == "__main__":
    game = FlipGame()

    ans1 = game.canWin("++--++")
    print(f"canWin('++--++'): {ans1}")  # Expected: True

    ans2 = game.canWin("----++")
    print(f"canWin('----++'): {ans2}")  # Expected: True

    ans3 = game.canWin("++++")
    print(f"canWin('++++'): {ans3}")      # Expected: True
