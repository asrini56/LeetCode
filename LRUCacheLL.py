"""
The most frequent operation of the problem is changing the node position in the list.
Change position of the node means two operations, delete and insert.
Double linked list data structure takes constant time O(1) to insert or delete nodes a linked list by repointing the previous and next pointer of the node.
Array data structure takes O(n) to insert or delete an element in the list by shifting all the element behind the position (backward for insertion, forward for deletion) by one.

put :
if the key is already in the cache, we update the value, remove the key node and insert the key node after the head;
if the key is not in cache, if the cache is not full,we insert the new key node after the head. If the cache is full, we delete the node before the tail to make room for the new key node, and insert the new key node after the head.

get:
return the value of the key.
remove the key node.
insert the key node after the head.
"""
class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.dic = dict() # key to node
        self.capacity = capacity
        self.head = ListNode(0, 0)
        self.tail = ListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key in self.dic:
            node = self.dic[key]
            self.removeFromList(node)
            self.insertIntoHead(node)
            return node.value
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self.dic:             # similar to get()        
            node = self.dic[key]
            self.removeFromList(node)
            self.insertIntoHead(node)
            node.value = value         # replace the value len(dic)
        else: 
            if len(self.dic) >= self.capacity:
                self.removeFromTail()
            node = ListNode(key,value)
            self.dic[key] = node
            self.insertIntoHead(node)
			
    def removeFromList(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def insertIntoHead(self, node):
        headNext = self.head.next 
        self.head.next = node 
        node.prev = self.head 
        node.next = headNext 
        headNext.prev = node
    
    def removeFromTail(self):
        if len(self.dic) == 0: return
        tail_node = self.tail.prev
        del self.dic[tail_node.key]
        self.removeFromList(tail_node)
