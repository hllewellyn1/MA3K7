########################
# MA3K7 - ASSIGNMENT 4 #
########################

import math
import cv2
import sys
import numpy as np

###############################
# GLOBAL VARIABLE DEFINITIONS #
###############################

N = 50

# COLOURS for cv2 (BGR)

BLACK = (0,0,0)



##############################################
# method 1 - iterative                       #
#                                            #
# - constructs spiral using direction method #
##############################################

# assertions
# -----------

# we assert that N is an integer greater than 2

if ((type(N) != int) or (N <= 2)):
    sys.exit("N must be an integer greater than 2")


# initialisation
# ---------------

# compute dimension of our array (we make it two bigger than we need, so to
# avoid needing array index checks)

if (math.ceil(math.sqrt(N))%2 == 0):
    dim = (math.ceil(math.sqrt(N)) + 1) + 2
else:
    dim = math.ceil(math.sqrt(N)) + 2

# we create a dim x dim array of zeros
    
matrix = []

for i in range(dim):
    toAdd = []
    for j in range(dim):
        toAdd.append(0)
    matrix.append(toAdd)


# compute spiral
# ---------------

# we add the first two values to our spiral
    
matrix_centre = int((dim-1)/2 )
       
matrix[matrix_centre][matrix_centre] = 1
matrix[matrix_centre][matrix_centre + 1] = 2

# we store these positions in 2-long lists

pos_n_minus_1 = [matrix_centre,matrix_centre + 1]
pos_n_minus_2 = [matrix_centre,matrix_centre]

# we iterate our algorithm and place naturals up to n

for i in range(3,N+1):
    
    # case 1 - (n-1) is absolutely right of (n-2)

    if ( (pos_n_minus_1[0] == pos_n_minus_2[0]) and (pos_n_minus_1[1] == pos_n_minus_2[1] + 1) ):
        
        # we check whether the space to the left has been filled, else we fill 
        # the one immediately forward

        if (matrix[pos_n_minus_1[0] - 1][pos_n_minus_1[1]] == 0):
            
            # place
            matrix[pos_n_minus_1[0] - 1][pos_n_minus_1[1]] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0] - 1,pos_n_minus_1[1]]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n

        else:
            
            # place
            matrix[pos_n_minus_1[0]][pos_n_minus_1[1] + 1] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0],pos_n_minus_1[1] + 1]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n



    # case 2 - (n-1) is absolutely above (n-2)

    elif ( (pos_n_minus_1[0] + 1 == pos_n_minus_2[0]) and (pos_n_minus_1[1] == pos_n_minus_2[1]) ):
        
        # we check whether the space to the left has been filled, else we fill 
        # the one immediately forward
        
        if (matrix[pos_n_minus_1[0]][pos_n_minus_1[1] - 1] == 0):
            
            # place
            matrix[pos_n_minus_1[0]][pos_n_minus_1[1] - 1] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0],pos_n_minus_1[1] - 1]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n

        else:
            # place

            matrix[pos_n_minus_1[0] - 1][pos_n_minus_1[1]] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0] - 1,pos_n_minus_1[1]]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n



    # case 3 - (n-1) is absolutely left of (n-2)

    elif ( (pos_n_minus_1[0] == pos_n_minus_2[0]) and (pos_n_minus_1[1] == pos_n_minus_2[1] - 1) ):
        
        # we check whether the space to the left has been filled, else we fill 
        # the one immediately forward
        
        if (matrix[pos_n_minus_1[0] + 1][pos_n_minus_1[1]] == 0):
            
            # place
            matrix[pos_n_minus_1[0] + 1][pos_n_minus_1[1]] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0] + 1,pos_n_minus_1[1]]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n

        else:
            # place
            matrix[pos_n_minus_1[0]][pos_n_minus_1[1] - 1] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0],pos_n_minus_1[1] - 1]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n

    # case 4 - (n-1) is absolutely below (n-2)

    elif ( (pos_n_minus_1[0] - 1 == pos_n_minus_2[0]) and (pos_n_minus_1[1] == pos_n_minus_2[1]) ):
        
        # we check whether the space to the left has been filled, else we fill 
        # the one immediately forward
        
        if (matrix[pos_n_minus_1[0]][pos_n_minus_1[1] + 1] == 0):
            
            # place
            matrix[pos_n_minus_1[0]][pos_n_minus_1[1] + 1] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0],pos_n_minus_1[1] + 1]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n

        else:
            
            # place
            matrix[pos_n_minus_1[0] + 1][pos_n_minus_1[1]] = i

            # update position vectors

            pos_n = [pos_n_minus_1[0] + 1,pos_n_minus_1[1]]
            pos_n_minus_2 = pos_n_minus_1
            pos_n_minus_1 = pos_n

# we trim down our matrix (since we added padding to avoid index checks)
            
temp_matrix = []

for i in range(1,dim-1):
    toAdd = []
    for j in range(1,dim-1):
        toAdd.append(matrix[i][j])
    temp_matrix.append(toAdd)

matrix = temp_matrix
        

# # visualise (using 600x600 png)
# # ----------

# # create and initialise pixel map

img = np.zeros((600,600,3),dtype='uint8')

img[:] = 255

for i in range(dim-2):
    for j in range(dim-2):
        x_coord = int(500*i/(dim-2)) + 50
        y_coord = int(500*j/(dim-2)) + 50
        img = cv2.putText(img, str(matrix[j][i]), (x_coord,y_coord), cv2.FONT_HERSHEY_COMPLEX,1, BLACK, 1, cv2.LINE_AA) 

# display image

cv2.imshow("MA3K7 Ass. 5",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(matrix)


###############################################
# method 2 - explicit                         #
#                                             #
# - constructs spiral using piecewise formula #
###############################################

# assertions
# ----------

# we assert that n be a natural number

if ((type(N) != int) or (N < 1)):
    sys.exit("N must be a natural number")


# compute spiral
# --------------

# populate a list of coordinates
    
coords = []

for i in range(1,N+1):
    
    # we compute m
    m = int(2*math.floor((math.sqrt(i)+1)/2)-1)

    # we compute coords of m under phi

    a = (m-1)/2
    b = (1-m)/2

    # case 1 (n == m**2)
    if (i == m**2):
        coords.append( (a, b) )
    
    # case 2 (upward-pointing band)
    elif ( (m**2 < i) and (i <= m**2 + (m+1)) ):
        coords.append( (a+1, (b-1)+(i-m**2)) )

    # case 3 (left-pointing band)
    elif ( (m**2 + (m+1) < i) and (i <= m**2 + 2*(m+1)) ):
        coords.append( ((a+1)-(i-m**2)+(m+1), b+m) )
    
    # case 4 (downward-pointing band
    elif ( (m**2 + 2*(m+1) < i) and (i <= m**2 + 3*(m+1)) ):
        coords.append( (a-m, (b+m) - (i-m**2) + 2*(m+1)) )
    
    # case 5 (right-pointing band)
    elif ( (m**2 + 3*(m+1) < i) and (i <= m**2 + 3*(m+1) + m) ):
        coords.append( (a-m+(i-m**2)-3*(m+1), b-1) )

    #print(str(i) + ": " + str(coords[i-1]))


# visualise
# ----------

for i in range(1,len(coords)+1):
    print(str(i) + ": " + str(coords[i-1]))
    
    