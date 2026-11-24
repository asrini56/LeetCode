import heapq
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

        # Min-heap entries: (expiry_timestamp, monotonic_seq, key)
        self._expiry_heap: list[tuple[float, int, int]] = []
        self._seq = 0

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

    def _schedule_expiry(self, key: int, expiry: float) -> None:
        if expiry < float("inf"):
            self._seq += 1
            heapq.heappush(self._expiry_heap, (expiry, self._seq, key))

    def _purge_expired_locked(self, now: float) -> None:
        while self._expiry_heap and self._expiry_heap[0][0] <= now:
            expiry, _, key = heapq.heappop(self._expiry_heap)
            node = self.cache.get(key)
            # Ignore stale heap entries from prior overwrites, deletes, or evictions.
            if node is None or node.expiry != expiry:
                continue
            if now >= node.expiry:
                self._remove(node)
                del self.cache[key]

    def _cleanup_loop(self, interval: float) -> None:
        while not self._stop_event.wait(timeout=interval):
            with self._lock:
                self._purge_expired_locked(time.monotonic())

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
                self._schedule_expiry(key, expire_time)
                return

            if len(self.cache) >= self.capacity:
                self._purge_expired_locked(now)

            while len(self.cache) >= self.capacity:
                lru = self.tail.prev
                if lru is None or lru is self.head:
                    break
                self._remove(lru)
                del self.cache[lru.key]

            node = Node(key, value, expiry=expire_time)
            self._add_to_head(node)
            self.cache[key] = node
            self._schedule_expiry(key, expire_time)

    def close(self, timeout: Optional[float] = 2.0) -> None:
        self._stop_event.set()
        if self._cleanup_thread is not None and self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=timeout)

    def __enter__(self) -> "SweepingTTLLRUCache":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
