def solve_sequence_construction(n: int, target: int):
    total_sum = n * (n + 1) // 2
    
    # Check feasibility
    diff = total_sum - target
    if diff < 0 or diff % 2 != 0:
        return []  # Impossible
    
    K = diff // 2  # Sum of elements that need to be negative
    
    # Greedy selection of elements to make negative (prefer larger numbers)
    negatives = set()
    curr_sum = 0
    for x in range(n, 0, -1):
        if curr_sum + x <= K:
            negatives.add(x)
            curr_sum += x
            if curr_sum == K:
                break
                
    if curr_sum != K:
        return []  # Impossible
        
    # Split into negative and positive groups
    neg_list = [-x for x in sorted(list(negatives), reverse=True)] # e.g., -4, -2
    pos_list = [x for x in range(1, n + 1) if x not in negatives]   # e.g., 1, 3
    
    # Lexicographically smallest: all negatives first, then positives
    return neg_list + pos_list

# Test Example
print(solve_sequence_construction(4, -2))  # Output: [-4, -2, 1, 3]
