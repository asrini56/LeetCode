#138. Copy List with Random Pointer, Time - O(n)
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        dictionary = collections.defaultdict(lambda: Node(0, None, None))
        dictionary[None] = None
        node = head
        while node:
            dictionary[node].val = node.val
            dictionary[node].next = dictionary[node.next]
            dictionary[node].random = dictionary[node.random]
            node = node.next
        return dictionary[head]
