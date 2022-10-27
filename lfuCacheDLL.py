class Node:
    def __init__(self,key,val=0,freq=1,next=None,prev=None):
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev
        self.freq = freq

class DoubleLinkedList:
    def __init__(self):
        self.head = Node(0,0)
        self.tail = Node(-1,-1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
    
    def remove(self,nodeToRemove):
        prevNode = nodeToRemove.prev
        prevNode.next = nodeToRemove.next
        nodeToRemove.next.prev = prevNode
        self.size-=1
        
    def removeFromTail(self,nodeToRemove=None):
        if self.head.next == self.tail:
            return None
        nodeToRemove = self.tail.prev
        prevNode = nodeToRemove.prev
        prevNode.next = self.tail
        self.tail.prev = prevNode
        self.size-=1
        return nodeToRemove
    
    def makeHead(self,node=None):
        currentHead = self.head.next
        self.head.next = node
        node.next = currentHead
        node.prev = self.head
        currentHead.prev = node
        self.size+=1
        
class LFUCache:

    def __init__(self, capacity: int):
        self.freq = defaultdict(DoubleLinkedList)
        self.capacity = capacity
        self.hashMap = {}
        self.min = 1
        

    def get(self, key: int) -> int:
        if key not in self.hashMap:
            return -1
        node = self.hashMap[key]
        f = node.freq
        self.freq[f].remove(node)
        del self.hashMap[key]
        if self.min == f and not self.freq[f]:
            self.min+=1
        node.freq+=1
        self.freq[node.freq].makeHead(node)
        newNode = Node(node.key,node.val,node.freq)
        self.hashMap[key] = newNode
        return node.val
        
        

    def put(self, key: int, value: int) -> None:
        if key in self.hashMap:
            node = self.hashMap[key]
            f = node.freq
            self.freq[f].remove(node)
            if self.min == f and not self.freq[f]:
                self.min+=1
            f+=1
            node = Node(key,value,f)
            self.freq[f].makeHead(node)
        else:
            if self.capacity == len(self.hashMap.keys()):
                print(self.min)
                nodeToRemove = self.freq[self.min].removeFromTail()
                if nodeToRemove:
                    del self.hashMap[nodeToRemove.key]
            node = Node(key,value)
            self.hashMap[key] = node
            f = node.freq
            self.min = 1
            self.freq[1].makeHead(node)
        


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
