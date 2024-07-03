from typing import List, Tuple, Dict, Optional


class ResourceLock:
    def __init__(self):
        self.locks: Dict[str, List[Tuple[int, int]]] = {}

    def add_lock(self, resource_id: str, start_time: int, end_time: int):
        if resource_id not in self.locks:
            self.locks[resource_id] = [(start_time, end_time)]
            return

        intervals = self.locks[resource_id]
        # Find the correct position to insert the new interval to keep the list sorted
        i = 0
        while i < len(intervals) and intervals[i][0] < start_time:
            i += 1
        intervals.insert(i, (start_time, end_time))

    def find_first_collision(self, resource_id: str) -> Optional[Tuple[int, int]]:
        intervals = self.locks.get(resource_id, [])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return intervals[i - 1], intervals[i]
        return None

    def is_locked(self, resource_id: str, t: int) -> bool:
        intervals = self.locks.get(resource_id, [])
        for start, end in intervals:
            if start <= t < end:
                return True
        return False

    def has_collision_at(self, resource_id: str, t: int) -> bool:
        intervals = self.locks.get(resource_id, [])
        active_intervals = [interval for interval in intervals if interval[0] <= t < interval[1]]
        return len(active_intervals) > 1

    def find_all_collisions(self, resource_id: str) -> List[Tuple[int, int]]:
        intervals = self.locks.get(resource_id, [])
        collisions = []
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                collisions.append((intervals[i - 1], intervals[i]))
        return collisions
