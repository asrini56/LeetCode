import time

class Node:
    def __init__(self, key=0, val=0, expiry=0, next=None, prev=None):
        self.key = key
        self.val = val
        self.expiry = expiry  # 1. Added expiry timestamp
        self.next = next
        self.prev = prev


class TTLLRUCache:

    def __init__(self, capacity: int, default_ttl: float = float('inf')):
        self.capacity = capacity
        self.default_ttl = default_ttl  # 2. Store default TTL in seconds
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cache = {}
    
    def addToHead(self, node: Node):
        nextNode = self.head.next
        self.head.next = node
        node.next = nextNode
        nextNode.prev = node
        node.prev = self.head

    def remove(self, node: Node):
        currentPrev = node.prev
        currentNext = node.next
        currentPrev.next = currentNext
        currentNext.prev = currentPrev
        

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            
            # 3. Lazy Expiration Check on read
            if node.expiry and time.time() > node.expiry:
                self.remove(node)
                del self.cache[key]
                return -1
            
            self.remove(node)
            self.addToHead(node)
            return node.val
        return -1
        

    def put(self, key: int, value: int, ttl: float = None) -> None:
        # Calculate absolute expiration time
        expire_time = time.time() + (ttl if ttl is not None else self.default_ttl)
        
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            node.expiry = expire_time  # Update expiry on overwrite
            self.remove(node)
            self.addToHead(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self.remove(lru)
                del self.cache[lru.key]
            
            node = Node(key, value, expiry=expire_time)
            self.addToHead(node)
            self.cache[key] = node
