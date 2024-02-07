##################################
# MA3K7 ASS. 2 - BINARY MATRICES #
##################################

import math as m
import numpy as np

###############################################################################
# GLOBAL VARIABLE DECLARATIONS
###############################################################################

# dimension of matrix
DIM = 3

# format specifier (dependent on DIM)
spec = "0" + str(DIM**2) + "b"

###############################################################################
# removeFromList()
#
# - utility function for removing values from list
###############################################################################

def removeFromList(xs, val):
   return [value for value in xs if value != val]

###############################################################################
# main()
#
# - there's no actual main function, this is just where execution starts!
###############################################################################

# generate a list of every binary number up to 2^(n^2)

binary_nums = []

for i in range(2**(DIM**2)):
    num = format(i,spec)
    binary_nums.append(num)

# convert these to matrices
    
matrices = []

for i in range(2**(DIM**2)):
    a = []
    for j in range(DIM**2):
        a.append(int(binary_nums[i][j]))
    b = np.array(a)
    matrices.append(np.reshape(b, (DIM,DIM)))

# remove the ones that aren't valid games

toRemove = []
    
for i in matrices:

    num0 = np.count_nonzero(i==0)
    num1 = np.count_nonzero(i==1)

    # player 0 goes first

    if ((num0 == m.ceil(DIM/2)) and (num1 == m.floor(DIM/2))):
        continue

    # player 1 goes first

    elif ((num0 == m.floor(DIM/2)) and (num1 == m.ceil(DIM/2))):
        continue

    else:
        toRemove.append(i)

for i in toRemove:
    if i in matrices:
        matrices.remove(i)

# show results
print(matrices)


###############################################################################
# PERMUTATIONS AND THEIR SIGNS
#
# i didn't end up using this stuff, but i'll include it anyway
###############################################################################

'''

# provide a list and return all possible permutations

def permute(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in permute(xs, low + 1):
            yield p        
        for i in range(low + 1, len(xs)):        
            xs[low], xs[i] = xs[i], xs[low]
            for p in permute(xs, low + 1):
                yield p        
            xs[low], xs[i] = xs[i], xs[low]

# given a permutation, return it's sign
            
def sign(xs):
    n = len(xs)
    cnt = 0
    for i in range(n):
        for j in range(i+1,n):
            if (xs[i]>xs[j]):
                cnt+=1
    return cnt%2

# print all signs of permutations of S_4

for p in permute([1, 2, 3, 4]):
    print(p)

'''