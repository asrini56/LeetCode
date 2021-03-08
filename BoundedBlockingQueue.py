#1188. Design Bounded Blocking Queue
import threading
from collections import deque
class BoundedBlockingQueue(object):

    def __init__(self, capacity: int):
        self.cap = capacity
        self.queue = deque()
        self.pushing = threading.Semaphore(self.cap)
        self.pulling = threading.Semaphore(0)
        self.editing = threading.Lock()
    
    def enqueue(self, element: int) -> None:
        self.pushing.acquire()
        self.editing.acquire()
        self.queue.append(element)
        self.pulling.release()
        self.editing.release()
    def dequeue(self) -> int:
        self.pulling.acquire()
        self.editing.acquire()
        result = self.queue.popleft()
        self.pushing.release()
        self.editing.release()
        return result

    def size(self) -> int:
        return len(self.queue)
