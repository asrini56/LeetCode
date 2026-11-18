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

"""
CLASS BLUEPRINT:

1. Type (Enum)
   - Variables: BASIC, PREMIUM
   - Methods: None

2. RateLimiterConfig
   - Variables: maxAllowedRequests, refillTime
   - Methods: __init__()

3. RateLimiter (ABC)
   - Variables: None
   - Methods: allowrequests(requestId: str) -> bool

4. TokenBucketAlgorithm (inherits RateLimiter)
   - Variables: configRule, capacity, refill_time, _buckets, _lock
   - Methods: __init__(configRule), allowrequests(requestId: str) -> bool

5. FixedWindow (inherits RateLimiter)
   - Variables: configRule, max_requests, window_size, _windows, _lock
   - Methods: __init__(configRule), allowrequests(requestId: str) -> bool

6. SlidingWindowLog (inherits RateLimiter)
   - Variables: configRule, capacity, refill_time, logs, lock
   - Methods: __init__(configRule), allowrequests(requestId: str) -> bool

7. RateLimitManager
   - Variables: limiters
   - Methods: __init__(), allowrequests(requestId: str, userType: Type) -> bool
"""

from abc import ABC, abstractmethod
from enum import Enum
import threading
import time
import collections

class Type(Enum):
    BASIC = 1
    PREMIUM = 2


class RateLimiterConfig:
    """Encapsulates configuration rules for request thresholds and time windows."""
    def __init__(self, maxAllowedRequests: int, refillTime: int):
        self.maxAllowedRequests = maxAllowedRequests
        self.refillTime = refillTime


class RateLimiter(ABC):
    """Abstract base class strategy interface for rate-limiting algorithms."""
    @abstractmethod
    def allowrequests(self, requestId: str) -> bool:
        pass


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

            while queue and queue[0] <= cutoff:
                queue.popleft()
            
            if len(queue) < self.capacity:
                queue.append(now)
                return True 
            
            return False


class RateLimitManager:
    """
    Facade class coordinating user tiers and routing requests to their 
    configured rate-limiting algorithm strategies.
    """
    def __init__(self):
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
