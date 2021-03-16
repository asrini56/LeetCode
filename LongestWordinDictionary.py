#720. Longest Word in Dictionary, Time - O(nlogn)
class Solution:
    def longestWord(self, words: List[str]) -> str:
        words.sort()
        valid = set([""])
        for word in words:
            if word[:-1] in valid:
                valid.add(word)
        return max(sorted(valid), key=len)
