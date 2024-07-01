import pytest

from resource_lock import ResourceLock


@pytest.fixture
def resource_lock():
    rl = ResourceLock()
    rl.add_lock("a", 1500, 1600)
    rl.add_lock("a", 1800, 1900)
    rl.add_lock("b", 1700, 3000)
    rl.add_lock("a", 1550, 1650)  # Adding a collision for testing
    return rl


def test_find_first_collision(resource_lock):
    collision = resource_lock.find_first_collision("a")
    assert collision is not None
    assert collision == ((1500, 1600), (1550, 1650))


def test_is_locked(resource_lock):
    assert resource_lock.is_locked("a", 1550) is True
    assert resource_lock.is_locked("a", 1750) is False
    assert resource_lock.is_locked("b", 2000) is True
    assert resource_lock.is_locked("b", 3100) is False


def test_has_collision_at(resource_lock):
    assert resource_lock.has_collision_at("a", 1550) is True
    assert resource_lock.has_collision_at("a", 1750) is False
    assert resource_lock.has_collision_at("b", 2000) is False


def test_find_all_collisions(resource_lock):
    collisions = resource_lock.find_all_collisions("a")
    assert len(collisions) == 1
    assert collisions[0] == ((1500, 1600), (1550, 1650))
