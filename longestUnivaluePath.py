#687. Longest Univalue Path, Time - O(N)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def __init__(self):
        self.ans = 0
    def longestUnivaluePath(self, root: TreeNode) -> int:
        if not root:
            return 0
        self.findLongest(root,root.val)
        return self.ans
    def findLongest(self,root,previous):
        if not root:
            return 0
        left = self.findLongest(root.left,root.val)
        right = self.findLongest(root.right,root.val)
        self.ans = max(self.ans,left+right)
        if root.val == previous:
            return 1 + max(left,right)
        return 0
