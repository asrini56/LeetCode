
import threading
from datetime import datetime

class GPUQuotaManager:
    def __init__(self):
        self.tenants = {}
        self.lock = threading.Lock()

    def add_tenant(self, tenant_id, quota):
        self.tenants[tenant_id] = {
            "quota": quota,
            "used": 0,
            "month": datetime.now().month
        }

    def allocate(self, tenant_id, gpu_count, hours):
        cost = gpu_count * hours

        with self.lock:
            tenant = self.tenants[tenant_id]

            # Reset usage if a new month starts.
            current_month = datetime.now().month

            if tenant["month"] != current_month:
                tenant["used"] = 0
                tenant["month"] = current_month

            if tenant["used"] + cost > tenant["quota"]:
                return False

            tenant["used"] += cost
            return True

    def get_remaining(self, tenant_id):
        tenant = self.tenants[tenant_id]
        return tenant["quota"] - tenant["used"]

manager = GPUQuotaManager()

manager.add_tenant("A", 100)

# 4 GPUs * 2 hours = 8
assert manager.allocate("A", 4, 2)
assert manager.get_remaining("A") == 92

# 8 GPUs * 10 hours = 80
assert manager.allocate("A", 8, 10)
assert manager.get_remaining("A") == 12

# 4 GPUs * 4 hours = 16
assert not manager.allocate("A", 4, 4)
assert manager.get_remaining("A") == 12

print("All tests passed!")
