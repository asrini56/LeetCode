class Node:
    def __init__(self,key = 0, val=0, next = None, prev = None):
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cache = {}
    
    def addToHead(self, node:Node):
        nextNode = self.head.next
        self.head.next = node

        node.next = nextNode
        nextNode.prev = node
        node.prev = self.head

    
    def remove(self, node:Node):
        currentNode = node
        currentPrev = node.prev
        currentNext = node.next

        currentPrev.next = currentNext
        currentNext.prev = currentPrev
        

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self.remove(node)
            self.addToHead(node)
            return node.val
        return -1
        

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self.remove(node)
            self.addToHead(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self.remove(lru)
                del self.cache[lru.key]
            
            node = Node(key , value)
            self.addToHead(node)
            self.cache[key] = node
            
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
