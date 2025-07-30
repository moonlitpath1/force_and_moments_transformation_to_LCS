# user data
from math import sqrt

def get_unit_vectors(o,v):

    #vector translation
    # do z - o, x - o
    translated = [v[i] - o[i] for i in range(3)]

    # compute magnitude 
    # v_mag = sqrt(vx2 + vy2 + vz2)
    magnitude = sqrt(sum(vect**2 for vect in translated))


    # compute direction cosines
    # direction cosines are components of unit vector in a 3d space
    return [round(vect/ magnitude, 8) for vect in translated]



def cross_product(a,b):
    return [
    round(a[1]*b[2] - a[2]*b[1], 8),  # i
    round(a[2]*b[0] - a[0]*b[2], 8),  # j
    round(a[0]*b[1] - a[1]*b[0], 8)   # k
]

def normalize(v):
    mag = sqrt(sum(i**2 for i in v))
    return [round(i / mag, 8) for i in v]
        
        







f = [5.338936329,	-0.2204605639,	1.947337627]

# origin
o = [-0.384017,	-0.369527,	-2.12E-03]

# x and z vector
# represented in the form of 
#   [ai + bj + ck = 0]
z = [-34.586,	-0.369527,	93.96715]
x = [93.58524,	-0.369527,	34.1999]

# --------------------------------------------
# get direction cosines 

z_cosines = get_unit_vectors(o,z)
x_cosines = get_unit_vectors(o,x)

# ---------------------------------------------
# z_cosines and x_cosines are unit vectors. 
# using them we can calc y's unit vector
#   use cross product
        #  y = z X x
# find determinant
#
# A × B = i(Ay * Bz - Az * By)
#       − j(Ax * Bz - Az * Bx)
#       + k(Ax * By - Ay * Bx)
# ----------------------------------------------


y_cosines_raw = cross_product(z_cosines, x_cosines)
y_cosines = normalize(y_cosines_raw)
# --------------s--------------------------------
# calculate f in lcs for each axis (x,y,z)
# xi, xj, xk are direc cosines along x direc --- x_cosines
    # fx total = fx xi + fy xj + fz xk

f_local = [
    round(sum(f[i] * x_cosines[i] for i in range(3)), 8),
    round(sum(f[i] * y_cosines[i] for i in range(3)), 8),
    round(sum(f[i] * z_cosines[i] for i in range(3)), 8)
]

print(z_cosines)

for i in range(3):
    print(f[i] * z_cosines[i])

print(f_local)












    




