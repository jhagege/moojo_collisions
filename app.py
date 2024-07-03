from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from resource_lock import ResourceLock


class Lock(BaseModel):
    resource_id: str
    start_time: int
    end_time: int


class ResourceLockAPI:
    def __init__(self):
        self.app = FastAPI()
        self.resource_lock = ResourceLock()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/add_lock")
        def add_lock(lock: Lock, resource_lock: ResourceLock = Depends(self.get_resource_lock)):
            resource_lock.add_lock(lock.resource_id, lock.start_time, lock.end_time)
            return {"message": "Lock added successfully"}

        @self.app.get("/first_collision/{resource_id}")
        def first_collision(resource_id: str, resource_lock: ResourceLock = Depends(self.get_resource_lock)):
            collision = resource_lock.find_first_collision(resource_id)
            if collision:
                return {"collision": collision}
            raise HTTPException(status_code=404, detail="No collision")

        @self.app.get("/is_locked")
        def is_locked(resource_id: str, t: int, resource_lock: ResourceLock = Depends(self.get_resource_lock)):
            locked = resource_lock.is_locked(resource_id, t)
            return {"is_locked": locked}

        @self.app.get("/has_collision")
        def has_collision(resource_id: str, t: int, resource_lock: ResourceLock = Depends(self.get_resource_lock)):
            collision = resource_lock.has_collision_at(resource_id, t)
            return {"has_collision": collision}

        @self.app.get("/all_collisions/{resource_id}")
        def all_collisions(resource_id: str, resource_lock: ResourceLock = Depends(self.get_resource_lock)):
            collisions = resource_lock.find_all_collisions(resource_id)
            return {"collisions": collisions}

    def get_resource_lock(self):
        return self.resource_lock


# Create an instance of the ResourceLockAPI
resource_lock_api = ResourceLockAPI()

# Expose the FastAPI app instance
app = resource_lock_api.app
