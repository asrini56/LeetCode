# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, greatest):
            if not node:
                return 0
            
            # Count current node if it's "good"
            count = 1 if node.val >= greatest else 0
            
            # Update the maximum value seen along this path
            new_greatest = max(greatest, node.val)
            
            # Sum up good nodes from left and right subtrees
            count += dfs(node.left, new_greatest)
            count += dfs(node.right, new_greatest)
            
            return count

        return dfs(root, root.val)
