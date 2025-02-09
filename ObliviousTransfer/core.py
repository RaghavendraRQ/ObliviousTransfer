# Binary Tree Implementation in Cloud Side

import ObliviousTransfer.constants as config

class Bucket:
    def __init__(self, chucks):
        self.chucks = chucks
        self.bucket = []
        self.bucket.append(chucks)

class CloudTree:
    def __init__(self, chucks):
        self.root = Bucket(chucks)
        self.current = self.root
        self.buckets = []

    def add(self, chucks):
        self.current.bucket.append(chucks)
        self.current = chucks

    def next(self):
        self.current = self.current.bucket[0]
        return self.current.chucks

    def prev(self):
        self.current = self.current.bucket[1]
        return self.current.chucks

    def reset(self):
        self.current = self.root
        return self.current.chucks

    def get(self):
        return self.current.chucks

    def get_root(self):
        return self.root

    def get_current(self):
        return self.current


# Position Map dictionary and maps the mobile cloud storage system from logical key of item to physical storage location
# For a key k of an item, the position map pm[k] returns a location tuple (l,p) indicated that the item may be located at the P(l,p) node of T
class PositionMap:
    def __init__(self):
        self.pm = {}

    def add(self, key, location):
        self.pm[key] = location

    def get(self, key):
        return self.pm[key]

    def remove(self, key):
        self.pm.pop(key)

# Stash is a temporary storage location for the items that are not updated into the cloud storage system
class Stash:

    class Item:
        def __init__(self, key, value):
            self.k = key
            self.v = value

        def __repr__(self):
            return f"({self.k}, {self.v})"

    def __init__(self):
        # Initialize the stash as a T x Z matrix with dummy item tuples
        self.stash = [[Stash.Item(None, None) for j in range(config.Z)] for i in range(config.T)]   # T x Z matrix

    def _random_and_uniform(self, lst):
        pass

    def push(self, key, value):
        ptr = 0
        for j in range(config.Z):
            if self.stash[1][j].k is None or self.stash[1][j].v is None:
                ptr = j

        if ptr == 0:
            return None
        self.stash[1][ptr] = Stash.Item(key, value)
        return 0

    def update(self, key, value):
        for i in range(1, config.T):
            for j in range(config.Z):
                if self.stash[i][j].k == key:
                    self.stash[i][j].v = value
                    return 0
        return None

    def get(self, key):
        for i in range(config.T):
            for j in range(config.Z):
                if self.stash[i][j].k == key:
                    return self.stash[i][j].v
        return None

    def pop(self):
        ptr = list(range(1, config.Z + 1)) # [1, Z]
        for i in range(0, config.T, -1):
            ptr[i] = 0
            if i == config.T:
                return self.stash[i][ptr[i]]
            else:
                self.stash[i + 1][ptr[i + 1]] = self.stash[i][ptr[i]]

            if i == 1:
                self.stash[i][ptr[i]] = Stash.Item(None, None)
            return None