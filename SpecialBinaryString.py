#761. Special Binary String, Time - O(n^2),space - O(n),where N is the length of S.
#MOUNTAIN - PEAKS AND VALLEYS
class Solution(object):
    def makeLargestSpecial(self, S):
        if not S: return S
        mountains = []
        anchor = bal = 0
        for i, x in enumerate(S):
            bal += 1 if x == '1' else -1
            if bal == 0:
                mountains.append("1{}0".format(
                    self.makeLargestSpecial(S[anchor+1: i])))
                anchor = i+1
        mountains.sort(reverse = True)
        print(mountains)
        return "".join(mountains)
