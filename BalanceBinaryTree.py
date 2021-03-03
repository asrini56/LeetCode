#1382. Balance a Binary Search Tree
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def balanceBST(self, root: TreeNode) -> TreeNode:
        nums = []
        def createInorder(node,nums):
            if node:
                createInorder(node.left,nums)
                nums.append(node.val)
                createInorder(node.right,nums)
        
        def createBalanced(left,right,nums):
            if left > right:
                return None
            else:
                mid = (left+right)//2
                root = TreeNode(nums[mid])
                root.left = createBalanced(left,mid-1,nums)
                root.right = createBalanced(mid+1,right,nums)
                return root
        createInorder(root,nums)
        return createBalanced(0,len(nums)-1,nums)
