#66. Plus One, Time - O(n)
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        for i in range(len(digits)-1,-1,-1):
            if digits[i] < 9:
                digits[i]+=1
                return digits
            digits[i] = 0
        result = [0] * (len(digits)+1)
        result[0] = 1
        return result
    """
    Working - 
    [1,2,3] - 
    i = 2: 3-> 4
    return [1,2,4]
    
    [1,9,9] - 
    i=2, 9 -> 0
    i = 1 9 -> 0
    i = 0, 1 -> 2
    return 200
    """
    
