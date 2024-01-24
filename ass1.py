###################################
# MA3K7 ASS. 1 - NUMBER BRACELETS #
###################################


###############################################################################
# GLOBAL VARIABLE DECLARATIONS
###############################################################################

# counter for number of bracelets
num_brac = 0


###############################################################################
# brac()
#
# - given a seed (x,y), this function returns the generated bracelet (list)
###############################################################################

def brac(x,y):
    out = [x,y]
    while ( not ((out[-1] == out[0]) and ((out[-2]+out[-1]) % 10 == out[1])) ):
        out.append((out[-2] + out[-1]) % 10)
    return out


###############################################################################
# compare()
#
# - given a bracelet, b, this function iterates over every pair of it's values
#   (i.e. equivalent seeds) and removes them from 'seeds'.  it also increments
#   num_brac   
###############################################################################

def compare(b):
    # bool to keep track of whether we've removed from 'seeds'
    removed = False

    # treat num_brac as global
    global num_brac

    n = len(b)
    
    for i in range(n-1):
        if (b[i],b[i+1]) in seeds:
            seeds.remove((b[i],b[i+1]))
            removed = True
    
    if removed == True:
        num_brac += 1

    return


###############################################################################
# main()
#
# - there's no actual main function, this is just where execution starts!
###############################################################################

# construct list of all possible seeds
# ------------------------------------

seeds = []

for i in range(10):
    for j in range(10):
        seeds.append((i,j))


# construct bracelets and call compare() until 'seeds' is empty
# -------------------------------------------------------------
        
# we start with brac(1,5) since that's the one in the question
        
compare(brac(1,5))

# we then loop, constructing bracelets from the first available
# seed in 'seeds' until 'seeds' is empty

while (len(seeds) != 0):
    first_seed = seeds[0]
    compare(brac(first_seed[0],first_seed[1]))


# we print our result
# -------------------
    
print(num_brac)
