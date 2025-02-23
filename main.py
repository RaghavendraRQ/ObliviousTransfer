from ObliviousTransfer.cloud import MobileCloudStorageSystem

# Initialize the cloud storage system with L=3, t=2, Z=2, and some initial items.
cloud = MobileCloudStorageSystem(3, 2, 2, [(1, "a"), (2, "b"), (3, "c")])

# Access the system: get the value for key 2.
print(cloud.access("get", 2))
print(cloud)

# Access the system: put a new value for key 2.
print(cloud.access("put", 2, "z"))
print(cloud)

# Access the system: remove the item with key 2.
print(cloud.access("remove", 2))
print(cloud)