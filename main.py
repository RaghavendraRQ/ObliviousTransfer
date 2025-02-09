from ObliviousTransfer.core import Stash

stash = Stash()

stash.push(2, 3)
print(stash.stash[1][4])