import collections

class LFUCache:
    """
    LFU (Least Frequently Used) Cache Implementation
    ------------------------------------------------
    Time Complexities:
        - get(key): O(1) time
        - put(key, value): O(1) time
        
    Space Complexity: O(capacity) to store keys, values, and frequencies.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_val = {}
        self.key_to_freq = {}
        # freq_to_keys maps: frequency -> OrderedDict of keys (LRU tie-breaker)
        self.freq_to_keys = collections.defaultdict(collections.OrderedDict)
        self.min_freq = 0

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        
        # Accessing the key increases its frequency: O(1)
        self._increment_freq(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        # If key exists, update value and bump frequency: O(1)
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._increment_freq(key)
            return

        # If cache is full, evict the LFU item (and LRU tie-breaker): O(1)
        if len(self.key_to_val) == self.capacity:
            # popitem(last=False) pops the oldest item in the minimum frequency bucket
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]

        # Insert new key with frequency 1: O(1)
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        
        # New items always reset min_freq to 1
        self.min_freq = 1

    def _increment_freq(self, key: int) -> None:
        freq = self.key_to_freq[key]
        self.key_to_freq[key] = freq + 1
        
        # Remove from old frequency bucket
        self.freq_to_keys[freq].pop(key)
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            # If empty bucket was our min_freq, increment min_freq
            if self.min_freq == freq:
                self.min_freq += 1

        # Add to new frequency bucket
        self.freq_to_keys[freq + 1][key] = None


# ==========================================
# EXAMPLE WALKTHROUGH
# ==========================================
if __name__ == "__main__":
    cache = LFUCache(2)  # Capacity of 2
    
    cache.put(1, 1)      # Cache is {1: 1}, frequencies: {1: freq 1}, min_freq = 1
    cache.put(2, 2)      # Cache is {1: 1, 2: 2}, frequencies: {1: 1, 2: 1}, min_freq = 1
    
    print(cache.get(1))  # Returns 1. Key 1 frequency becomes 2. freq_to_keys[1] has [2], freq_to_keys[2] has [1]
    
    cache.put(3, 3)      # Capacity (2) is full! 
                         # min_freq is 1, and the LRU key with freq 1 is key 2. 
                         # Evict key 2. Cache becomes {1: 1, 3: 3}.
                         
    print(cache.get(2))  # Returns -1 (not found, was evicted)
    print(cache.get(3))  # Returns 3. Key 3 frequency becomes 2.
    
    cache.put(4, 4)      # Capacity (2) is full again!
                         # min_freq is now 2. Both key 1 and key 3 have frequency 2.
                         # LRU tie-breaker evicts key 1 (the oldest inserted with freq 2).
                         # Cache becomes {3: 3, 4: 4}.
                         
    print(cache.get(1))  # Returns -1 (evicted)
    print(cache.get(3))  # Returns 3
    print(cache.get(4))  # Returns 4
