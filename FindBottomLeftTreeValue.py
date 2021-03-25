# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
import collections
class Solution:
    def findBottomLeftValue(self, root: TreeNode) -> int:
        queue = collections.deque([root])
        ans = 0
        while queue:
            l = []
            for i in range(len(queue)):
                node = queue.popleft()
                l.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            if l:
                ans = l[0]
        return ans
