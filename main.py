from ObliviousTransfer.cloud import MobileCloudStorageSystem

cloud = MobileCloudStorageSystem(3, 2, 2, [(1, "a"), (2, "b"), (3, "c")])

print(cloud.access("get", 2))
print(cloud)

print(cloud.access("put", 2, "z"))
print(cloud)

print(cloud.access("remove", 2))
print(cloud)