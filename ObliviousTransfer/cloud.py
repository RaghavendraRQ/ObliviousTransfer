from ObliviousTransfer.core import Stash, PositionMap, CloudTree
from damgard_jurik.crypto import keygen

def init_cloud(set_size):
    s = 5
    public_key, private_key = keygen(s=s)
    position_map = PositionMap()
    stash = Stash()
    cloud_tree = CloudTree(None)

    for i in range(1, set_size + 1):
        pass

    for bucket in cloud_tree.buckets:
        if bucket is None:
            bucket = ()
        c = public_key.encrypt(bucket)
        for j in range(1, c):
            pass

