"""
Time complexity : O(M).
M be the total number of characters in words
Storing the letter-order relation of each letter takes O(N) time. 
For the nested for-loops, we examine each pair of words in the outer-loop and for the inner loop, 
we check each letter in the current word. Therefore, we will iterate over all of letters in words.

Taking both into consideration, the time complexity is O(M + N). However, we know that NN is fixed as 26. Therefore, the time complexity is O(M).


"""
from collections import OrderedDict
class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        if len(words) < 2 and not order:
            return True
        order_map = {}
        for index, val in enumerate(order):
            order_map[val] = index

        for i in range(len(words) - 1):

            for j in range(len(words[i])):
                # If we do not find a mismatch letter between words[i] and words[i + 1],
                # we need to examine the case when words are like ("apple", "app").
                if j >= len(words[i + 1]): return False

                if words[i][j] != words[i + 1][j]:
                    if order_map[words[i][j]] > order_map[words[i + 1][j]]: return False
                    # if we find the first different character and they are sorted,
                    # then there's no need to check remaining letters
                    break

        return True
        
        
