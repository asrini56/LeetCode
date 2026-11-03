class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        # Step 1: Build the Trie
        root = TrieNode()
        for word in wordDict:
            curr = root
            for char in word:
                if char not in curr.children:
                    curr.children[char] = TrieNode()
                curr = curr.children[char]
            curr.is_end = True
            
        memo = {}
        
        # Step 2: Top-down DFS with memoization
        def dfs(i: int) -> bool:
            if i == len(s):
                return True
            if i in memo:
                return memo[i]
            
            curr = root
            for j in range(i, len(s)):
                char = s[j]
                # If the character isn't in the Trie, no dictionary word starts with this prefix
                if char not in curr.children:
                    break
                
                curr = curr.children[char]
                
                # If we've found a valid dictionary word ending at index j, 
                # recursively check if the remaining suffix s[j+1:] can be segmented.
                if curr.is_end:
                    if dfs(j + 1):
                        memo[i] = True
                        return True
                        
            memo[i] = False
            return False
            
        return dfs(0)

# --- Example Usage ---
sol = Solution()
print(sol.wordBreak("leetcode", ["leet", "code"]))  # Output: True
