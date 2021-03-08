#250. Count Univalue Subtrees, Time - O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countUnivalSubtrees(self, root: TreeNode) -> int:
        if not root:
            return 0
        self.count = 0
        self.checkUnique(root)
        return self.count
    def checkUnique(self,root):
        #Leaf Node
        if not root.left and not root.right:
            self.count+=1
            return True
        isUnique = True
        if root.left:
            isUnique = self.checkUnique(root.left) and isUnique and root.left.val == root.val
        if root.right:
            isUnique = self.checkUnique(root.right) and isUnique and root.right.val == root.val
        if isUnique:
            self.count+=1
        return isUnique
