from ObliviousTransfer.cloud import MobileCloudStorageSystem

from client import Client

cloud = MobileCloudStorageSystem(3, 2, 2, [(1, "a"), (2, "b"), (3, "c")])

client = Client(initial_items=[(1, "a"), (2, "b"), (3, "c")])


### Three methods: get, put, remove

print(cloud.access("get", 2))
print(cloud)

print(cloud.access("put", 2, "z"))
print(cloud)

print(cloud.access("remove", 2))
print(cloud)