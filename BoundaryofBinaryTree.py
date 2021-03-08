#545. Boundary of Binary Tree, Time - O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def boundaryOfBinaryTree(self, root: TreeNode) -> List[int]:
        if not root:
            return []
        result = []
        result.append(root.val)
        self.left(root.left,result)
        self.leaves(root.left,result)
        self.leaves(root.right,result)
        self.right(root.right,result)
        return result
    def left(self,root,result):
        if not root or (not root.left and not root.right):
            return
        result.append(root.val)
        if root.left:
            self.left(root.left,result)
        if not root.left:
            self.left(root.right,result)
    def right(self,root,result):
        if not root or (not root.left and not root.right):
            return
        if root.right:
            self.right(root.right,result)
        if not root.right:
            self.right(root.left,result)
        result.append(root.val)
    def leaves(self,root,result):
        if not root:
            return
        if root.left == None and root.right == None:
            result.append(root.val)
        self.leaves(root.left,result)
        self.leaves(root.right,result)
