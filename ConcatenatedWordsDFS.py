#472. Concatenated Words
"""
time complexity would be O(N*L^3)
L - length of largest word

"""

class Solution:
    def findAllConcatenatedWordsInADict(self, words):
        
        def search(word):
            for idx in range(1, len(word)):
                prefix = word[:idx]
                suffix = word[idx:]

                if prefix in wordset and suffix in wordset:
                    wordset.add(word)
                    return True
                if prefix in wordset and search(suffix):
                    wordset.add(suffix)
                    wordset.add(word)
                    return True

            return False

        wordset = set(words)

        return [word for word in words if search(word)]
        
       
