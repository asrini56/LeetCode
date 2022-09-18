#1448. Count Good Nodes in Binary Tree, Time - O(N)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        self.good = 0
        def dfs(root,maximum):
            if not root:
                return
            if root.val >= maximum:
                self.good+=1
            dfs(root.left,max(root.val,maximum))
            dfs(root.right,max(root.val,maximum))
        if not root:
            return self.good
        dfs(root,root.val)
        return self.good
