# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def widthOfBinaryTree(self, root: TreeNode) -> int:
        queue = collections.deque()
        queue.append((root,1))
        result = 0
        while queue:
            result = max(result,queue[-1][1] - queue[0][1] + 1)
            for i in range(len(queue)):
                node,pos = queue.popleft()
                if node.left:
                    queue.append((node.left,pos*2))
                if node.right:
                    queue.append((node.right,pos*2 + 1))
        return result
