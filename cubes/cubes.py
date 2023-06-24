import numpy as np
import itertools as it
from numpy import rot90, array

n = 3
# represents how many cubes can fit inside. 0 represents all of one color
# +1 represents all of other color
n_size = np.power(n, 3) + 1
# array to simulate the cube
cube = array([[[0 for k in range(n)] for j in range(n)] for i in range(n)])
# value to hold all rotations
pos_states = []


# how many of the other cube we might have, ranging from 0 to n_size
def add_cubes(o_cube):
    for i in range(o_cube):
        cube[i//4][i//2 % 2][i % 2] = 1


# taken from stack overflow, to simulate every single possible face and orientation
def rotations24(polycube):
    def rotations4(polycube, axes):
        for i in range(4):
             yield rot90(polycube, i, axes)
    yield from rotations4(polycube, (1,2))
    yield from rotations4(rot90(polycube, 2, axes=(0,2)), (1,2))
    yield from rotations4(rot90(polycube, axes=(0,2)), (0,1))
    yield from rotations4(rot90(polycube, -1, axes=(0,2)), (0,1))
    yield from rotations4(rot90(polycube, axes=(0,1)), (0,2))
    yield from rotations4(rot90(polycube, -1, axes=(0,1)), (0,2))


# array to see all possible values
val = []

# for all possible values in range up to actual size
for i in range(0, n_size):
    # value to hold how many unique ones there are
    tval = 0
    pos_states = []
    # generate how many of the other color there are
    add_cubes(i)
    # permeate with all possible combinations.
    perm_states = sorted(set(list(it.permutations(cube.flatten()))))
    # loop through while perm_states is not size 0 for a specific state in perm_states
    while len(perm_states) != 0:
        for z in perm_states:
            # count it as a unique state
            tval += 1
            # find all rotations of the permutation
            for x in rotations24(array(z).reshape(2, 2, 2)):
                x = tuple(x.flatten())
                pos_states.append(x)
            # and remove them from perm_states
                while x in perm_states:
                    perm_states.remove(x)
        pos_states = sorted(set(pos_states))
    val.append(tval)

print(val)
print(sum(val))

