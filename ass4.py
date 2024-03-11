########################
# MA3K7 - ASSIGNMENT 4 #
########################

import sys

######################
# CLASS DECLARATIONS #
######################

class Node:

    def __init__(self, value = None, left = None, right = None):
        self.value = value
        self.left  = left
        self.right = right

    def __str__(self):
        return f"Node(val = {self.value}, l = {self.left}, r = {self.right})"
    
  
###############################################################################
# extendTree()
#
# - this extends a tree, as would a toss of the coin
###############################################################################

def extendTree(tree):
    
    # if it's the end of a branch, we extend that branch

    if (type(tree.left) != Node):
        tree.left = Node(tree.left, tree.left+1, tree.left+2)
        tree.right = Node(tree.right, tree.right+1, tree.right+2) 

    # if it's not the end of a branch, we increase the recursion depth
    # in order to find the end
        
    else:
        extendTree(tree.left)
        extendTree(tree.right)


###############################################################################
# listFromBranch()
#
# - given a binary tree and a branch specifier (binary number/sequence), this
#   function returns a list of values on the specified branch.
#
# - important note:
#
#   this function does not check whether the branch specifier is compatible
#   (it doesn't check the depth of the tree, neither does it check whether
#   the tree is binary or not) with the passed tree.  please be sure of this 
#   when calling.
#        
###############################################################################
        
def listFromBranch(tree,specifier):
    
    subtree = tree
    branch = []

    # we add the root value to the list

    branch.append(subtree.value)

    for i in range(len(specifier)):
        
        if(specifier[i] == '0'):
            
            # add left value to list (might be node, might be int)

            if (type(subtree.left) == Node):
                branch.append(subtree.left.value)
            else:
                branch.append(subtree.left)

            # continue down left of tree
            subtree = subtree.left

        if(specifier[i] == '1'):
            
            # add right value to list (might be node, might be int)

            if (type(subtree.right) == Node):
                branch.append(subtree.right.value)
            else:
                branch.append(subtree.right)

            # continue down right of tree
            subtree = subtree.right
        
    return branch
    

#########################################################################
# P_K(k)
#
# - this function finds the probability that P(K) happens for target 'k'
#   (see rubric for details).  it does this by constructing the prob.
#   tree, traversing every branch and incrementing a counter if that
#   branch passes by k.
#########################################################################

def P_K(k):
    
    # we assert that k>1 is an integer

    if (int(k) != k):
        sys.exit("k must be an integer greater than 1")

    if (k<=1):
        sys.exit("k must be an integer greater than 1")

    # we generate the probability tree
        
    probTree = Node(1,2,3)

    for i in range(k-2):
        print("Extending Tree - Progress:  " + str(i) + "/" + str(k-2))
        extendTree(probTree)
    
    # we generate the list of all binary numbers from 0 to 2^(k-1)-1,
    # from which one can construct a bijection to the set of branch
    # specifiers for binary trees

    binary_nums = []

    for i in range(2**(k-1)):
        num = format(i,"0" + str(k-1) + "b")
        binary_nums.append(num)

    # we use these branch specifiers to count the branches which contain k

    num_succesful_branches = 0  
    
    for i in binary_nums:
        print("Checking Branch " + str(i))
        if k in listFromBranch(probTree,i):
            num_succesful_branches += 1
        
    return num_succesful_branches/(2**(k-1))


###############################################################################
# main()
#
# - no real main, but execution starts here
###############################################################################

# don't call this for k>19, it takes too long

print(P_K(7))



            


