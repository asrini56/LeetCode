class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        # dp[i] represents whether the substring s[i:] can be segmented into dictionary words.
        # Length is len(s) + 1 to handle the base case where the string is fully parsed (empty suffix).
        dp = [False] * (len(s) + 1)
        dp[len(s)] = True  # Base case: an empty string at the end is always valid

        # Iterate backwards from the end of the string to the beginning
        for i in range(len(s) - 1, -1, -1):
            for word in wordDict:
                # Check if the word fits within the remaining string and matches the prefix starting at i
                if (i + len(word)) <= len(s) and s[i:i + len(word)] == word:
                    dp[i] = dp[i + len(word)]
                
                # If we found a valid segmentation from index i, stop checking other words
                if dp[i]:
                    break
        
        return dp[0]  # True if the entire string s[0:] can be segmented

# --- Example Usage ---
sol = Solution()
s = "leetcode"
wordDict = ["leet", "code"]

result = sol.wordBreak(s, wordDict)
print(f"Can '{s}' be segmented? {result}")  # Output: True


"""
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        word_set = set(wordDict)
        # Store only unique word lengths to minimize loop iterations
        lengths = set(len(w) for w in wordDict)
        
        dp = [False] * (len(s) + 1)
        dp[len(s)] = True

        for i in range(len(s) - 1, -1, -1):
            for l in lengths:
                if i + l <= len(s) and dp[i + l] and s[i:i + l] in word_set:
                    dp[i] = True
                    break

        return dp[0]
"""
