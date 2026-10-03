import heapq
import sys
from typing import List, Tuple, Dict, Any, Optional

class Job:
    def __init__(self, arrival_time: int, job_id: str, priority: int, duration: int, resources: int, arrival_order: int):
        self.arrival_time = arrival_time
        self.job_id = job_id
        self.priority = priority
        self.duration = duration
        self.resources = resources
        self.arrival_order = arrival_order

        self.start_time: Optional[int] = None
        self.finish_time: Optional[int] = None
        self.assigned_worker: Optional[str] = None

    def __lt__(self, other: 'Job') -> bool:
        if self.priority != other.priority:
            return self.priority > other.priority
        if self.arrival_time != other.arrival_time:
            return self.arrival_time < other.arrival_time
        return self.arrival_order < other.arrival_order

class JobSchedulerSimulation:
    def __init__(self, num_workers: int, jobs: List[Job]):
        self.num_workers = num_workers
        self.jobs = sorted(jobs, key=lambda j: (j.arrival_time, j.arrival_order))
        self.worker_ids = [f"W{i+1}" for i in range(num_workers)]

    def run_simulation(self) -> Tuple[List[Job], float]:
        current_time = 0
        ready_queue: List[Job] = []
        
        free_workers: List[int] = list(range(1, self.num_workers + 1))
        heapq.heapify(free_workers)

        running_events: List[Tuple[int, int, Job]] = []

        unprocessed_jobs_idx = 0
        n_jobs = len(self.jobs)
        completed_jobs: List[Job] = []

        total_wait_time = 0

        while len(completed_jobs) < n_jobs:
            next_time_events = []
            if unprocessed_jobs_idx < n_jobs:
                next_time_events.append(self.jobs[unprocessed_jobs_idx].arrival_time)
            if running_events:
                next_time_events.append(running_events[0][0])

            if not next_time_events:
                break
                
            current_time = min(next_time_events)

            while running_events and running_events[0][0] == current_time:
                f_time, w_idx, finished_job = heapq.heappop(running_events)
                completed_jobs.append(finished_job)
                heapq.heappush(free_workers, w_idx)

            while unprocessed_jobs_idx < n_jobs and self.jobs[unprocessed_jobs_idx].arrival_time <= current_time:
                new_job = self.jobs[unprocessed_jobs_idx]
                heapq.heappush(ready_queue, new_job)
                unprocessed_jobs_idx += 1

            while ready_queue and free_workers:
                job = heapq.heappop(ready_queue)
                worker_idx = heapq.heappop(free_workers)
                
                job.assigned_worker = f"W{worker_idx}"
                job.start_time = current_time
                job.finish_time = current_time + job.duration
                
                wait_time = job.start_time - job.arrival_time
                total_wait_time += wait_time

                heapq.heappush(running_events, (job.finish_time, worker_idx, job))

        avg_wait_time = total_wait_time / n_jobs if n_jobs > 0 else 0.0
        return completed_jobs, avg_wait_time

if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if lines:
        first = lines[0].split()
        w, n = int(first[0]), int(first[1])
        jobs = []
        for i in range(1, 1 + n):
            parts = lines[i].split()
            if len(parts) >= 5:
                arr_t = int(parts[0])
                j_id = parts[1]
                prio = int(parts[2])
                dur = int(parts[3])
                res = int(parts[4])
                jobs.append(Job(arr_t, j_id, prio, dur, res, i - 1))
        scheduler = JobSchedulerSimulation(num_workers=w, jobs=jobs)
        completed, avg_wait = scheduler.run_simulation()
        completed.sort(key=lambda j: j.start_time)
        for job in completed:
            print(f"{job.job_id} {job.assigned_worker} {job.start_time} {job.finish_time}")
        print(f"AVG_WAIT {avg_wait:.2f}")
