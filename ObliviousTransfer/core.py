
class Bucket:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
    def __repr__(self):
        return f"({self.key}, {self.value})"

class CloudTree:
    def __init__(self, L):
        self.L = L
        self.levels = []
        for level in range(L + 1):
            self.levels.append([Bucket() for _ in range(2 ** level)])

    def update_node(self, level, index, bucket):
        self.levels[level][index] = bucket

    def get_node(self, level, index):
        return self.levels[level][index]

    def get_dummy_locations(self):
        """Return a list of (level, index) for all buckets that are currently dummy."""
        locations = []
        for level in range(self.L + 1):
            for index, bucket in enumerate(self.levels[level]):
                if bucket.key is None:
                    locations.append((level, index))
        return locations

    def get_all_locations(self):
        """Return a list of all possible (level, index) pairs in the tree."""
        locations = []
        for level in range(self.L + 1):
            for index in range(2 ** level):
                locations.append((level, index))
        return locations

    def __repr__(self):
        s = ""
        for level, buckets in enumerate(self.levels):
            s += f"Level {level}: " + str(buckets) + "\n"
        return s


class PositionMap:
    def __init__(self):
        self.map = {}  # key -> (level, index)
    def update(self, key, location):
        self.map[key] = location
    def get(self, key):
        return self.map.get(key, None)
    def remove(self, key):
        if key in self.map:
            del self.map[key]
    def __repr__(self):
        return str(self.map)


class Stash:
    class Item:
        def __init__(self, key=None, value=None):
            self.k = key
            self.v = value
        def __repr__(self):
            return f"({self.k}, {self.v})"

    def __init__(self, t, Z):
        self.t = t  # Number of rows
        self.Z = Z  # Number of columns in each row
        self.matrix = [[Stash.Item() for _ in range(Z)] for _ in range(t)]

    def push(self, key, value):
        """Push a new (key, value) into the bottom row (row index t-1) into the first free slot."""
        row = self.t - 1
        for j in range(self.Z):
            if self.matrix[row][j].k is None:
                self.matrix[row][j] = Stash.Item(key, value)
                return 0
        return None

    def update(self, key, value):
        """Update an item with the given key in the stash."""
        for i in range(self.t):
            for j in range(self.Z):
                if self.matrix[i][j].k == key:
                    self.matrix[i][j].v = value
                    return 0
        return None

    def get(self, key):
        """Return the value associated with key in the stash (if any)."""
        for i in range(self.t):
            for j in range(self.Z):
                if self.matrix[i][j].k == key:
                    return self.matrix[i][j].v
        return None

    def pop(self):
        """
        Remove and return one item from the stash.
        First, try to remove an item from the top row.
        If the top row is empty, shift all rows upward and try again.
        """
        for j in range(self.Z):
            if self.matrix[0][j].k is not None:
                item = self.matrix[0][j]
                self.matrix[0][j] = Stash.Item()
                return item
        for i in range(1, self.t):
            for j in range(self.Z):
                self.matrix[i - 1][j] = self.matrix[i][j]
                self.matrix[i][j] = Stash.Item()
        for j in range(self.Z):
            if self.matrix[0][j].k is not None:
                item = self.matrix[0][j]
                self.matrix[0][j] = Stash.Item()
                return item
        return None

    def __repr__(self):
        s = ""
        for row in self.matrix:
            s += str(row) + "\n"
        return s
