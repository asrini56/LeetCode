from types import new_class


class LinkedList():
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

class Tree():
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BSTToLinkedList:

    def convert(self, root:Tree) -> LinkedList:
        if not root:
            return None
        
        head = None
        prev = None

        def dfs(root:Tree) -> LinkedList:
            nonlocal head, prev
            if not root:
                return None
            
            dfs(root.left)
            currentNode = LinkedList(root.val)

            if prev is None:
                head = currentNode
            else:
                prev.next = currentNode
                currentNode.prev = prev
            
            prev = currentNode

            dfs(root.right)
        
        dfs(root)
        return head

if __name__ == "__main__":

    tree1 = Tree(1)
    tree2 = Tree(4)
    tree3 = Tree(6)
    tree4 = Tree(2)
    tree1.left = tree2
    tree1.right = tree3
    tree2.left = tree4

    print(tree1)
    
    converter = BSTToLinkedList()
    result = converter.convert(tree1)

    curr = result
    vals = []
    while curr:
        vals.append(str(curr.val))
        curr = curr.next
    
    print(" <-> ".join(vals))



    

