
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


class KVStore:
    BLOCK_SIZE = 8

    def __init__(self, storage):
        self.storage = storage
        self.meta = {}
        self.next_block = 0

    def set(self, key, value):
        data = value.encode("utf-8")
        size = len(data)

        num_blocks = (size + 7) // 8
        start = self.next_block

        for i in range(num_blocks):
            chunk = data[i * 8:(i + 1) * 8]
            self.storage.write(
                start + i,
                chunk.ljust(8, b'\0')
            )

        # Update metadata after writing.
        self.meta[key] = (start, size)
        self.next_block += num_blocks

    def get(self, key):
        if key not in self.meta:
            return None

        start, size = self.meta[key]
        num_blocks = (size + 7) // 8

        data = bytearray()

        for i in range(num_blocks):
            data.extend(self.storage.read(start + i))

        return bytes(data[:size]).decode("utf-8")

    def delete(self, key):
        if key not in self.meta:
            return False

        del self.meta[key]
        return True



def test_sequential():
    storage = BlockStorage()
    kv = KVStore(storage)

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

    # More than 8 bytes
    kv.set("long", "Hello World!")
    assert kv.get("long") == "Hello World!"

    # Multiple blocks
    kv.set("large", "A" * 100)
    assert kv.get("large") == "A" * 100

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

    print("Sequential allocation: all tests passed!")


test_sequential()
