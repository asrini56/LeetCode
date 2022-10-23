#Time - O(H)
def find(root,target):
    if not root:
        return
    successor = None
    while root:
        if root.data <= target:
            root = root.right
        else:
            successor = root
            root = root.left
    print(successor.data)
