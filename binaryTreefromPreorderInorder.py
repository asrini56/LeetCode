#105. Construct Binary Tree from Preorder and Inorder Traversal, Time and Space - O(N)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        def arrayToTree(left,right):
            nonlocal index
            if left > right:
                return None
            val = preorder[index]
            root = TreeNode(val)
            index+=1
            root.left = arrayToTree(left,hmap[val]-1)
            root.right = arrayToTree(hmap[val]+1,right)
            return root
        index = 0
        hmap = {}
        for i,value in enumerate(inorder):
            hmap[value] = i
        
        return arrayToTree(0,len(preorder)-1)
            
