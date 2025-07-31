# user data
from math import sqrt
import pandas as pd
import env


#-------------------------------------

#clear terminal
import os
os.system('clear')  

#------------------------------------

#just for printing
# Show full output
pd.set_option('display.max_columns', None)         # Show all columns
pd.set_option('display.max_rows', None)            # Show all rows (be careful with large datasets)
pd.set_option('display.max_colwidth', None)        # Remove column width limit
pd.set_option('display.width', 0)   

#------------------------------------


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

#------------------------------------


def cross_product(a,b):
    return [
    round(a[1]*b[2] - a[2]*b[1], 8),  # i
    round(a[2]*b[0] - a[0]*b[2], 8),  # j
    round(a[0]*b[1] - a[1]*b[0], 8)   # k
]

#------------------------------------


def normalize(v):
    mag = sqrt(sum(i**2 for i in v))
    return [round(i / mag, 8) for i in v]
        
#------------------------------------


def lcs_transform(f,o,z,x):
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

    #y unit vector
    y_cosines_raw = cross_product(z_cosines, x_cosines)
    y_cosines = normalize(y_cosines_raw)


    # -----------------------------------------------


    # calculate f in lcs for each axis (x,y,z)
    # xi, xj, xk are direc cosines along x direc --- x_cosines
        # fx total = fx xi + fy xj + fz xk

    f_local = [
        round(sum(f[i] * x_cosines[i] for i in range(3)), 8),
        round(sum(f[i] * y_cosines[i] for i in range(3)), 8),
        round(sum(f[i] * z_cosines[i] for i in range(3)), 8)
    ]

    return f_local


#------------------------------------



#main function
if __name__ == '__main__':

    # Read the file
    df = pd.read_csv(env.csv_file_path)

    # Forward-fill to get the filename down to all rows
    df['Result File'] = df['Result File'].ffill()
    df['Summation Point'] = df['Summation Point'].ffill()

    # Filter out the 'Centroid' row — exclude it from the cleaned dataset
    df_data = df[df['Summation Point'] != 'Centroid'].copy()

    # Rename 
    df_data.rename(columns={
        'Result File': 'file',
        'Summation Point': 'nodeid'
    }, inplace=True)

    # df_data['file'] = filename  # Assign extracted filename to all rows

    # Create force and moment vectors
    df_data['force'] = df_data[['Fx', 'Fy', 'Fz']].values.tolist()
    df_data['moment'] = df_data[['Mx', 'My', 'Mz']].values.tolist()

    # Keep only final required columns
    df_clean = df_data[['file', 'nodeid', 'force', 'moment']].reset_index(drop=True)

    print(df_clean)

