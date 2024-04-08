############################
# MA3K7 - BIG MINI PROJECT #
############################

import os
import sys
import random as r
import numpy as np
import cv2
import matplotlib.pyplot as plt


################################
# GLOBAL VARIABLE DECLARATIONS #
################################

# maths constants

PI = 3.14159265

# colours (BGR)

BLACK = (0,0,0)
WHITE = (255,255,255)

BLUE = (252,211,3)
GREEN = (49,173,82)
RED = (3,25,255)


# timestep
DT = 0.05

# max. simulation time
T_MAX = 60

# number (initial), radius, and mass of 'A' particles

num_A = 10
RAD_A = 1
MASS_A = 1

# number (initial), radius, and mass of 'B' particles

num_B = 10
RAD_B = 2
MASS_B = 3

# number (initial), radius, and mass of 'C' particles

num_C = 10
RAD_C = 3
MASS_C = 3


# width and height of rectangular domain

DOMAIN_X = 100
DOMAIN_Y = 100

# scale factor for drawing
SCALE_FACTOR = min(500/DOMAIN_X,500/DOMAIN_Y)

# our program's state is entirely determined by the particles,
# so we create a list, 'state', to represent this

state = []


#####################
# CLASS DEFINITIONS #
#####################

class Particle:
    
    # constructor

    def __init__(self,xpos,ypos,xvel,yvel,speed,type):
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.speed = speed
        self.type = type

    # string representation
        
    def __str__(self):
        return f"Particle({self.xpos}, {self.ypos}, {self.xvel}, {self.yvel}, {self.speed}, {self.type})"
    
    # method to advance along trajectory

    def advance(self):
        global DT
        self.xpos += self.speed*self.xvel*DT
        self.ypos += self.speed*self.yvel*DT

    # gets radius from global variable

    def getRad(self):
        global RAD_A
        global RAD_B
        global RAD_C

        if (self.type == 'A'):
            return RAD_A
        elif (self.type == 'B'):
            return RAD_B
        else:
            return RAD_C
        
    # gets mass from global variable

    def getMass(self):
        global MASS_A
        global MASS_B
        global MASS_C

        if (self.type == 'A'):
            return MASS_A
        elif (self.type == 'B'):
            return MASS_B
        else:
            return MASS_C



###############################################################
# areIntersecting()                                           #
#                                                             #
# - this function takes two particles, returning true if they #
#   intersect and false otherwise                             #
###############################################################
        
def areIntersecting(particleP,particleQ):
    
    # determine radii
    
    rad_P = particleP.getRad()
    rad_Q = particleQ.getRad()

    # compute distance between particle centres - true if less than sum of radii
    
    if (np.sqrt( (particleP.xpos - particleQ.xpos)**2 + (particleP.ypos - particleQ.ypos)**2) <= rad_P+rad_Q):
        return True
    else:
        return False


###############################################################
# draw()                                                      #
#                                                             #
# - this function takes the game state and draws it using cv2 #
###############################################################
        
