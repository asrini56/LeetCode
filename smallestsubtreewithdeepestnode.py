# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def subtreeWithAllDeepest(self, root: TreeNode) -> TreeNode:
        self.m = float("-inf")
        self.ans = None
        def dfs(node,height):
            if not node:
                return height
            left = dfs(node.left,height+1)
            right = dfs(node.right,height+1)
            if left and right:
                if left == right:
                    if left > self.m:
                        self.m = left
                    if self.m == left:
                        self.ans = node
            return max(left,right)
        dfs(root,0)
        return self.ans
                
            
