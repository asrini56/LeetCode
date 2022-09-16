#104. Maximum Depth of Binary Tree - Time - O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        maximum = 0
        def dfs(root,count):
            nonlocal maximum
            if not root.left and not root.right:
                if maximum < count:
                    maximum = count
                    return
            else:
                count+=1
                if root.left:
                    dfs(root.left,count)
                if root.right:
                    dfs(root.right,count)
        dfs(root,1)
        return maximum