def draw(debug=False):
       
    # create pixel map

    img = np.zeros((600,600,3),dtype='uint8')

    img[:] = 255

    # draw domain boundary (hard-coded)

    img = cv2.line(img, (50,50), (int(DOMAIN_X*SCALE_FACTOR)+50,50), BLACK, 2)    
    img = cv2.line(img, (int(DOMAIN_X*SCALE_FACTOR)+50,50), (int(DOMAIN_X*SCALE_FACTOR)+50,int(DOMAIN_Y*SCALE_FACTOR)+50), BLACK, 2)  
    img = cv2.line(img, (int(DOMAIN_X*SCALE_FACTOR)+50,int(DOMAIN_Y*SCALE_FACTOR)+50), (50,int(DOMAIN_Y*SCALE_FACTOR)+50), BLACK, 2)  
    img = cv2.line(img, (50,int(DOMAIN_Y*SCALE_FACTOR)+50), (50,50), BLACK, 2)  

    # draw domain boundary (using linesegs from domain_boundary)

    # ...

    # draw particles
    # if particles are too small compared to domain, then they don't draw as their radius
    # gets rounded to zero (by int()).  we should check for this and just draw the smallest possible circle

    for i in range(num_A+num_B+num_C):
        #A
        if (state[i].type == 'A'):
            img = cv2.circle(img, (int((state[i].xpos) * SCALE_FACTOR )+50,int((state[i].ypos) * SCALE_FACTOR )+50), int(SCALE_FACTOR*RAD_A), BLUE , -1) 
        #B
        elif (state[i].type == 'B'):    
            img = cv2.circle(img, (int((state[i].xpos) * SCALE_FACTOR )+50,int((state[i].ypos) * SCALE_FACTOR )+50), int(SCALE_FACTOR*RAD_B), GREEN , -1) 
        #C
        elif (state[i].type == 'C'):
            img = cv2.circle(img, (int((state[i].xpos) * SCALE_FACTOR )+50,int((state[i].ypos) * SCALE_FACTOR )+50), int(SCALE_FACTOR*RAD_C), RED , -1) 

    # add labels etc.

    img = cv2.putText(img, "t = " + str(round(t,1)), (50,30), cv2.FONT_HERSHEY_COMPLEX,0.75, BLACK, 1, cv2.LINE_AA)
  
    img = cv2.circle(img, (55,int(DOMAIN_Y*SCALE_FACTOR) + 75), 5, BLUE , -1) 
    img = cv2.putText(img, "particle A", (65,int(DOMAIN_Y*SCALE_FACTOR) + 78), cv2.FONT_HERSHEY_COMPLEX,0.5, BLACK, 1, cv2.LINE_AA)

    img = cv2.circle(img, (175,int(DOMAIN_Y*SCALE_FACTOR) + 75), 5, GREEN , -1) 
    img = cv2.putText(img, "particle B", (185,int(DOMAIN_Y*SCALE_FACTOR) + 78), cv2.FONT_HERSHEY_COMPLEX,0.5, BLACK, 1, cv2.LINE_AA)

    img = cv2.circle(img, (295,int(DOMAIN_Y*SCALE_FACTOR) + 75), 5, RED , -1) 
    img = cv2.putText(img, "particle C", (305,int(DOMAIN_Y*SCALE_FACTOR) + 78), cv2.FONT_HERSHEY_COMPLEX,0.5, BLACK, 1, cv2.LINE_AA)

    # show and add to list for video processing

    video.write(img)

    debug_start = 4.7
    debug_end =  T_MAX

    if ((debug==True) and (t>debug_start) and (t<debug_end) ):
        cv2.imshow("MA3K7 BIG PROJECT (t="+str(round(t,2))+")",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


###############################################################
# ppCollide()                                                 #
#                                                             #
# - this function deals with all particle-particle collisions #
###############################################################
    
def ppCollide():
    
    # we construct a list of pairs (we do this instead of a nested for loop
    # because we consider (i,j) = (j,i))

    global num_A
    global num_B
    global num_C
    
    listOfUniqueTuples = []

    for i in range(num_A+num_B+num_C):
        for j in range(num_A+num_B+num_C):
            if not ((j,i) in listOfUniqueTuples):
                listOfUniqueTuples.append((i,j))
        
    # we loop over this list
                
    for n in range(len(listOfUniqueTuples)):
        
        i = listOfUniqueTuples[n][0]
        j = listOfUniqueTuples[n][1]
        
        # compute mass of particle_i

        mass_i = state[i].getMass()
    

        # we don't want to consider particle_i here

        if (i==j):
            continue
        
        # we only proceed if they are colliding

        if (not areIntersecting(state[i],state[j])):
            continue
            
        # compute mass of particle_j

        mass_j = state[j].getMass()
        

        # compute new velocity vectors

        xvel_i = state[i].xvel
        yvel_i = state[i].yvel

        xvel_j = state[j].xvel
        yvel_j = state[j].yvel

        cx_i = state[i].xpos
        cy_i = state[i].ypos

        cx_j = state[j].xpos
        cy_j = state[j].ypos

            
        # newxvel_i = xvel_i - ( (2*mass_j) / (mass_i + mass_j) ) * ( ((xvel_i - xvel_j)*(cx_i - cx_j) + (yvel_i - yvel_j)*(cy_i - cy_j)) / (np.abs(cx_i - cx_j)**2) ) * (cx_i - cx_j)
        # newyvel_i = yvel_i - ( (2*mass_j) / (mass_i + mass_j) ) * ( ((xvel_i - xvel_j)*(cx_i - cx_j) + (yvel_i - yvel_j)*(cy_i - cy_j)) / (np.abs(cy_i - cy_j)**2) ) * (cy_i - cy_j)

        
        newxvel_i = xvel_i - ( (2*mass_j) / (mass_i + mass_j) ) * ( ((xvel_i - xvel_j)*(cx_i - cx_j) + (yvel_i - yvel_j)*(cy_i - cy_j)) / (np.linalg.norm([cx_i-cx_j,cy_i-cy_j])**2) ) * (cx_i - cx_j)
        newyvel_i = yvel_i - ( (2*mass_j) / (mass_i + mass_j) ) * ( ((xvel_i - xvel_j)*(cx_i - cx_j) + (yvel_i - yvel_j)*(cy_i - cy_j)) / (np.linalg.norm([cx_i-cx_j,cy_i-cy_j])**2) ) * (cy_i - cy_j)

        # newxvel_j = xvel_j - ( (2*mass_i) / (mass_i + mass_j) ) * ( ((xvel_j - xvel_i)*(cx_j - cx_i) + (yvel_j - yvel_i)*(cy_j - cy_i)) / (np.abs(cx_j - cx_i)**2) ) * (cx_j - cx_i)
        # newyvel_j = yvel_j - ( (2*mass_i) / (mass_i + mass_j) ) * ( ((xvel_j - xvel_i)*(cx_j - cx_i) + (yvel_j - yvel_i)*(cy_j - cy_i)) / (np.abs(cy_j - cy_i)**2) ) * (cy_j - cy_i)

        newxvel_j = xvel_j - ( (2*mass_i) / (mass_i + mass_j) ) * ( ((xvel_j - xvel_i)*(cx_j - cx_i) + (yvel_j - yvel_i)*(cy_j - cy_i)) / (np.linalg.norm([cx_j-cx_i,cy_j-cy_i])**2) ) * (cx_j - cx_i)
        newyvel_j = yvel_j - ( (2*mass_i) / (mass_i + mass_j) ) * ( ((xvel_j - xvel_i)*(cx_j - cx_i) + (yvel_j - yvel_i)*(cy_j - cy_i)) / (np.linalg.norm([cx_j-cx_i,cy_j-cy_i])**2) ) * (cy_j - cy_i)
           

        # normalise and set new velocity vectors

        state[i].xvel = newxvel_i / (np.sqrt(newxvel_i**2 + newyvel_i**2))
        state[i].yvel = newyvel_i / (np.sqrt(newxvel_i**2 + newyvel_i**2))

        state[j].xvel = newxvel_j / (np.sqrt(newxvel_j**2 + newyvel_j**2))
        state[j].yvel = newyvel_j / (np.sqrt(newxvel_j**2 + newyvel_j**2))


        # change particle type

        # A and B colliding
        if ((state[i].type == 'A' and state[j].type == 'B') or (state[j].type == 'A' and state[i].type == 'B')):
            state[i].type = 'C'
            state[j].type = 'C'
            num_A = num_A - 1
            num_B = num_B - 1
            num_C = num_C + 2
        elif ((state[i].type == 'B' and state[j].type == 'C') or (state[j].type == 'B' and state[i].type == 'C')):
            state[i].type = 'A'
            state[j].type = 'A'
            num_C = num_C - 1
            num_B = num_B - 1
            num_A = num_A + 2
        elif ((state[i].type == 'A' and state[j].type == 'C') or (state[j].type == 'A' and state[i].type == 'C')):
            state[i].type = 'B'
            state[j].type = 'B'
            num_A = num_A - 1
            num_C = num_C - 1
            num_B = num_B + 2

        # otherwise, collisions will register at next timestep

        for k in range(5):
            state[i].advance()
            state[j].advance()

    return


###############################################################
# pbCollide()                                                 #
#                                                             #
# - this function deals with all particle-boundary            #
#   collisions.  it uses the formula v-2(v.n)n for when one   #
#   surface is the reflector, and simply flips v when two     #
#   are at play (since corners are retroreflectors)           #
#                                                             #
###############################################################
    
def pbCollide():
    
    # we loop over all particles

    for i in range(len(state)):
        
        # we get the radius of our particle
        rad = state[i].getRad()
        
        # 9 possible cases:

        # touching top ?

        if (state[i].ypos - rad <= 0):  
            
            # also touching left or right?

            if ( (state[i].xpos - rad <= 0) or (state[i].xpos + rad >= DOMAIN_X) ):  
                
                # flip velocity vector
                state[i].xvel = -state[i].xvel
                state[i].yvel = -state[i].yvel

                # advance (to avoid re-dedection of boundary collision)

                for j in range(3):
                    state[i].advance()

            else:
                
                # normal vector of top boundary
                nml = (0,-1)

                # compute new velocity vector
                new_x = state[i].xvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[0])
                new_y = state[i].yvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[1])

                # update velocity vector
                state[i].xvel = new_x / np.sqrt(new_x**2 + new_y**2)
                state[i].yvel = new_y / np.sqrt(new_x**2 + new_y**2)

                # make sure is in domain

                state[i].ypos = rad

                # advance (to avoid re-dedection of boundary collision)
                for j in range(3):
                    state[i].advance()

        # touching right ?

        elif (state[i].xpos + rad >= DOMAIN_X):
            
            # also touching bottom ?

            if (state[i].ypos + rad >= DOMAIN_Y):
                
                # flip vector
                state[i].xvel = -state[i].xvel
                state[i].yvel = -state[i].yvel

                # advance (to avoid re-dedection of boundary collision)
                for j in range(3):
                    state[i].advance()

            # just right

            else:
                
                # normal vector of right boundary
                nml = (-1,0)

                # compute new velocity vector
                new_x = state[i].xvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[0])
                new_y = state[i].yvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[1])

                # update velocity vector
                state[i].xvel = new_x / np.sqrt(new_x**2 + new_y**2)
                state[i].yvel = new_y / np.sqrt(new_x**2 + new_y**2)

                # make sure is in domain

                state[i].xpos = 100 - rad

                # advance (to avoid re-dedection of boundary collision)
                
                for j in range(3):
                    state[i].advance()

        # touching bottom ?

        elif (state[i].ypos + rad >= DOMAIN_Y):
            
            # also touching left ?

            if  (state[i].xpos - rad <= 0):
                
                # flip vector
                state[i].xvel = -state[i].xvel
                state[i].yvel = -state[i].yvel

                # advance (to avoid re-dedection of boundary collision)
                
                for j in range(3):
                    state[i].advance()

            # just bottom

            else:
                
                # normal vector of bottom boundary
                nml = (0,1)

                # compute new velocity vector
                new_x = state[i].xvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[0])
                new_y = state[i].yvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[1])

                # update velocity vector
                state[i].xvel = new_x / np.sqrt(new_x**2 + new_y**2)
                state[i].yvel = new_y / np.sqrt(new_x**2 + new_y**2)

                # make sure is in domain

                state[i].ypos = 100 - rad

                # advance (to avoid re-dedection of boundary collision)
                
                for j in range(3):
                    state[i].advance()

        # touching left ?

        elif  (state[i].xpos - rad <= 0):
            
            # normal vector of left boundary
            nml = (1,0)

            # compute new velocity vector
            new_x = state[i].xvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[0])
            new_y = state[i].yvel - 2*( (state[i].xvel * nml[0]) + (state[i].yvel * nml[1]) )*(nml[1])

            # update velocity vector
            state[i].xvel = new_x / np.sqrt(new_x**2 + new_y**2)
            state[i].yvel = new_y / np.sqrt(new_x**2 + new_y**2)

            # make sure is in domain

            state[i].xpos = rad

            # advance (to avoid re-dedection of boundary collision)
            
            for j in range(3):
                state[i].advance()

        # no collision

        else:
            continue
            
    return
    


