import threading
from typing import Dict

class ResourceManager:
    """
    A thread-safe resource and capacity allocator that tracks available blocks 
    across a pool of nodes, preventing race conditions under high concurrency.
    """
    def __init__(self, capacity: Dict[str, int]):
        # Keep a baseline reference of the maximum capacity per resource
        self.max_resource_capacity = capacity.copy()
        # Active available capacity tracker
        self.capacity = capacity.copy()
        # Explicit lock to guard all state mutations
        self.lock = threading.Lock()
    
    def allocate(self, resource_id: str, amount: int) -> bool:
        """
        Attempts to atomically allocate the requested amount of capacity for a resource.
        Returns True if successful, False if insufficient capacity or unknown resource.
        """
        if amount <= 0:
            raise ValueError("Allocation amount must be greater than zero.")
            
        with self.lock:
            if resource_id not in self.capacity:
                return False
                
            if self.capacity[resource_id] >= amount:
                self.capacity[resource_id] -= amount
                return True
                
            return False

    def release(self, resource_id: str, amount: int) -> None:
        """
        Releases allocated capacity back to the resource pool, ensuring 
        it never exceeds the original maximum initialized capacity.
        """
        if amount <= 0:
            raise ValueError("Release amount must be greater than zero.")
            
        with self.lock:
            if resource_id not in self.max_resource_capacity:
                raise KeyError(f"Unknown resource_id: {resource_id}")
                
            current = self.capacity.get(resource_id, 0)
            max_cap = self.max_resource_capacity[resource_id]
            
            # Clamp the new capacity so it never overflows past the maximum limit
            self.capacity[resource_id] = min(max_cap, current + amount)


# --- Test Harness ---
if __name__ == "__main__":
    # Initialize resource manager with compute blocks / GPU nodes
    initial_pools = {"node-gpu-01": 16, "node-gpu-02": 32}
    manager = ResourceManager(initial_pools)

    # Test concurrent allocations
    import concurrent.futures

    def worker_job(res_id, amt):
        success = manager.allocate(res_id, amt)
        return res_id, amt, success

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(worker_job, "node-gpu-01", 4),
            executor.submit(worker_job, "node-gpu-01", 8),
            executor.submit(worker_job, "node-gpu-01", 10), # Should fail (only 16 total)
        ]
        
        for future in concurrent.futures.as_completed(futures):
            res_id, amt, success = future.result()
            print(f"Allocating {amt} on {res_id}: {'SUCCESS' if success else 'FAILED (Insufficient Capacity)'}")

    print(f"Remaining capacity: {manager.capacity}")
    
    # Test release
    manager.release("node-gpu-01", 8)
    print(f"Capacity after releasing 8 units: {manager.capacity}")
