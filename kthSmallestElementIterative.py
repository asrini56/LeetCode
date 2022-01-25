"""
Time complexity: O(H + k), where HH is a tree height. 
This complexity is defined by the stack, which contains at least H + kelements, 
since before starting to pop out one has to go down to a leaf. 
This results in O(logN+k) for the balanced tree and O(N+k) for completely unbalanced tree with all the nodes in the left subtree.
Space complexity: O(H) to keep the stack, where H is a tree height. 
That makes O(N) in the worst case of the skewed tree, and O(logN) in the average case of the balanced tree.
"""

class Solution:
    def kthSmallest(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """
        stack = []
        
        while True:
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            k -= 1
            if not k:
                return root.val
            root = root.right
