from damgard_jurik.crypto import PublicKey, EncryptedNumber, keygen
import random
from typing import List, Tuple, Optional
from ObliviousTransfer.core import Stash, PositionMap


class CloudTree:
    def __init__(self, L: int):
        self.L = L
        self.levels = []
        for level in range(L + 1):
            self.levels.append([[] for _ in range(2 ** level)])

    def update_node(self, level: int, index: int, bucket: List[EncryptedNumber]):
        self.levels[level][index] = bucket

    def get_node(self, level: int, index: int) -> List[EncryptedNumber]:
        return self.levels[level][index]

    def get_all_locations(self) -> List[Tuple[int, int]]:
        locations = []
        for level in range(self.L + 1):
            for idx in range(2 ** level):
                locations.append((level, idx))
        return locations

    def get_dummy_locations(self) -> List[Tuple[int, int]]:
        return [(lvl, idx) for lvl in range(len(self.levels))
                for idx, bucket in enumerate(self.levels[lvl])
                if not bucket]  # Check for empty list instead of None


class MobileCloudClient:
    def __init__(self, L: int, s: int = 1, n_bits: int = 1024):
        self.L = L
        self.s = s
        self.public_key, self.private_key_ring = keygen(
            n_bits=n_bits,
            s=s,
            threshold=3,
            n_shares=3
        )
        self.tree = CloudTree(L)
        self.position_map = PositionMap()
        self.stash: Stash = Stash(100)

    def _bytes_to_int(self, data: bytes) -> List[int]:
        chunk_size = (self.public_key.n.bit_length() // 8) - 1
        return [int.from_bytes(data[i:i + chunk_size], 'big')
                for i in range(0, len(data), chunk_size)]

    def _int_to_bytes(self, integers: List[int]) -> bytes:
        chunk_size = (self.public_key.n.bit_length() // 8) - 1
        return b''.join(num.to_bytes(chunk_size, 'big') for num in integers)

    def _encrypt_bucket(self, data: bytes) -> List[EncryptedNumber]:
        chunks = self._bytes_to_int(data)
        return self.public_key.encrypt_list(chunks)

    def _decrypt_bucket(self, bucket: List[EncryptedNumber]) -> bytes:
        decrypted = self.private_key_ring.decrypt_list(bucket)
        return self._int_to_bytes(decrypted)

    def initialize(self, items: List[Tuple[str, bytes]]):
        locs = self.tree.get_all_locations()
        random.shuffle(locs)

        for key, value in items:
            if not locs:
                raise RuntimeError("Not enough buckets for initialization")
            level, idx = locs.pop()
            encrypted = self._encrypt_bucket(value)
            self.tree.update_node(level, idx, encrypted)
            self.position_map.update(key, (level, idx))

        for level, idx in locs:
            self.tree.update_node(level, idx, [])

    def _oblivious_access(self, op: str, key: str, value: Optional[bytes] = None) -> Optional[bytes]:
        orig_loc = self.position_map.get(key)
        new_loc = random.choice(self.tree.get_dummy_locations())

        if orig_loc:
            encrypted = self.tree.get_node(*orig_loc)
            decrypted = self._decrypt_bucket(encrypted)

            if op == 'put':
                decrypted = self._bytes_to_int(value)
                re_encrypted = self.public_key.encrypt_list(decrypted)
                self.tree.update_node(new_loc[0], new_loc[1], re_encrypted)
                self.position_map.update(key, new_loc)
            elif op == 'remove':
                decrypted = []
                self.position_map.remove(key)
                self.tree.update_node(orig_loc[0], orig_loc[1], decrypted)

            if op == 'get':
                return self._int_to_bytes(decrypted)
        else:
            if op == 'put':
                encrypted = self._encrypt_bucket(value)
                self.tree.update_node(new_loc[0], new_loc[1], encrypted)
                self.position_map.update(key, new_loc)

        return None

    def get(self, key: str) -> Optional[bytes]:
        return self._oblivious_access('get', key)

    def put(self, key: str, value: bytes):
        self._oblivious_access('put', key, value)

    def remove(self, key: str):
        self._oblivious_access('remove', key)


class CloudStorageServer:
    def __init__(self):
        self.tree: Optional[CloudTree] = None
        self.public_key: Optional[PublicKey] = None

    def store_tree(self, tree: CloudTree, public_key: PublicKey):
        self.tree = tree
        self.public_key = public_key

    def get_encrypted_path(self, level: int) -> List[List[EncryptedNumber]]:
        if not self.tree or level >= len(self.tree.levels):
            return []
        return self.tree.levels[level]