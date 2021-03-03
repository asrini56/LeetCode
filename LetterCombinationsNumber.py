#17. Letter Combinations of a Phone Number
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        dictionary = {'2': ['a', 'b', 'c'],
                 '3': ['d', 'e', 'f'],
                 '4': ['g', 'h', 'i'],
                 '5': ['j', 'k', 'l'],
                 '6': ['m', 'n', 'o'],
                 '7': ['p', 'q', 'r', 's'],
                 '8': ['t', 'u', 'v'],
                 '9': ['w', 'x', 'y', 'z']}
        ans = []
        def formList(c,num):
            if len(num) == 0:
                ans.append(c)
            else:
                for i in dictionary[num[0]]:
                    formList(c+i,num[1:])
        
        if digits:
            formList("",digits)
        return ans
