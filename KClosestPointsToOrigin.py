# K Closest Points to Origin, Time - O(n)
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        def swap(left,right,nums):
            nums[left],nums[right] = nums[right],nums[left]
        def quickSelect(nums,st,end,pos):
            while True:
                if st > end:
                    break
                else:
                    pivot = st
                    left = st + 1
                    right = end
                    while left <= right:
                        if nums[left][1] > nums[pivot][1] and nums[right][1] < nums[pivot][1]:
                            swap(left,right,nums)
                        if nums[left][1] <= nums[pivot][1]:
                            left+=1
                        if nums[right][1] >= nums[pivot][1]:
                            right -= 1
                    swap(pivot,right,nums)
                    if right == pos:
                        return right
                    if right < pos:
                        st = right + 1
                    else:
                        end = right - 1
        l = []
        for i in range(len(points)):
            l.append((points[i],points[i][0]**2 + points[i][1]**2))
        pos = k
        limit = quickSelect(l,0,len(l)-1,pos)
        if limit == None:
            limit = len(l)
        ans = []
        for i in range(limit):
            ans.append(l[i][0])
        return ans
