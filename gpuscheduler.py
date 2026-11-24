import heapq


class Node:
    def __init__(self, node_id: str, gpu_count: int) -> None:
        if gpu_count <= 0:
            raise ValueError("GPU count must be positive")

        self.node_id = node_id
        self.total_gpus = gpu_count
        self.free_gpus: set[int] = set(range(gpu_count))
        self.healthy = True


class Job:
    def __init__(
        self, job_id: str, gpu_count: int, priority: int, preemptible: bool = True
    ) -> None:
        if not job_id:
            raise ValueError("Job ID cannot be empty")

        if gpu_count <= 0:
            raise ValueError("GPU count must be positive")

        self.job_id = job_id
        self.gpu_count = gpu_count
        self.priority = priority
        self.preemptible = preemptible
        self.allocation: dict[str, list[int]] = {}


class Scheduler:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.running: dict[str, Job] = {}
        self.pending: list[tuple[int, int, Job]] = []

        # Track every submitted job to prevent duplicates
        self.all_jobs: dict[str, Job] = {}

        self._seq = 0

    def add_node(self, node: Node) -> None:
        if node.node_id in self.nodes:
            raise ValueError("Duplicate node ID")

        self.nodes[node.node_id] = node

    def _free_gpu_count(self) -> int:
        return sum(
            len(n.free_gpus)
            for n in self.nodes.values()
            if n.healthy
        )

    def _healthy_gpu_count(self) -> int:
        return sum(
            n.total_gpus
            for n in self.nodes.values()
            if n.healthy
        )

    def _allocate(self, job: Job) -> bool:
        if self._free_gpu_count() < job.gpu_count:
            return False

        # Phase 1: Build allocation plan
        plan: dict[str, list[int]] = {}
        needed = job.gpu_count

        for node in self.nodes.values():
            if not node.healthy or not node.free_gpus:
                continue

            take = sorted(node.free_gpus)[:needed]

            if take:
                plan[node.node_id] = take
                needed -= len(take)

            if needed == 0:
                break

        if needed > 0:
            return False

        # Phase 2: Commit allocation
        for node_id, gpus in plan.items():
            self.nodes[node_id].free_gpus.difference_update(gpus)

        job.allocation = plan
        self.running[job.job_id] = job

        return True

    def _enqueue(self, job: Job) -> None:
        job.allocation = {}

        heapq.heappush(
            self.pending,
            (-job.priority, self._seq, job)
        )

        self._seq += 1

    def _release(self, job: Job) -> None:
        for node_id, gpus in job.allocation.items():
            node = self.nodes.get(node_id)

            if node and node.healthy:
                node.free_gpus.update(gpus)

        job.allocation = {}

    def submit(self, job: Job) -> bool:
        # Validate duplicate submission
        if job.job_id in self.all_jobs:
            raise ValueError("Duplicate job ID")

        # Reject requests larger than currently healthy cluster capacity
        if job.gpu_count > self._healthy_gpu_count():
            raise ValueError("Job exceeds healthy cluster capacity")

        self.all_jobs[job.job_id] = job

        if self._allocate(job):
            return True

        self._enqueue(job)
        return False

    def complete(self, job_id: str) -> None:
        job = self.running.pop(job_id, None)

        if not job:
            return

        self._release(job)
        self._drain_pending()

    def fail_node(self, node_id: str) -> None:
        node = self.nodes.get(node_id)

        if not node or not node.healthy:
            return

        node.healthy = False
        node.free_gpus.clear()

        affected = [
            j for j in self.running.values()
            if node_id in j.allocation
        ]

        for job in affected:
            self.running.pop(job.job_id, None)
            self._release(job)
            self._enqueue(job)

        self._drain_pending()

    def _drain_pending(self) -> None:
        requeue = []

        while self.pending:
            entry = heapq.heappop(self.pending)
            job = entry[2]

            if not self._allocate(job):
                requeue.append(entry)

        for entry in requeue:
            heapq.heappush(self.pending, entry)


# -------------------------------
# Example usage
# -------------------------------

scheduler = Scheduler()

scheduler.add_node(Node("N1", 4))
scheduler.add_node(Node("N2", 4))

job1 = Job("A", 4, priority=1)
job2 = Job("B", 4, priority=2)
job3 = Job("C", 2, priority=3)

print(scheduler.submit(job1))  # True
print(scheduler.submit(job2))  # True
print(scheduler.submit(job3))  # False (pending)

print("Running:", list(scheduler.running.keys()))

scheduler.complete("A")

print("Running:", list(scheduler.running.keys()))
print("Pending:", [x[2].job_id for x in scheduler.pending])

# -------------------------------
# PREEMPTION (INTERVIEW EXTENSION)
# -------------------------------
#
# Goal: Allow a higher-priority job to preempt lower-priority preemptible
# running jobs atomically so we never evict victims unless enough GPUs
# can actually be freed and allocated to the incoming job.
#
# Proposed helper on Scheduler:
#
# def _try_preempt_for(self, job: Job) -> bool:
#     # 1. Select candidate victims: currently running, preemptible,
#     #    and strictly lower priority than `job`.
#     candidates = sorted(
#         (
#             r for r in self.running.values()
#             if r.preemptible and r.priority < job.priority
#         ),
#         key=lambda r: (r.priority, r.job_id),
#     )
#
#     # 2. Check feasibility before mutating running state:
#     #    sum current free GPUs across healthy nodes + GPUs held by candidates.
#     reclaimable = sum(
#         len(gpus)
#         for victim in candidates
#         for node_id, gpus in victim.allocation.items()
#         if self.nodes.get(node_id) and self.nodes[node_id].healthy
#     )
#     if self._free_gpu_count() + reclaimable < job.gpu_count:
#         return False
#
#     # 3. Evict only enough victims to satisfy `job.gpu_count`:
#     victims_to_preempt: list[Job] = []
#     projected_free = self._free_gpu_count()
#     for victim in candidates:
#         if projected_free >= job.gpu_count:
#             break
#         victims_to_preempt.append(victim)
#         projected_free += sum(
#             len(gpus)
#             for node_id, gpus in victim.allocation.items()
#             if self.nodes.get(node_id) and self.nodes[node_id].healthy
#         )
#
#     # 4. Commit preemption: checkpoint/stop victims, release GPUs,
#     #    requeue preempted jobs, then allocate to `job`.
#     for victim in victims_to_preempt:
#         self.running.pop(victim.job_id, None)
#         self._release(victim)
#         self._enqueue(victim)
#
#     allocated = self._allocate(job)
#     if not allocated:
#         # Defensive fallback: if placement could not satisfy `job`,
#         # try draining pending so preempted jobs can resume if possible.
#         self._drain_pending()
#         return False
#     return True
#
# Integration in `submit(self, job: Job)`:
#     if self._allocate(job):
#         return True
#     if self._try_preempt_for(job):
#         return True
#     self._enqueue(job)
#     return False
