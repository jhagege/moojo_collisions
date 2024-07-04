from typing import List, Tuple, Dict, Optional

import bisect

from collision_detector.interface import CollisionDetector


class IntervalConflictDetector(CollisionDetector):
    def __init__(self):
        self.locks: Dict[str, List[Tuple[int, int]]] = {}

    def add_lock(self, resource_id: str, start_time: int, end_time: int):
        if resource_id not in self.locks:
            self.locks[resource_id] = [(start_time, end_time)]
        else:
            intervals = self.locks[resource_id]
            i = bisect.bisect_left(intervals, (start_time, end_time))
            intervals.insert(i, (start_time, end_time))

    def find_first_collision(self, resource_id: str) -> Optional[Tuple[int, int]]:
        intervals = self.locks.get(resource_id, [])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return intervals[i - 1], intervals[i]
        return None

    def is_locked(self, resource_id: str, t: int) -> bool:
        intervals = self.locks.get(resource_id, [])
        i = bisect.bisect_right(intervals, (t, float('inf'))) - 1
        if i >= 0 and intervals[i][0] <= t < intervals[i][1]:
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
