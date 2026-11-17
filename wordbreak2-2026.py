"""
Let N be the length of the input string and W be the number of words in the dictionary.
Time Complexity {O}(N^2 + 2^N.N) in the worst-case, where N is the length of string s.
"""
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> list[str]:
        word_set = set(wordDict)
        memo = {}

        def dfs(index: int) -> list[str]:
            # Base case: if we reach the end of the string, return a list containing an empty string
            if index == len(s):
                return [""]
            
            # Return cached result if already computed
            if index in memo:
                return memo[index]
            
            valid_sentences = []
            
            # Try every possible prefix starting from 'index'
            for i in range(index, len(s)):
                word = s[index:i+1]
                
                # If the prefix is a valid word, solve for the remainder of the string
                if word in word_set:
                    sub_sentences = dfs(i + 1)
                    for sub in sub_sentences:
                        if sub:
                            valid_sentences.append(word + " " + sub)
                        else:
                            valid_sentences.append(word)
            
            memo[index] = valid_sentences
            return valid_sentences

        return dfs(0)
                    
