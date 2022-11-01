#2381. Shifting Letters II -> Time - O(n)
"""
Instead of shifting every character in each shift, could you keep track of which characters are shifted and by how much across all shifts?
Try marking the start and ends of each shift, then perform a prefix sum of the shifts.
"""
class Solution:
    def shiftingLetters(self, s: str, shifts: List[List[int]]) -> str:
        s = list(s)
        cum_shift = [0]*(len(s)+1)
        cum = 0
        for start, end, direc in shifts:
            if direc == 0:
                cum_shift[start] -= 1
                cum_shift[end+1] += 1
            else:
                cum_shift[start] += 1
                cum_shift[end+1] -= 1
        for i in range(len(s)):
            cum += cum_shift[i]
            s[i] = chr((ord(s[i]) - 97 + cum) % 26 + 97)
        return "".join(s)
