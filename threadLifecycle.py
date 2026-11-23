import queue
import threading


class Solution:

    def someFunction(self, id: int) -> None:
        print("id = ", id)

    def orchestrator(self, num_workers: int = 4, total_ids: int = 16) -> None:
        if num_workers <= 0:
            raise ValueError("num_workers must be positive")
        if total_ids < 0:
            raise ValueError("total_ids must be non-negative")

        work_queue: queue.Queue[int | None] = queue.Queue()
        errors: list[tuple[int, BaseException]] = []
        errors_lock = threading.Lock()

        def worker() -> None:
            while True:
                item = work_queue.get()
                try:
                    if item is None:
                        return
                    self.someFunction(item)
                except BaseException as exc:
                    with errors_lock:
                        errors.append((item, exc))
                finally:
                    work_queue.task_done()

        threads = [
            threading.Thread(target=worker, name=f"id-worker-{idx}")
            for idx in range(num_workers)
        ]
        for t in threads:
            t.start()

        for i in range(total_ids):
            work_queue.put(i)

        for _ in threads:
            work_queue.put(None)

        work_queue.join()
        for t in threads:
            t.join()

        if errors:
            raise RuntimeError(f"Failed processing IDs: {[item for item, _ in errors]}") from errors[0][1]


if __name__ == "__main__":
    Solution().orchestrator()
