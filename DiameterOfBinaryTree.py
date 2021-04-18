#543. Diameter of Binary Tree,Time - O(N)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        self.ans = 0
        def findMax(root):
            if not root:
                return 0
            left = findMax(root.left)
            right = findMax(root.right)
            if left+right > self.ans:
                self.ans = left+right
            return 1+max(left,right)
        findMax(root)
        return self.ans
