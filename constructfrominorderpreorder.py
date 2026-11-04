from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """
        Reconstructs a unique binary tree given its preorder and inorder traversals.
        
        Algorithm Overview:
        - Preorder traversal (Root -> Left -> Right) tells us the ROOT of each subtree in order.
        - Inorder traversal (Left -> Root -> Right) tells us the BOUNDARIES of left and right subtrees.
        - We use a hash map for O(1) index lookups in the inorder list.
        
        Example Walkthrough:
        -------------------
        preorder = [3, 9, 20, 15, 7]
        inorder  = [9, 3, 15, 20, 7]
        
        1. Hash Map created: temp = {9:0, 3:1, 15:2, 20:3, 7:4}
        2. Initial call: build(left=0, right=4)
           - self.j = 0 -> Root value = preorder[0] = 3
           - temp[3] = index 1 in inorder
           - Left Subtree range in inorder: [0, 0]   (contains [9])
           - Right Subtree range in inorder: [2, 4]  (contains [15, 20, 7])
           
        3. Build Left Subtree: build(left=0, right=0)
           - self.j = 1 -> Root value = preorder[1] = 9
           - temp[9] = index 0 in inorder
           - Left call: build(0, -1) -> returns None
           - Right call: build(1, 0) -> returns None
           - Returns Node(9)
           
        4. Build Right Subtree: build(left=2, right=4)
           - self.j = 2 -> Root value = preorder[2] = 20
           - temp[20] = index 3 in inorder
           - Left call: build(2, 2) -> creates Node(15)
           - Right call: build(4, 4) -> creates Node(7)
           - Returns Node(20) with left=15, right=7
           
        5. Final Tree:
                3
               / \
              9  20
                /  \
               15   7
        """
        # Step 1: Pre-map every inorder value to its index for O(1) lookups
        temp = {val: idx for idx, val in enumerate(inorder)}
        self.j = 0  # Pointer moving sequentially through preorder array
        
        def build(left: int, right: int) -> Optional[TreeNode]:
            # Base Case: No elements remaining in this subtree range
            if left > right:
                return None
            
            # Step 2: Select the current root from preorder traversal
            val = preorder[self.j]
            self.j += 1
            root = TreeNode(val)
            
            # Step 3: Find root's position in inorder array to divide subtrees
            inorder_idx = temp[val]
            
            # Step 4: Recursively construct Left and Right subtrees
            # Left subtree elements fall in inorder range [left, inorder_idx - 1]
            root.left = build(left, inorder_idx - 1)
            
            # Right subtree elements fall in inorder range [inorder_idx + 1, right]
            root.right = build(inorder_idx + 1, right)
            
            return root
        
        return build(0, len(inorder) - 1)

# --- Example Usage & Validation ---
sol = Solution()

# Test Case 1
preorder1 = [3, 9, 20, 15, 7]
inorder1 = [9, 3, 15, 20, 7]
root1 = sol.buildTree(preorder1, inorder1)

print(f"Root value: {root1.val}")            # Output: 3
print(f"Left child: {root1.left.val}")        # Output: 9
print(f"Right child: {root1.right.val}")      # Output: 20
print(f"Right-Left child: {root1.right.left.val}")   # Output: 15
print(f"Right-Right child: {root1.right.right.val}") # Output: 7
