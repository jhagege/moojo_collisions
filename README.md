
# Resource Lock Library with FastAPI

This library is designed to detect collisions on shared resources. The library provides functionality to add lock intervals for resources and to check for collisions and lock status at given times. The API is documented and interactive using FastAPI.

## Features

- Add lock intervals for resources.
- Compute the first collision for a given resource.
- Determine if a resource is locked at a specific time.
- Check if a resource has a collision at a specific time.
- Find all collisions for a given resource.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/jhagege/moojo_collisions
cd moojo_collisions
```

2. Build the Docker image:

```sh
docker build -t resource-lock-api .
```

## Usage

1. Run the Docker container:

```sh
docker run -it --rm -p 8080:8080 resource-lock-api
```

2. Access the API documentation:

- Swagger UI: [http://localhost:8080/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8080/redoc](http://localhost:8000/redoc)

3. Access the online version deployed with ci/cd: 
- Swagger UI: [https://my-app-yftkbunxyq-uc.a.run.app/docs](https://my-app-yftkbunxyq-uc.a.run.app/docs)
- Redoc: [https://my-app-yftkbunxyq-uc.a.run.app/redoc](https://my-app-yftkbunxyq-uc.a.run.app/redoc)

## API

### `ResourceLock` Class

#### Methods

- `add_lock(resource_id: str, start_time: int, end_time: int)`

  Adds a lock interval for the specified resource.

- `find_first_collision(resource_id: str) -> Optional[Tuple[int, int]]`

  Computes the first collision for the given resource. Returns a tuple of the colliding intervals or `None` if no collision is found.

- `is_locked(resource_id: str, t: int) -> bool`

  Determines if the specified resource is locked at time `t`.

- `has_collision_at(resource_id: str, t: int) -> bool`

  Checks if the specified resource has a collision at time `t`.

- `find_all_collisions(resource_id: str) -> List[Tuple[int, int]]`

  Finds all collisions for the given resource. Returns a list of tuples of the colliding intervals.

## Examples

### Adding Locks

```python
rl = ResourceLock()
rl.add_lock("a", 1500, 1600)
rl.add_lock("a", 1800, 1900)
rl.add_lock("b", 1700, 3000)
rl.add_lock("a", 1550, 1650)  # Adding a collision for testing
```

### Finding the First Collision

```python
collision = rl.find_first_collision("a")
print(collision)  # Output: ((1500, 1600), (1550, 1650))
```

### Checking Lock Status

```python
is_locked = rl.is_locked("a", 1550)
print(is_locked)  # Output: True
```

### Checking for Collisions

```python
has_collision = rl.has_collision_at("a", 1550)
print(has_collision)  # Output: True
```

### Finding All Collisions

```python
collisions = rl.find_all_collisions("a")
print(collisions)  # Output: [((1500, 1600), (1550, 1650))]
```

## Running Tests

The tests are written using the `pytest` framework. To run the tests, use the following command:

```sh
docker run --rm resource-lock-api pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## Author

Joachim Hagege