###############################################################################
# main()
#
# - no main() as such, but execution starts here
###############################################################################

# ASSERTIONS ON INPUT PARAMETERS
# -------------------------------

# we require all radii, domain dimensions, and masses to be positive
    
if ((RAD_A <= 0) or (RAD_B <= 0) or (RAD_C <= 0)):
    sys.exit("one or more particle radii are non-positive")

if ((DOMAIN_X <= 0) or (DOMAIN_Y <= 0)):
    sys.exit("one or more domain dimensions are non-positive")

if ((MASS_A <= 0) or (MASS_B <= 0) or (MASS_C <= 0)):
    sys.exit("one or more particle masses are non-positive")


# we require T_MAX be non-negative
    
if (T_MAX < 0):
    sys.exit("T_MAX is negative")


# we require DOMAIN_X,DOMAIN_Y > max(RAD_A,RAD_B,RAD_C), so that
# particles are guaranteed to fit inside the domain
    
if (min(DOMAIN_X,DOMAIN_Y) <= 2*max(max(RAD_A,RAD_B),max(RAD_B,RAD_C))):
    sys.exit("one or more particle radii greater than domain size")

# we require particle radii be no less than max(DOMAIN_X,DOMAIN_Y)/100,
# so to prevent rendering issues (compute actual bound)
    
