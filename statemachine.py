import threading


class TaskStateMachine:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tasks: dict[str, dict] = {}

    def on_complete(self, task_id: str, attempt: int) -> None:
        """Override in a subclass to handle task completion side effects."""
        pass

    def on_bill(self, task_id: str, amount: float) -> None:
        """Override in a subclass to handle billing side effects."""
        pass

    def _get_or_create(self, task_id: str, attempt: int) -> dict:
        rec = self._tasks.get(task_id)
        if rec is None:
            rec = {
                "state": "PENDING",
                "attempt": attempt,
                "executed": False,
                "billed": False,
                "seen_events": set(),
            }
            self._tasks[task_id] = rec
        return rec

    def start_attempt(self, task_id: str) -> int:
        with self._lock:
            rec = self._get_or_create(task_id, attempt=1)
            if rec["state"] != "COMPLETED":
                rec["attempt"] += 1
                rec["state"] = "PENDING"
            return rec["attempt"]

    def handle_event(
        self,
        event_id: str,
        task_id: str,
        attempt: int,
        status: str,
        amount: float = 0.0,
    ) -> bool:
        if not event_id or not task_id or attempt < 1:
            raise ValueError("Invalid event parameters")

        run_complete = False
        run_bill = False
        result = False

        with self._lock:
            rec = self._get_or_create(task_id, attempt)

            # 1. Duplicate event retry
            if event_id in rec["seen_events"]:
                return False
            rec["seen_events"].add(event_id)

            # 2. Stale event from an older worker attempt
            if attempt < rec["attempt"]:
                return False

            # 3. Newer attempt arrived
            if attempt > rec["attempt"]:
                if rec["state"] == "COMPLETED":
                    return False
                rec["attempt"] = attempt
                rec["state"] = "PENDING"

            # 4. Already terminal
            if rec["state"] == "COMPLETED":
                return False

            if status == "STARTED":
                if rec["state"] == "PENDING":
                    rec["state"] = "RUNNING"
                result = True
            elif status == "FAILED":
                rec["state"] = "FAILED"
                result = True
            elif status == "COMPLETED":
                rec["state"] = "COMPLETED"
                if not rec["executed"]:
                    rec["executed"] = True
                    run_complete = True
                if not rec["billed"]:
                    rec["billed"] = True
                    run_bill = True
                result = True
            else:
                raise ValueError(f"Unknown status: {status}")

        # Runs after `with self._lock:` exits so the lock is already released.
        if run_complete:
            self.on_complete(task_id, attempt)
        if run_bill:
            self.on_bill(task_id, amount)

        return result


if __name__ == "__main__":
    done = []
    billed = []

    class RecordingTaskStateMachine(TaskStateMachine):
        def on_complete(self, task_id: str, attempt: int) -> None:
            done.append((task_id, attempt))

        def on_bill(self, task_id: str, amount: float) -> None:
            billed.append((task_id, amount))

    sm = RecordingTaskStateMachine()

    sm.handle_event("ev-1", "t1", 1, "COMPLETED", 5.0)
    sm.handle_event("ev-2", "t1", 1, "STARTED", 5.0)     # Late out-of-order start
    sm.handle_event("ev-1", "t1", 1, "COMPLETED", 5.0)   # Duplicate retry

    sm.handle_event("ev-3", "t2", 1, "FAILED", 2.0)
    sm.start_attempt("t2")                                # Now attempt 2
    sm.handle_event("ev-4", "t2", 1, "COMPLETED", 2.0)   # Stale attempt 1
    sm.handle_event("ev-5", "t2", 2, "COMPLETED", 4.0)   # Valid attempt 2

    print("Completed:", done)   # [('t1', 1), ('t2', 2)]
    print("Billed:", billed)     # [('t1', 5.0), ('t2', 4.0)]
