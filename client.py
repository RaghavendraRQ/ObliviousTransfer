from ObliviousTransfer.core import Stash, PositionMap
from ObliviousTransfer.constants import Config
import damgard_jurik.crypto as damgard_jurik
from ObliviousTransfer.cloud import MobileCloudStorageSystem


class Client:
    def __init__(self, L=3, t=2, Z=3, initial_items=None):
        """
        Initialize the client with:
        - L: Tree height
        - t: Stash rows
        - Z: Stash columns
        - initial_items: List of (key, value) tuples
        """
        if initial_items is None:
            initial_items = []

        self.mcs = MobileCloudStorageSystem(L, t, Z, initial_items)
        self.access_counter = {}  # For temporal locality tracking

    def request(self, op, key, value=None):
        """
        Handle client requests with temporal locality optimization
        op: 'get', 'put', or 'remove'
        key: Key to operate on
        value: New value for 'put' operations
        """
        # Check temporal locality first
        if key in self.access_counter and self.access_counter[key] > 0:
            self.access_counter[key] -= 1
            stash_val = self.mcs.stash.get(key)
            if stash_val is not None:
                if op == 'get':
                    return stash_val
                elif op == 'put':
                    self.mcs.stash.update(key, value)
                    return stash_val
                elif op == 'remove':
                    self.mcs.stash.update(key, None)
                    self.mcs.pm.remove(key)
                    return stash_val

        # If not in stash or counter expired, proceed with normal access
        result = self.mcs.access(op, key, value)

        # Update access counter for temporal locality
        if op != 'remove' and result is not None:
            self.access_counter[key] = Config.TEMPORAL_LOCALITY_WINDOW

        return result

    def get_public_key(self):
        """Get the client's public key for the cloud"""
        return self.mcs.public_key

    def get_tree_state(self):
        """Get the current tree state (for cloud synchronization)"""
        return self.mcs.tree

    def verify_integrity(self, cloud_tree):
        """
        Verify integrity using verification chunks
        Returns True if verification passes, False otherwise
        """
        # Compare verification chunks for all buckets
        for level in range(self.mcs.L + 1):
            for index in range(2 ** level):
                local_bucket = self.mcs.tree.get_node(level, index)
                cloud_bucket = cloud_tree.get_node(level, index)

                if local_bucket.verification_chunk != cloud_bucket.verification_chunk:
                    return False
        return True