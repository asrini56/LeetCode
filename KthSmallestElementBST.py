#230. Kth Smallest Element in a BST, Time - O(N), Space - O(N)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
import collections
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.res=[]
        def helper(root):
            if not root: return
            helper(root.left)
            self.res.append(root.val)
            helper(root.right)
        helper(root)
        return self.res[k-1]
