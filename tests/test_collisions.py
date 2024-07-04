import pytest

from collision_detector.time_interval_collision_detector import IntervalConflictDetector


@pytest.fixture
def collision_detector():
    rl = IntervalConflictDetector()
    rl.add_lock("a", 1500, 1600)
    rl.add_lock("a", 1800, 1900)
    rl.add_lock("b", 1700, 3000)
    rl.add_lock("a", 1550, 1650)  # Adding a collision for testing
    return rl


def test_find_first_collision(collision_detector):
    collision = collision_detector.find_first_collision("a")
    assert collision is not None
    assert collision == ((1500, 1600), (1550, 1650))


def test_is_locked(collision_detector):
    assert collision_detector.is_locked("a", 1550) is True
    assert collision_detector.is_locked("a", 1750) is False
    assert collision_detector.is_locked("b", 2000) is True
    assert collision_detector.is_locked("b", 3100) is False


def test_has_collision_at(collision_detector):
    assert collision_detector.has_collision_at("a", 1550) is True
    assert collision_detector.has_collision_at("a", 1750) is False
    assert collision_detector.has_collision_at("b", 2000) is False


def test_find_all_collisions(collision_detector):
    collisions = collision_detector.find_all_collisions("a")
    assert len(collisions) == 1
    assert collisions[0] == ((1500, 1600), (1550, 1650))
