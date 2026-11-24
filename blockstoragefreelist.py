
class BlockStorage:
    BLOCK_SIZE = 8

    def __init__(self, num_blocks=1000):
        self.blocks = [
            bytearray(b'?' * 8)
            for _ in range(num_blocks)
        ]

    def read(self, index):
        if index < 0 or index >= len(self.blocks):
            raise IndexError("Invalid block index")

        return bytes(self.blocks[index])

    def write(self, index, data):
        if index < 0 or index >= len(self.blocks):
            raise IndexError("Invalid block index")

        if len(data) > 8:
            raise ValueError("Data exceeds block size")

        # Deliberately do not clear remaining bytes.
        self.blocks[index][:len(data)] = data


class KVStoreFreeList:
    BLOCK_SIZE = 8

    def __init__(self, storage):
        self.storage = storage
        self.meta = {}
        self.next_block = 0
        self.free_blocks = []

    def allocate(self, count):
        block_ids = []

        for _ in range(count):
            if self.free_blocks:
                block_id = self.free_blocks.pop()
            else:
                block_id = self.next_block
                self.next_block += 1

            block_ids.append(block_id)

        return block_ids

    def release(self, block_ids):
        self.free_blocks.extend(block_ids)

    def set(self, key, value):
        data = value.encode("utf-8")
        size = len(data)

        num_blocks = (size + 7) // 8

        # Allocate new blocks first.
        new_blocks = self.allocate(num_blocks)

        # Write the new value.
        for i, block_id in enumerate(new_blocks):
            chunk = data[i * 8:(i + 1) * 8]

            self.storage.write(
                block_id,
                chunk.ljust(8, b'\0')
            )

        # Save old metadata.
        old = self.meta.get(key)

        # Update metadata.
        self.meta[key] = (new_blocks, size)

        # Reclaim old blocks.
        if old is not None:
            old_blocks, _ = old
            self.release(old_blocks)

    def get(self, key):
        if key not in self.meta:
            return None

        block_ids, size = self.meta[key]

        data = bytearray()

        for block_id in block_ids:
            data.extend(self.storage.read(block_id))

        return bytes(data[:size]).decode("utf-8")

    def delete(self, key):
        if key not in self.meta:
            return False

        block_ids, _ = self.meta.pop(key)

        self.release(block_ids)

        return True



def test_free_list():
    storage = BlockStorage()
    kv = KVStoreFreeList(storage)

    # Basic set/get
    kv.set("name", "Alice")
    assert kv.get("name") == "Alice"

    # Missing key
    assert kv.get("missing") is None

    # Empty string
    kv.set("empty", "")
    assert kv.get("empty") == ""

    # Exactly 8 bytes
    kv.set("eight", "12345678")
    assert kv.get("eight") == "12345678"

    # Multiple blocks
    kv.set("long", "Hello World!")
    assert kv.get("long") == "Hello World!"

    # Unicode
    kv.set("unicode", "你好世界")
    assert kv.get("unicode") == "你好世界"

    # Overwrite
    kv.set("name", "Bob")
    assert kv.get("name") == "Bob"

    # Delete
    assert kv.delete("name") is True
    assert kv.get("name") is None

    # Delete nonexistent key
    assert kv.delete("name") is False

    # Reuse deleted blocks
    kv.set("temp", "12345678")
    before = kv.next_block

    kv.delete("temp")
    kv.set("another", "ABCDEFGH")

    # Should reuse the freed block.
    assert kv.next_block == before
    assert kv.get("another") == "ABCDEFGH"

    # Overwrite with a larger value
    kv.set("another", "A" * 40)
    assert kv.get("another") == "A" * 40

    # Overwrite with an empty value
    kv.set("another", "")
    assert kv.get("another") == ""

    print("Free-list allocation: all tests passed!")


test_free_list()
