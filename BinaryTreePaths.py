# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        self.ans = []
        def dfs(root,s):
            if not root.left and not root.right:
                self.ans.append(s+str(root.val))
            if root.left:
                left = dfs(root.left,s+str(root.val)+"->")
            if root.right:
                right = dfs(root.right,s+str(root.val)+"->")
        dfs(root,"")
        return self.ans
