from typing import List, Tuple, Optional, Dict


class EncryptedBucket:
    def __init__(self, ciphertexts: List[int] = None):
        self.ciphertexts = ciphertexts or []

    def __repr__(self):
        return f"EncryptedBucket({len(self.ciphertexts)} ciphertexts)"


class CloudTree:
    def __init__(self, L: int):
        self.L = L
        self.levels = []
        for level in range(L + 1):
            self.levels.append([EncryptedBucket() for _ in range(2 ** level)])

    def update_node(self, level: int, index: int, bucket: EncryptedBucket):
        self.levels[level][index] = bucket

    def get_node(self, level: int, index: int) -> EncryptedBucket:
        return self.levels[level][index]

    def get_dummy_locations(self) -> List[Tuple[int, int]]:
        locations = []
        for level in range(self.L + 1):
            for idx, bucket in enumerate(self.levels[level]):
                if not bucket.ciphertexts:
                    locations.append((level, idx))
        return locations

    def get_all_locations(self) -> List[Tuple[int, int]]:
        locations = []
        for level in range(self.L + 1):
            for idx in range(2 ** level):
                locations.append((level, idx))
        return locations

    def __repr__(self):
        return "\n".join(f"Level {i}: {lvl}" for i, lvl in enumerate(self.levels))


class PositionMap:
    def __init__(self):
        self.map: Dict[str, Tuple[int, int]] = {}

    def update(self, key: str, location: Tuple[int, int]):
        self.map[key] = location

    def get(self, key: str) -> Optional[Tuple[int, int]]:
        return self.map.get(key)

    def remove(self, key: str):
        if key in self.map:
            del self.map[key]

    def __repr__(self):
        return str(self.map)


class Stash:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = []

    def add(self, key: str, value: bytes):
        if len(self.items) < self.capacity:
            self.items.append((key, value))

    def get(self, key: str) -> Optional[bytes]:
        for k, v in self.items:
            if k == key:
                return v
        return None

    def remove(self, key: str):
        self.items = [(k, v) for k, v in self.items if k != key]

    def __repr__(self):
        return str(self.items)