# ...
    


# INITIALISATION OF SIMULATION
# -----------------------------
        
# we'll uniformly distribute the spatial coordinates of our
# (num_A+num_B+num_C) particles across our domain.  
    
# when doing so, we take into account each particle's radius
# so that all particles spawn entirely in the domain

x_coords = []
y_coords = []

for i in range(num_A+num_B+num_C):
    x = r.uniform(0,(DOMAIN_X))
    y = r.uniform(0,(DOMAIN_Y))
    x_coords.append(round(x,2))
    y_coords.append(round(y,2))
    

# we'll uniformly distribute the velocity vectors of our 
# (num_A+num_B+num_C) particles, converting from polar to
# cartesian.  this way, we don't have to normalise.
    
x_components = []
y_components = []
    
for i in range(num_A+num_B+num_C):
    theta = r.uniform(0,2*PI)
    x = np.cos(theta)
    y = np.sin(theta)
    x_components.append(round(x,2))
    y_components.append(round(y,2))

# we'll uniformly distribute the speeds between 0 and 3
    
speeds = []

for i in range(num_A+num_B+num_C):
    v = r.uniform(15,20)
    speeds.append(v)


# we then populate 'state' with A, B and C particles in turn

for i in range(num_A):
    state.append(Particle(x_coords[i],y_coords[i],x_components[i],y_components[i],speeds[i],'A'))

