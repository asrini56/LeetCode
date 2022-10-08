#134. Gas Station, Time - O(n)
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas) < sum(cost):
            return -1
        diff = [0] * len(gas)
        for i in range(len(gas)):
            diff[i] = gas[i] - cost[i]
        result = 0
        total = 0
        for i in range(len(diff)):
            total = total + diff[i]
            if total < 0:
                total = 0
                result = i + 1
        return result
