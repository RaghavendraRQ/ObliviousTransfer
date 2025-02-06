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
position_map = {}

# Stash is a temporary storage location for the items that are not updated into the cloud storage system
class Stash:
    def __init__(self):
        self.stash = []

    def push(self, key, value):
        ptr = 0
        for j in range(config.Z):
            if self.stash[1][j] is None:
                ptr = j

        if ptr == 0:
            return None
        self.stash[1][ptr] = (key, value)
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

    def pop(self, key):
        for i in range(0, config.T, -1):
            pass