for i in range(num_B):
    index = num_A + i
    state.append(Particle(x_coords[index],y_coords[index],x_components[index],y_components[index],speeds[i],'B'))

for i in range(num_C):
    index = num_A + num_B + i
    state.append(Particle(x_coords[index],y_coords[index],x_components[index],y_components[index],speeds[i],'C'))




'''
# INITIALISATION (DEBUG)
# ----------------------

num_A = 0

num_B = 0

#state.append(Particle(100,100,1,0,10,'B'))

num_C = 4

# state.append(Particle(25,25,-1/np.sqrt(2),-1/np.sqrt(2),20,'C'))
# state.append(Particle(25,75,1/np.sqrt(2),-1/np.sqrt(2),20,'C'))
# state.append(Particle(75,75,1/np.sqrt(2),1/np.sqrt(2),20,'C'))
# state.append(Particle(75,25,-1/np.sqrt(2),1/np.sqrt(2),20,'C'))

state.append(Particle(25,25,-np.cos(PI/8),-np.sin(PI/8),20,'C'))
state.append(Particle(25,75,np.sin(PI/8),-np.cos(PI/8),20,'C'))
state.append(Particle(75,75,np.cos(PI/8),np.sin(PI/8),20,'C'))
state.append(Particle(75,25,-np.sin(PI/8),np.cos(PI/8),20,'C'))
    
'''

