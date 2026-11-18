class Node:
    def __init__(self, key=0, val=0, freq=1, next=None, prev=None):
        self.key = key
        self.val = val
        self.freq = freq
        self.next = next
        self.prev = prev


class DoublyLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def addToHead(self, node: Node):
        nextNode = self.head.next
        self.head.next = node
        node.next = nextNode
        nextNode.prev = node
        node.prev = self.head
        self.size += 1

    def remove(self, node: Node):
        currentPrev = node.prev
        currentNext = node.next
        currentPrev.next = currentNext
        currentNext.prev = currentPrev
        self.size -= 1

    def popTail(self) -> Node:
        if self.size == 0:
            return None
        lru_node = self.tail.prev
        self.remove(lru_node)
        return lru_node


class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_node = {}      # Maps key -> Node
        self.freq_to_dll = {}      # Maps freq -> DoublyLinkedList

    def _update_freq(self, node: Node):
        curr_freq = node.freq
        dll = self.freq_to_dll[curr_freq]
        dll.remove(node)

        # If the min_freq DLL is now empty, increment min_freq
        if curr_freq == self.min_freq and dll.size == 0:
            self.min_freq += 1

        # Move node to the next frequency bucket
        node.freq += 1
        if node.freq not in self.freq_to_dll:
            self.freq_to_dll[node.freq] = DoublyLinkedList()
        self.freq_to_dll[node.freq].addToHead(node)

    def get(self, key: int) -> int:
        if key not in self.key_to_node:
            return -1
        
        node = self.key_to_node[key]
        self._update_freq(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        # Case 1: Key exists -> update value and bump frequency
        if key in self.key_to_node:
            node = self.key_to_node[key]
            node.val = value
            self._update_freq(node)
            return

        # Case 2: Capacity reached -> evict LFU (and LRU tie-broken) item
        if len(self.key_to_node) >= self.capacity:
            min_freq_dll = self.freq_to_dll[self.min_freq]
            lru_evict = min_freq_dll.popTail()
            del self.key_to_node[lru_evict.key]

        # Case 3: Insert new key with initial frequency 1
        node = Node(key, value, freq=1)
        self.key_to_node[key] = node
        self.min_freq = 1
        
        if 1 not in self.freq_to_dll:
            self.freq_to_dll[1] = DoublyLinkedList()
        self.freq_to_dll[1].addToHead(node)
