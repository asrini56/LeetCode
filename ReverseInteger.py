#7. Reverse Integer, Time - O(logN)
class Solution:
    def reverse(self, x: int) -> int:
        maxInt = pow(2,31)-1
        minInt = -pow(2,31)
        reverse = 0
        check = x
        x = abs(x)
        while x:
            pop = x % 10
            x = x // 10
            if reverse > maxInt//10:
                return 0
            if reverse <= minInt:
                return 0
            reverse = reverse * 10 + pop
        if check < 0:
            return -reverse
        return reverse
