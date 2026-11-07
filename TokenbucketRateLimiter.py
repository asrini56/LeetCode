import threading
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: float = 10.0, refill_rate: float = 1.0):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def acquire(self, tokens: int = 1):
        with self.lock:
            now = time.time()
            time_since_refill = now - self.last_refill
            new_tokens = self.refill_rate * time_since_refill

            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False


limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=2.0)

print("Attempting rapid burst of 6 requests...")
for i in range(1, 7):
    success = limiter.acquire(1)
    print(f"Request {i}: {'Allowed' if success else 'Rate Limited'}")

print("\nWaiting 1.5 seconds for tokens to refill (at 2 tokens/sec)...")
time.sleep(1.5)

print("Attempting subsequent requests...")
for i in range(1, 4):
    success = limiter.acquire(1)
    print(f"Request {i}: {'Allowed' if success else 'Rate Limited'}")

