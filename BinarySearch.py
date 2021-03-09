#Time - O(logn)
def binary(nums,s):
    left = 0
    right = len(nums)-1
    while left <= right:
        mid = (left+right)//2
        if nums[mid] == s:
            return mid
        elif nums[mid] < s:
            left = mid+1
        else:
            right = mid-1
print(binary([3,6,10,14],10))
