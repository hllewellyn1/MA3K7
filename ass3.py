###############################################################################
# MA3K7 - ASSIGNMENT 3 (HAT NUMBERS)
###############################################################################

import random as rand
import matplotlib.pyplot as plt

###############################################################################
# GLOBAL VARIABLES DECLARATIONS
###############################################################################

N = 15743

###############################################################################
# play()
#
# this function generates [1,2,...,2024], removes numbers randomly and adds
# their difference (as described in the problem), then returns the final int
###############################################################################

def play():

    # construct list [1,2,...,2024]

    hat = []

    for i in range(1,N+1):
        hat.append(i)
        
    while (len(hat)>1):

        # choose a random index and remove it from 'hat'

        ind1 = rand.randint(0,len(hat)-1)
        num1 = hat[ind1]

        hat.pop(ind1)

        # choose another random index and remove it from 'hat'

        ind2 = rand.randint(0,len(hat)-1)
        num2 = hat[ind2]

        hat.pop(ind2)

        # find the difference and add it to 'hat'
            
        diff = abs(num1-num2)
        hat.append(diff)
    
    return hat[0]



###############################################################################
# main()
#
# no real main function, but execution starts here
###############################################################################

xs = []

for i in range(1000):
    xs.append(play())
    #debug
    print(play())
    #print("i = " + str(i))

#pp.plot(xs, len(xs) * [0], "x")

fig,ax = plt.subplots()    

#ax.boxplot(xs,showfliers=False,vert=False)
ax.violinplot(xs,vert=False,showmedians=True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.yticks([])
plt.xlim(-1,N)
plt.show()