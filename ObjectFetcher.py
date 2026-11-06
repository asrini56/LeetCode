import concurrent.futures
import threading
import time


class ObjectFetcher:
    """
    A resilient concurrent object/storage client featuring exponential backoff,
    thread-safe error tracking, and non-blocking batch execution via ThreadPoolExecutor.
    """
    def __init__(self, max_workers: int = 4, max_retry: int = 3, backoff: float = 1.0):
        """
        Time Complexity: O(1)
        Constant time allocation for configuration primitives and locks.
        """
        self.max_workers = max_workers
        self.max_retry = max_retry
        self.backoff = backoff

        self.lock = threading.Lock()
        self.errors: dict[str, str] = {}
    
    def fetch_single_object(self, key: str):
        """
        Time Complexity: O(R * S) in the worst case
        - R: Number of retries (`max_retry`)
        - S: Size/cost of fetching the object data per attempt
        Retries up to `max_retry` times with exponential backoff on failure, 
        recording errors thread-safely under `self.lock`.
        """
        data = None
        error = None
        for i in range(self.max_retry):
            try:
                # fetch object (O(S) where S is payload size)
                data = "abc"
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
        """
        Overall Time Complexity: O((N * S) / W)
        - N: Total number of object keys (`len(object_keys)`)
        - S: Time to fetch a single object
        - W: Concurrency factor (`max_workers`)
        Submits N tasks into a thread pool, aggregates completed results asynchronously
        via `as_completed`, and isolates task exceptions without dropping the batch.
        """
        result = {}
        future_object_to_id = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for id in object_keys:
                future = executor.submit(self.fetch_single_object, id)
                future_object_to_id[future] = id
            
            for future in concurrent.futures.as_completed(future_object_to_id):
                try:
                    data = future.result()
                    id = future_object_to_id[future]
                    result[id] = data
                except Exception as e:
                    print(f"Error for id: {id}, error - {str(e)}")
        
        return result


# --- Test Harness ---

# 1. Instantiate our ObjectFetcher with 4 workers, 3 retries, and 0.1s base backoff
fetcher = ObjectFetcher(max_workers=4, max_retry=3, backoff=0.1)

# 2. Define a list of test object keys
keys = ["obj_1", "obj_2", "obj_3", "obj_4", "obj_5"]

print("Starting concurrent object fetching...")
results = fetcher.fetch_objects(keys)

print("\n--- Results ---")
for key, data in results.items():
    print(f"Key: {key} -> Data: {data}")

print("\n--- Errors Logged ---")
if fetcher.errors:
    for key, err in fetcher.errors.items():
        print(f"Failed Key: {key} -> Error: {err}")
else:
    print("No errors encountered!")
