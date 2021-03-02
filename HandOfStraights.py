#846. Hand of Straights, Time - O(nlogn) + O(n*W)
from collections import Counter
class Solution:
    def isNStraightHand(self, hand: List[int], W: int) -> bool:
        if len(hand) < W:
            return False
        hand.sort()
        counter = Counter(hand)
        i,j = 0,len(hand)
        while i < j:
            current = hand[i]
            for k in range(W):
                curr = current + k
                if curr not in counter:
                    return False
                elif counter[curr] == 1:
                    del counter[curr]
                else:
                    counter[curr]-=1
            while i < j and hand[i] not in counter:
                i+=1
        return True
