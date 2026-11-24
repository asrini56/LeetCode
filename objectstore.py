from dataclasses import dataclass
import threading
import time
from typing import Optional


@dataclass
class StoredObject:
    key: str
    data: bytes
    content_type: str
    size: int
    updated_at: float


class ObjectStorage:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._buckets: dict[str, dict[str, StoredObject]] = {}

    def create_bucket(self, bucket: str) -> None:
        if not bucket:
            raise ValueError("Bucket name cannot be empty")
        with self._lock:
            if bucket in self._buckets:
                raise ValueError(f"Bucket '{bucket}' already exists")
            self._buckets[bucket] = {}

    def delete_bucket(self, bucket: str, force: bool = False) -> None:
        with self._lock:
            objects = self._buckets.get(bucket)
            if objects is None:
                raise KeyError(f"Bucket '{bucket}' does not exist")
            if objects and not force:
                raise ValueError(f"Bucket '{bucket}' is not empty")
            del self._buckets[bucket]

    def put_object(
        self,
        bucket: str,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StoredObject:
        if not key:
            raise ValueError("Object key cannot be empty")
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Object data must be bytes-like")

        payload = bytes(data)
        with self._lock:
            objects = self._buckets.get(bucket)
            if objects is None:
                raise KeyError(f"Bucket '{bucket}' does not exist")

            obj = StoredObject(
                key=key,
                data=payload,
                content_type=content_type,
                size=len(payload),
                updated_at=time.monotonic(),
            )
            objects[key] = obj
            return StoredObject(
                key=obj.key,
                data=bytes(obj.data),
                content_type=obj.content_type,
                size=obj.size,
                updated_at=obj.updated_at,
            )

    def get_object(self, bucket: str, key: str) -> StoredObject:
        with self._lock:
            objects = self._buckets.get(bucket)
            if objects is None:
                raise KeyError(f"Bucket '{bucket}' does not exist")
            obj = objects.get(key)
            if obj is None:
                raise KeyError(f"Key '{key}' not found in bucket '{bucket}'")

            return StoredObject(
                key=obj.key,
                data=bytes(obj.data),
                content_type=obj.content_type,
                size=obj.size,
                updated_at=obj.updated_at,
            )

    def delete_object(self, bucket: str, key: str) -> bool:
        with self._lock:
            objects = self._buckets.get(bucket)
            if objects is None:
                raise KeyError(f"Bucket '{bucket}' does not exist")
            return objects.pop(key, None) is not None

    def list_objects(self, bucket: str, prefix: str = "") -> list[str]:
        with self._lock:
            objects = self._buckets.get(bucket)
            if objects is None:
                raise KeyError(f"Bucket '{bucket}' does not exist")
            return sorted(k for k in objects if k.startswith(prefix))


if __name__ == "__main__":
    store = ObjectStorage()
    store.create_bucket("checkpoints")

    store.put_object("checkpoints", "run1/step_100.pt", b"weights-100")
    store.put_object("checkpoints", "run1/step_200.pt", b"weights-200")
    store.put_object("checkpoints", "run2/step_100.pt", b"other-weights")

    print("List run1/:", store.list_objects("checkpoints", prefix="run1/"))
    fetched = store.get_object("checkpoints", "run1/step_200.pt")
    print("Fetched:", fetched.key, fetched.size, fetched.data)

    store.delete_object("checkpoints", "run1/step_100.pt")
    print("After delete:", store.list_objects("checkpoints", prefix="run1/"))
