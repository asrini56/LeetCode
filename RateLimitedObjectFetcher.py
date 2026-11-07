import concurrent.futures
import threading
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: float = 10.0, refill_rate: float = 1.0):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def acquire(self, tokens: int = 1, timeout: float = 5.0) -> bool:
        start_time = time.time()
        
        while True:
            with self.lock:
                now = time.time()
                elapsed = now - self.last_refill
                self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
                self.last_refill = now
                
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True
                
                deficit = tokens - self.tokens
                sleep_duration = deficit / self.refill_rate
            
            if timeout is not None and (time.time() - start_time) + sleep_duration > timeout:
                return False
            
            time.sleep(sleep_duration)


class RateLimitedObjectFetcher:
    def __init__(self, max_workers: int = 4, max_retry: int = 3, backoff: float = 1.0, 
                 capacity: float = 5.0, refill_rate: float = 2.0):
        self.max_workers = max_workers
        self.max_retry = max_retry
        self.backoff = backoff
        
        self.rate_limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)
        self.lock = threading.Lock()
        self.errors: dict[str, str] = {}
    
    def fetch_single_object(self, key: str):
        # 1. Acquire rate limiter token before initiating fetch (blocks if rate-limited)
        if not self.rate_limiter.acquire(tokens=1, timeout=3.0):
            raise TimeoutError("Rate limit exceeded and timeout reached while waiting for tokens.")
        
        data = None
        error = None
        for i in range(self.max_retry):
            try:
                # Simulated remote object storage fetch
                data = f"data_for_{key}"
                break
            except Exception as e:
                error = e
                timeToSleep = self.backoff * (2 ** i)
                time.sleep(timeToSleep)
        
        if not data and error:
            with self.lock:
                self.errors[key] = str(error)
                raise error
        
        return data
    
    def fetch_objects(self, object_keys: list[str]) -> dict[str, any]:
        result = {}
        future_object_to_id = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for key in object_keys:
                future = executor.submit(self.fetch_single_object, key)
                future_object_to_id[future] = key
            
            for future in concurrent.futures.as_completed(future_object_to_id):
                key = future_object_to_id[future]
                try:
                    result[key] = future.result()
                except Exception as e:
                    result[key] = None
        
        return result


# --- Test Harness ---
if __name__ == "__main__":
    client = RateLimitedObjectFetcher(max_workers=4, max_retry=2, backoff=0.1, capacity=3.0, refill_rate=5.0)
    keys = [f"obj_{i}" for i in range(1, 10)]

    print(f"Starting rate-limited fetch for {len(keys)} keys...")
    start_time = time.time()
    results = client.fetch_objects(keys)
    duration = time.time() - start_time

    print(f"\nCompleted in {duration:.2f} seconds.")
    for k, v in results.items():
        print(f"{k} -> {v}")
