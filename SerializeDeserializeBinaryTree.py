#297. Serialize and Deserialize Binary Tree
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:
    
    def dfs(self,root):
        if not root:
            return 'None'
        else:
            treeLeft = self.dfs(root.left)
            treeRight = self.dfs(root.right)
            return str(root.val) + "," + treeLeft + "," + treeRight

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        return self.dfs(root)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        result = data.split(',')
        def traverse():
            newNode = result.pop(0)
            if newNode == 'None':
                return None
            newTree = TreeNode(int(newNode))
            newTree.left = traverse()
            newTree.right = traverse()
            return newTree
        return traverse()

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
