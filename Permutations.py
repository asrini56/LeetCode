#46. Permutations
#Time and space - O(n!)
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def permutation(i,nums,answer):
            if i == len(nums) - 1:
                answer.append(nums[:])
            else:
                for j in range(i,len(nums)):
                    nums[i],nums[j] = nums[j],nums[i]
                    permutation(i+1,nums,answer)
                    nums[i],nums[j] = nums[j],nums[i]
        answer = []
        permutation(0,nums,answer)
        return answer
