#103. Binary Tree Zigzag Level Order Traversal
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        queue = deque([root])
        result = []
        r = 1
        while queue:
            l = []
            for i in range(len(queue)):
                node = queue.popleft()
                l.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            if r == 1:
                result.append(l)
                r = -1
            else:
                l.reverse()
                result.append(l)
                r = 1
        return result
