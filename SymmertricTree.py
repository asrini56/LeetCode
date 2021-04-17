#101. Symmetric Tree, Time - O(n)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
import collections
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        queue = deque([root.left,root.right])
        while queue:
            node,node1 = queue.popleft(),queue.popleft()
            if not node1 and not node:
                continue
            if not node or not node1:
                return False
            if node.val != node1.val:
                return False
            queue+= [node.right, node1.left,node.left,node1.right]
        return True
