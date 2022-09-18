#572. Subtree of Another Tree - Time - O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def checkTree(root1, root2):
            if not root1 and not root2:
                return True
            elif root1 and not root2 or root2 and not root1:
                return False
            
            if root1.val != root2.val:
                return False
            
            return checkTree(root1.left, root2.left) and checkTree(root1.right, root2.right)
        
        def dfs(root,subRoot):
            if not root:
                return False
            if root:
                if root.val == subRoot.val and checkTree(root, subRoot):
                    return True
                return (dfs(root.left,subRoot) or dfs(root.right,subRoot))
        return dfs(root,subRoot)
