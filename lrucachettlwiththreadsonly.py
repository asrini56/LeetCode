import threading
import time
from typing import Optional


class Node:

    def __init__(
        self,
        key: int = 0,
        val: int = 0,
        expiry: float = float("inf"),
        next: Optional["Node"] = None,
        prev: Optional["Node"] = None,
    ) -> None:
        self.key = key
        self.val = val
        self.expiry = expiry
        self.next = next
        self.prev = prev


class SweepingTTLLRUCache:

    def __init__(
        self,
        capacity: int,
        default_ttl: float = float("inf"),
        cleanup_interval: Optional[float] = None,
    ) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if default_ttl <= 0:
            raise ValueError("default_ttl must be positive")
        if cleanup_interval is not None and cleanup_interval <= 0:
            raise ValueError("cleanup_interval must be positive")

        self.capacity = capacity
        self.default_ttl = default_ttl
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cache: dict[int, Node] = {}

        self._cleanup_thread: Optional[threading.Thread] = None
        if cleanup_interval is not None:
            self._cleanup_thread = threading.Thread(
                target=self._cleanup_loop,
                args=(cleanup_interval,),
                name="ttl-lru-sweeper",
                daemon=True,
            )
            self._cleanup_thread.start()

    def _add_to_head(self, node: Node) -> None:
        first = self.head.next
        self.head.next = node
        node.next = first
        node.prev = self.head
        if first is not None:
            first.prev = node

    def _remove(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node is not None:
            prev_node.next = next_node
        if next_node is not None:
            next_node.prev = prev_node
        node.prev = None
        node.next = None

    def _evict_expired_locked(self, now: float) -> None:
        expired_keys = [
            key for key, node in self.cache.items() if now >= node.expiry
        ]
        for key in expired_keys:
            node = self.cache.pop(key)
            self._remove(node)

    def _cleanup_loop(self, interval: float) -> None:
        while not self._stop_event.wait(timeout=interval):
            with self._lock:
                self._evict_expired_locked(time.monotonic())

    def get(self, key: int) -> int:
        with self._lock:
            node = self.cache.get(key)
            if node is None:
                return -1

            now = time.monotonic()
            if now >= node.expiry:
                self._remove(node)
                del self.cache[key]
                return -1

            self._remove(node)
            self._add_to_head(node)
            return node.val

    def put(self, key: int, value: int, ttl: Optional[float] = None) -> None:
        effective_ttl = self.default_ttl if ttl is None else ttl
        if effective_ttl <= 0:
            raise ValueError("ttl must be positive")

        with self._lock:
            now = time.monotonic()
            expire_time = now + effective_ttl

            if key in self.cache:
                node = self.cache[key]
                node.val = value
                node.expiry = expire_time
                self._remove(node)
                self._add_to_head(node)
                return

            if len(self.cache) >= self.capacity:
                self._evict_expired_locked(now)

            while len(self.cache) >= self.capacity:
                lru = self.tail.prev
                if lru is None or lru is self.head:
                    break
                self._remove(lru)
                del self.cache[lru.key]

            node = Node(key, value, expiry=expire_time)
            self._add_to_head(node)
            self.cache[key] = node

    def close(self, timeout: Optional[float] = 2.0) -> None:
        self._stop_event.set()
        if self._cleanup_thread is not None and self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=timeout)

    def __enter__(self) -> "SweepingTTLLRUCache":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


if __name__ == "__main__":
    # 1. TTL expiration and LRU eviction demo
    with SweepingTTLLRUCache(capacity=2, default_ttl=5.0, cleanup_interval=0.2) as cache:
        cache.put(1, 100, ttl=0.3)  # Expires quickly
        cache.put(2, 200)           # Uses default_ttl (5.0s)
        print("Initial get(1):", cache.get(1))  # 100

        time.sleep(0.35)
        print("After TTL get(1):", cache.get(1))  # -1 (expired)

        cache.put(3, 300)  # Capacity is 2; key 2 is still live
        print("get(2):", cache.get(2))  # 200
        print("get(3):", cache.get(3))  # 300

        cache.put(4, 400)  # Evicts LRU entry if at capacity
        print("get(2) after put(4):", cache.get(2))
        print("get(3) after put(4):", cache.get(3))
        print("get(4) after put(4):", cache.get(4))

    # 2. Concurrent threads demo
    with SweepingTTLLRUCache(capacity=50, default_ttl=2.0, cleanup_interval=0.25) as shared_cache:
        def writer(worker_id: int) -> None:
            for offset in range(20):
                key = worker_id * 20 + offset
                shared_cache.put(key, key * 10, ttl=0.5)

        def reader(worker_id: int) -> None:
            hits = 0
            for _ in range(30):
                for offset in range(20):
                    key = ((worker_id + offset) % 4) * 20 + offset
                    if shared_cache.get(key) != -1:
                        hits += 1
                time.sleep(0.01)
            print(f"Reader {worker_id} observed {hits} hits")

        threads = [
            threading.Thread(target=writer, args=(0,)),
            threading.Thread(target=writer, args=(1,)),
            threading.Thread(target=reader, args=(0,)),
            threading.Thread(target=reader, args=(1,)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    print("Cache closed cleanly.")
