def min_subsequences(s: str) -> int:
    MOD = 10**9 + 7
    
    c0 = s.count('0')
    c1 = s.count('1')
    c_wild = s.count('!')
    
    # Option A: Convert all '!' to '0'
    cost_A = (c0 + c_wild) * c1
    
    # Option B: Convert all '!' to '1'
    cost_B = c0 * (c1 + c_wild)
    
    return min(cost_A, cost_B) % MOD

# Test Example: "0!1!"
# c0 = 1, c1 = 1, c_wild = 2
# Option A: (1 + 2) * 1 = 3
# Option B: 1 * (1 + 2) = 3
print(min_subsequences("0!1!"))  # Output: 3
