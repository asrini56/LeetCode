class DoubleLinkedList:
    def __init__(self,key = 0,val=0,next=None,prev=None):
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev
class LRUCache:

    def __init__(self, capacity: int):
        self.hashMap = {}
        self.capacity = capacity
        self.head = DoubleLinkedList(0,0)
        self.tail = DoubleLinkedList(-1,-1)
        self.head.next = self.tail
        self.tail.prev = self.head
        

    def get(self, key: int) -> int:
        if key not in self.hashMap:
            return -1
        else:
            node = self.hashMap[key]
            self.remove(node)
            self.makeHead(node)
            return node.val
            
        

    def put(self, key: int, value: int) -> None:
        if key not in self.hashMap:
            if len(self.hashMap) == self.capacity:
                nodeToRemove = self.tail.prev
                keyToRemove = nodeToRemove.key
                node = DoubleLinkedList(key,value)
                self.removeFromTail(nodeToRemove)
                del self.hashMap[keyToRemove]
            node = DoubleLinkedList(key,value)
            self.makeHead(node)
            self.hashMap[key] = node
        elif key in self.hashMap:
            node = self.hashMap[key]
            self.remove(node)
            node = DoubleLinkedList(key,value)
            self.makeHead(node)
            self.hashMap[key] = node
    
    def remove(self,nodeToRemove):
        prevNode = nodeToRemove.prev
        prevNode.next = nodeToRemove.next
        nodeToRemove.next.prev = prevNode
        
    def removeFromTail(self,nodeToRemove):
        prevNode = nodeToRemove.prev
        prevNode.next = self.tail
        self.tail.prev = prevNode
    
    def makeHead(self,node):
        currentHead = self.head.next
        self.head.next = node
        node.next = currentHead
        node.prev = self.head
        currentHead.prev = node
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
