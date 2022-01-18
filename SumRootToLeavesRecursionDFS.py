#129. Sum Root to Leaf Numbers, Time - O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumNumbers(self, root: TreeNode) -> int:
        self.ans = 0
        def dfs(root,s):
            if not root:
                return 0
            if not root.left and not root.right:
                s+=str(root.val)
                self.ans+=int(s)
                s = ""
            s+=str(root.val)   
            if root.left:
                dfs(root.left,s)
            if root.right:
                dfs(root.right,s)
        dfs(root,"")
        return self.ans
        
