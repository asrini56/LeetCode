# Platform: leetcode.com
# No. 227. Basic Calculator II
# Link: https://leetcode.com/problems/basic-calculator-ii/
# Difficulty: Medium
# Dev: Chumicat
# Date: 2020/11/24
# Submission: https://leetcode.com/submissions/detail/423635510/
# (Time, Space) Complexity : O(n), O(1)
class Solution:
    def calculate(self, s: str) -> int:
        # ret[0] + ret[1] sign ret[2] c
        ret, sign = [0, 0, 0], '+'
        for c in s + '+0+0':
            if c.isdigit():
                ret[2] = 10*ret[2] + int(c)
            elif c is not ' ':
                if sign is '*':
                    ret[1], ret[2] = ret[1]*ret[2], 0
                elif sign is '/':
                    ret[1], ret[2] = int(ret[1]/ret[2]), 0
                elif sign is '+':
                    ret[0], ret[1], ret[2] = ret[0]+ret[1], ret[2], 0
                elif sign is '-':
                    ret[0], ret[1], ret[2] = ret[0]+ret[1], -ret[2], 0
                sign = c
        return ret[0]
