from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collision_detector.time_interval_collision_detector import CollisionDetector, IntervalConflictDetector


class Lock(BaseModel):
    resource_id: str
    start_time: int
    end_time: int


class CollisionDetectorAPI:
    def __init__(self, resource_lock: CollisionDetector = IntervalConflictDetector()):
        self.app = FastAPI()
        self.resource_lock = resource_lock
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/add_lock")
        def add_lock(lock: Lock):
            self.resource_lock.add_lock(lock.resource_id, lock.start_time, lock.end_time)
            return {"message": "Lock added successfully"}

        @self.app.get("/first_collision/{resource_id}")
        def first_collision(resource_id: str):
            collision = self.resource_lock.find_first_collision(resource_id)
            if collision:
                return {"collision": collision}
            raise HTTPException(status_code=404, detail="No collision")

        @self.app.get("/is_locked")
        def is_locked(resource_id: str, t: int):
            locked = self.resource_lock.is_locked(resource_id, t)
            return {"is_locked": locked}

        @self.app.get("/has_collision")
        def has_collision(resource_id: str, t: int):
            collision = self.resource_lock.has_collision_at(resource_id, t)
            return {"has_collision": collision}

        @self.app.get("/all_collisions/{resource_id}")
        def all_collisions(resource_id: str):
            collisions = self.resource_lock.find_all_collisions(resource_id)
            return {"collisions": collisions}


# Instantiate the ResourceLock and pass it to ResourceLockAPI
# Enables dependency injection, potentially mocking for testing etc.
collision_detector = IntervalConflictDetector()
resource_lock_api = CollisionDetectorAPI(collision_detector)

# Expose the FastAPI app instance
app = resource_lock_api.app