# RUNNING OF SIMULATION
# ----------------------

# set initial time
t = 0


# set up videowriter

frame_rate = 1/DT

video = cv2.VideoWriter('sim.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (600, 600))


# we simulate until either 1) a steady state is reached, or 2)
# we reach t=T_MAX.

continueSim = True

# log

file = open("log.txt", "w")
file.write(str(round(t,2)) + " " + str(num_A) + " " + str(num_B) + " " + str(num_C) + " " + "\n")
file.close()

while(continueSim):
    
    # we draw the game state
    draw(debug=False)
    
    # we deal with particle-particle collisions
    ppCollide()

    # we deal with particle-boundary collisions
    pbCollide()

    # we call advance()

    for i in range(num_A+num_B+num_C):
        state[i].advance()

    # we check to see whether continueSim should be false

    if (num_A == 0 and num_B==0):
        continueSim = False
    
    if (num_A == 0 and num_C==0):
        continueSim = False

    if (num_B == 0 and num_C==0):
        continueSim = False

    if (round(t,2) >= T_MAX):
        continueSim = False

    # we advance time
        
    print(round(t,2))
    t += DT

    # log

    file = open("log.txt", "a")
    file.write(str(round(t,2)) + " " + str(num_A) + " " + str(num_B) + " " + str(num_C) + " " + "\n")
    file.close()


video.release()


#################################
# PLOTTING OF NUMS AGAINST TIME #
#################################


# read in data from file

file = open("log.txt", "r")

raw_data = file.readlines()

# parse and store in arrays

time_data = []

A_data = []
B_data = []
C_data = []

for i in range(len(raw_data)):
    if i%10 == 0:
        parsed = raw_data[i].split(" ")
        time_data.append(float(parsed[0]))
        A_data.append(int(parsed[1]))
        B_data.append(int(parsed[2]))
        C_data.append(int(parsed[3]))

# plot

plt.plot(time_data, A_data, label = "num_A") 
plt.plot(time_data, B_data, label = "num_B") 
plt.plot(time_data, C_data, label = "num_C") 

plt.locator_params(axis='y', nbins=6)

plt.xlabel("t (s)")
plt.ylabel("Number of particles")

plt.legend() 
plt.show()


###############################################################################
# FOOTNOTES:
#
# 1) there are some resolution issues (can't draw really small particles).
#    perhaps we should take advantage of cv2.resize(), as well as rendering
#    to a bigger grid.  for the meanwhile however, just don't use huge domains
#    with tiny particles, try and keep radii greater than 1/100 of domain
#    length or width.  MAKE SURE TO CALCULATE THE ACTUAL BOUND ON RADII
#
# 2) if making the move to arbitrary jordan curve domains, a few changes need
#    to be made.  firstly, we need an actual representation of the domain,
#    specifically one that allows computation of normal vectors at any point,
#    and one that allows us to use our isInInterior() function.  i'd imagine
#    linesegments would be great for this.
#
###############################################################################
#
# TO-DO:
#
# 1) sort out ppCollide to deal with collisions between particles that share
#    an x component or y component.  currently, that results in a division by
#    zero (take a look at velocity vector formula)
#
# 2) there's an issue were particle might spawn on top of each other, and so will
#    collide forever
#
#
###############################################################################














