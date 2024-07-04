from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class CollisionDetector(ABC):
    @abstractmethod
    def add_lock(self, resource_id: str, start_time: int, end_time: int):
        pass

    @abstractmethod
    def find_first_collision(self, resource_id: str) -> Optional[Tuple[int, int]]:
        pass

    @abstractmethod
    def is_locked(self, resource_id: str, t: int) -> bool:
        pass

    @abstractmethod
    def has_collision_at(self, resource_id: str, t: int) -> bool:
        pass

    @abstractmethod
    def find_all_collisions(self, resource_id: str) -> List[Tuple[int, int]]:
        pass
