"""
Given an input list of integer ranges, find and output the ranges that overlap with at least 1 other range.
The order of ranges in the output is not important.
If a range appears more than once in the list, then it is considered an overlap with other instances of the
same range, hence the range must appear in the output as many times as it does in the input.
"""

import collections
temp = [
(1, 10),
(15, 20),
(101, 110),
(1, 10),
(1, 10),
(105, 120),
]

temp.sort()
answer = []
if len(temp) < 2:
    print([])
tempDict = collections.Counter(temp)
answerDict = collections.defaultdict(int)
print(temp)
maximum = temp[0][1]
lastMaxKey = temp[0]
for i in range(1,len(temp)):
    print(maximum)
    if temp[i][0] <= maximum:
        if answerDict[lastMaxKey] < tempDict[lastMaxKey]:
            answer.append(lastMaxKey)
            answerDict[lastMaxKey]+=1
        if answerDict[temp[i]] < tempDict[temp[i]]:
            answerDict[temp[i]]+=1
            answer.append(temp[i])
    if maximum < temp[i][1]:
        maximum = temp[i][1]
        lastMaxKey = temp[i]
print(answer)
