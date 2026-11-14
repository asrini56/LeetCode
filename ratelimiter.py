"""
=============================================================================
CLASS-LEVEL DESIGN & ARCHITECTURAL DOCUMENTATION: EXTENSIBLE RATE LIMITER
=============================================================================
1. Architecture & Design Patterns:
   - Strategy Pattern: `RateLimiter` serves as an abstract base class strategy 
     interface allowing concrete algorithms (TokenBucketAlgorithm, FixedWindow, 
     SlidingWindowLog) to be plugged in interchangeably.
   - Facade Pattern: `RateLimitManager` acts as the unified entry point, managing 
     tier-based configurations and delegating requests to the correct limiter instance.

2. Concurrency & Thread Safety:
   - Fine-Grained Locking: Each algorithm implementation utilizes thread locks 
     (`threading.Lock`) to prevent race conditions during concurrent state updates.
=============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
import threading
import time
import collections

class Type(Enum):
    BASIC = 1
    PREMIUM = 2


# =============================================================================
# class RateLimiterConfig:
# - maxAllowedRequests
# - refillTime
# =============================================================================
class RateLimiterConfig:
    """Encapsulates configuration rules for request thresholds and time windows."""
    def __init__(self, maxAllowedRequests: int, refillTime: int):
        self.maxAllowedRequests = maxAllowedRequests
        self.refillTime = refillTime


# =============================================================================
# class RateLimiter: -> abstract class
#     +allowrequests(requestId: str, type)
# =============================================================================
class RateLimiter(ABC):
    """Abstract base class strategy interface for rate-limiting algorithms."""
    @abstractmethod
    def allowrequests(self, requestId: str) -> bool:
        pass


# =============================================================================
# class TokenBucketAlgorithm -> implements RateLimiter :
# - configRule: RateLimiterConfig
#     +allowrequests(requestId)
# =============================================================================
class TokenBucketAlgorithm(RateLimiter):
    def __init__(self, configRule: RateLimiterConfig):
        self.configRule = configRule
        self.capacity = configRule.maxAllowedRequests
        self.refill_time = configRule.refillTime
        self._buckets: dict[str, tuple[float, float]] = {}
        self._lock = threading.Lock()

    def allowrequests(self, requestId: str) -> bool:
        now = time.time()
        with self._lock:
            if requestId not in self._buckets:
                self._buckets[requestId] = (float(self.capacity), now)
            
            tokens, last_refill = self._buckets[requestId]
            elapsed = now - last_refill
            tokens_to_add = elapsed * (self.capacity / self.refill_time)
            tokens = min(float(self.capacity), tokens + tokens_to_add)
            
            if tokens >= 1.0:
                tokens -= 1.0
                self._buckets[requestId] = (tokens, now)
                return True
            
            self._buckets[requestId] = (tokens, now)
            return False


# =============================================================================
# class FixedWindow -> implements RateLimiter :
# - configRule: RateLimiterConfig
#     +allowrequests(requestId)
# =============================================================================
class FixedWindow(RateLimiter):
    def __init__(self, configRule: RateLimiterConfig):
        self.configRule = configRule
        self.max_requests = configRule.maxAllowedRequests
        self.window_size = configRule.refillTime
        self._windows: dict[str, tuple[float, int]] = {}
        self._lock = threading.Lock()

    def allowrequests(self, requestId: str) -> bool:
        now = time.time()
        with self._lock:
            if requestId not in self._windows:
                self._windows[requestId] = (now, 1)
                return True
            
            window_start, count = self._windows[requestId]
            if now - window_start >= self.window_size:
                self._windows[requestId] = (now, 1)
                return True
            
            if count < self.max_requests:
                self._windows[requestId] = (window_start, count + 1)
                return True
            
            return False


# =============================================================================
# class SlidingWindowLog -> implements RateLimiter :
# - configRule: RateLimiterConfig
#     +allowrequests(requestId)
# =============================================================================
class SlidingWindowLog(RateLimiter):
    def __init__(self, configRule: RateLimiterConfig):
        self.configRule = configRule
        self.capacity = self.configRule.maxAllowedRequests
        self.refill_time = self.configRule.refillTime
        self.logs: dict[str, collections.deque] = {}
        self.lock = threading.Lock()
    
    def allowrequests(self, requestId: str) -> bool:
        now = time.time()
        cutoff = now - self.refill_time
        with self.lock:
            if requestId not in self.logs:
                self.logs[requestId] = collections.deque([now])
                return True

            queue = self.logs[requestId]

            # Prune expired timestamps in O(1) per pop
            while queue and queue[0] <= cutoff:
                queue.popleft()
            
            if len(queue) < self.capacity:
                queue.append(now)
                return True 
            
            return False


# =============================================================================
# RateLimitManager ->
# - requestId
#     +allowrequests(requestId, userType: Type)
# =============================================================================
class RateLimitManager:
    """
    Facade class coordinating user tiers and routing requests to their 
    configured rate-limiting algorithm strategies.
    """
    def __init__(self):
        # Configuring distinct algorithms and rules per client tier
        self.limiters = {
            Type.BASIC: TokenBucketAlgorithm(
                RateLimiterConfig(maxAllowedRequests=5, refillTime=60)
            ),
            Type.PREMIUM: FixedWindow(
                RateLimiterConfig(maxAllowedRequests=50, refillTime=60)
            )
        }

    def allowrequests(self, requestId: str, userType: Type) -> bool:
        limiter = self.limiters.get(userType)
        if not limiter:
            raise ValueError(f"Unknown user type: {userType}")
            
        allowed = limiter.allowrequests(requestId)
        if allowed:
            print(f"Request allowed for [{userType.name}] client {requestId} using {limiter.__class__.__name__}")
        else:
            print(f"Rate limit exceeded for [{userType.name}] client {requestId} using {limiter.__class__.__name__}")
        return allowed
