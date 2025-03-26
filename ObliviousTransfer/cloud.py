from ObliviousTransfer.core import Stash, PositionMap, CloudTree, Bucket
from ObliviousTransfer.constants import Config
import damgard_jurik.crypto as damgard_jurik
import random



class MobileCloudStorageSystem:
    def __init__(self, L, t, Z, items):
        """
        L: Tree height (tree has L+1 levels).
        t: Number of stash rows; Z: number of stash columns.
        items: initial list of (key, value) tuples.
        """
        self.config = Config(L, t, Z, temp_window=3)
        self.L = L

        self.public_key, self.private_key = damgard_jurik.keygen(1024)

        self.tree = CloudTree(L)
        self.stash = Stash(t, Z)
        self.pm = PositionMap()

        # Run the initialization algorithm.
        self.init_system(items)

    def init_system(self, items):
        """
        Initialization:
          For each (key, value) in items, assign it to a unique bucket
          in the tree (from the set of all nodes) and update the position map.
        """
        possible_locations = self.tree.get_all_locations()  # All (level, index) pairs.
        random.shuffle(possible_locations)
        for (key, value) in items:
            if not possible_locations:
                raise Exception("Not enough tree nodes to store all items!")
            loc = possible_locations.pop()
            self.pm.update(key, loc)
            self.tree.update_node(loc[0], loc[1], Bucket(key, value))

    def access(self, op, key, v_new=None):
        """
        Access protocol (simplified simulation of OSU):
          - op: 'get', 'put', or 'remove'
          - key: key to operate on
          - v_new: for 'put', the new value

        Steps:
          1. If the item is not in the stash, use the position map to fetch it from the tree.
             (If found, push it into the stash and mark the tree bucket as dummy.)
          2. Record the original value.
          3. For 'put', update the value; for 'remove', set value to None and remove from pm.
          4. Pop an item from the stash and write it back into a randomly chosen dummy bucket in the tree.
             Update the position map accordingly.
          5. Return the original value.
        """
        stash_val = self.stash.get(key)
        if stash_val is not None:
            current_item = (key, stash_val)
        else:
            location = self.pm.get(key)
            if location is None:
                if op == 'put':
                    current_item = (key, None)
                else:
                    return None
            else:
                level, index = location
                bucket = self.tree.get_node(level, index)
                current_item = (bucket.key, bucket.value)
                self.stash.push(bucket.key, bucket.value)
                self.tree.update_node(level, index, Bucket())
        orig_value = current_item[1]

        if op == 'put':
            self.stash.update(key, v_new)
            current_item = (key, v_new)
        elif op == 'remove':
            self.stash.update(key, None)
            self.pm.remove(key)
            current_item = (key, None)

        popped = self.stash.pop()
        if popped is not None and popped.k is not None:
            dummies = self.tree.get_dummy_locations()
            if dummies:
                new_loc = random.choice(dummies)
            else:
                new_loc = random.choice(self.tree.get_all_locations())
            self.tree.update_node(new_loc[0], new_loc[1], Bucket(popped.k, popped.v))
            self.pm.update(popped.k, new_loc)
        return orig_value

    def __repr__(self):
        s = "===== Binary Tree =====\n" + str(self.tree)
        s += "\n===== Stash =====\n" + str(self.stash)
        s += "\n===== Position Map =====\n" + str(self.pm)
        return s
