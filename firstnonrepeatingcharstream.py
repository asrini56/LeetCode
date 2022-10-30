class DNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None


class DLinkedList:
    def __init__(self):
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def push(self, node):
        node.prev = self.tail.prev
        node.prev.next = node
        self.tail.prev = node
        node.next = self.tail

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev


class Solution:
    def firstUniqChar(self, s: str) -> int:
        existing = {}
        repititions = defaultdict(bool)
        dl = DLinkedList()
        for i, char in enumerate(s):
            h = ord(char) - ord("a")
            if h not in existing:
                node = DNode(i)
                existing[h] = node
                dl.push(node)
            elif not repititions[h]:
                repititions[h] = True
                node = existing[h]
                dl.remove(node)
        return dl.head.next.value if dl.head.next.value is not None else -1
