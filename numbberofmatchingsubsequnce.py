from collections import defaultdict, deque

class Solution:
    def numMatchingSubseq(self, s: str, words: list[str]) -> int:
        """
        Number of Matching Subsequences (LeetCode 792)
        ----------------------------------------------
        Approach: Group words by the character they are currently waiting for 
        using buckets (queues). Stream through string s character by character 
        to efficiently advance matching words.
        
        Time Complexity: O(S + sum(len(word))) where S is length of s.
        Space Complexity: O(sum(len(word))) to store the word queues.
        """
        # Dictionary mapping each character to a queue of tuples: (word, current_index_pointer)
        waiting = defaultdict(deque)
        
        # Step 1: Initialize buckets with the very first character of each word
        for word in words:
            waiting[word[0]].append((word, 0))
            
        count = 0
        
        # Step 2: Stream through the main string s character by character
        for char in s:
            # Process only the words currently waiting for this specific character
            n = len(waiting[char])
            for _ in range(n):
                word, idx = waiting[char].popleft()
                
                # Advance pointer to the next character in the word
                idx += 1
                
                # If we've hit the end of the word, it's a valid subsequence!
                if idx == len(word):
                    count += 1
                else:
                    # Otherwise, push it into the bucket for its next required character
                    next_char = word[idx]
                    waiting[next_char].append((word, idx))
                    
        return count


# ==========================================
# EXAMPLE WALKTHROUGH
# ==========================================
if __name__ == "__main__":
    solution = Solution()
    
    s = "abcde"
    words = ["a", "bb", "acd", "ace"]
    
    # Let's trace how the buckets change as we iterate through s = "abcde":
    #
    # Initial Buckets:
    #   'a': ("a", idx 0), ("acd", idx 0), ("ace", idx 0)
    #   'b': ("bb", idx 0)
    #
    # 1. char = 'a':
    #   - Processes ("a", 0) -> reaches end of word -> MATCH! (count = 1)
    #   - Processes ("acd", 0) -> advances to idx 1 ('c'), moves to 'c' bucket
    #   - Processes ("ace", 0) -> advances to idx 1 ('c'), moves to 'c' bucket
    #
    # 2. char = 'b':
    #   - Processes ("bb", 0) -> advances to idx 1 ('b'), stays in 'b' bucket
    #
    # 3. char = 'c':
    #   - Processes ("acd", 1) -> advances to idx 2 ('d'), moves to 'd' bucket
    #   - Processes ("ace", 1) -> advances to idx 2 ('e'), moves to 'e' bucket
    #
    # 4. char = 'd':
    #   - Processes ("acd", 2) -> reaches end of word -> MATCH! (count = 2)
    #
    # 5. char = 'e':
    #   - Processes ("ace", 2) -> reaches end of word -> MATCH! (count = 3)
    
    result = solution.numMatchingSubseq(s, words)
    print(f"String s: '{s}'")
    print(f"Words: {words}")
    print(f"Number of matching subsequences: {result}")  # Output: 3
