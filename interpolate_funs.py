# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 10:55:31 2016

@author: Andrej
"""

import numpy as np
from scipy.interpolate import splrep

# Filter data on a subinterval
# x - position: an average of positions
# y - value: a filtered value: average, median, lpw-pas filter
def filterData(curr_timesIn, curr_valsIn, fCode):
    if fCode == 1:
        new_time = np.mean(curr_timesIn)
        new_val = np.mean(curr_valsIn)
        return new_time, new_val



# -----------------------------------------------------------------------------
# Interpolate data
# Assumed: 
#  * tMin => min(xIn) & tMax <= max(xIn)
#  * vars curr_low_time in curr_low_ind are existing in data!
# * no times are repeated or decreasing
def interpolateBS(xIn, yIn, tMin, tMax, kIn, TsIn, fCode):

    # filter along subintervals - create filtered dataset
    new_times = np.empty(0)
    new_vals = np.empty(0)

    curr_upp_time = tMin
    curr_upp_ind = 0
    
    # Skip times lower than tMin so that next time is larger than tMin in terms of indeces: to assure that yIn[curr_low_ind] exists!
    while ((curr_upp_ind < len(xIn)-1) and (xIn[curr_upp_ind] < curr_upp_time or np.isnan(xIn[curr_upp_ind]))):
        curr_upp_ind += 1
    curr_low_ind = curr_upp_ind
    
    # interpolate:
    upp_ind_lim = np.minimum(len(xIn), len(yIn))
    curr_mid_time = tMin
    while (curr_upp_ind < upp_ind_lim-1): # We ealk through indicies!

        # Get uppper available index
        curr_low_ind = curr_upp_ind
        curr_cut_time = xIn[curr_low_ind] + TsIn
        while ((curr_upp_ind < len(xIn)-1) and (xIn[curr_upp_ind+1] <= curr_cut_time or np.isnan(xIn[curr_upp_ind]))):
            curr_upp_ind = curr_upp_ind + 1
            
        # Set new time bounds
        #curr_low_time = xIn[curr_low_ind]
        curr_upp_time = xIn[curr_upp_ind] #curr_upp_time + TsIn

        # Get times and vals if any available
        curr_times = xIn[curr_low_ind:curr_upp_ind]
        curr_vals = yIn[curr_low_ind:curr_upp_ind]
        numOfCurPs = min(len(curr_times), len(curr_vals)) # Number of points on this interval

        # Add mid points if numOfCurPs == 0:
        if numOfCurPs == 0: # Empty interval = exactly when => use linear interpolation to the next point 

            if xIn[curr_low_ind+1] > xIn[curr_low_ind]:
                slope_k = (yIn[curr_low_ind+1] - yIn[curr_low_ind]) /(xIn[curr_low_ind+1] - xIn[curr_low_ind]) # We did no move on - empty subinterval
            else:
                print 'interpolateBS: Error in handling empty time intervals'
            diff_val = slope_k*TsIn # A jump per single Ts
            
            curr_mid_time = np.maximum(xIn[curr_low_ind], curr_mid_time) + TsIn/2.0 # Not to go back in time
            curr_mid_val = yIn[curr_low_ind] + diff_val/2.0
            new_times = np.append(new_times, curr_mid_time) # Add to points
            new_vals = np.append(new_vals, curr_mid_val)
            curr_mid_time += TsIn/2.0 # Add 
            curr_mid_val += diff_val/2.0
            while (curr_mid_time < xIn[curr_low_ind+1] - TsIn/1.999): # add all empty points and not adding last point twice
                curr_mid_val += diff_val
                new_times = np.append(new_times, curr_mid_time + TsIn/2.0) # Add to points
                new_vals = np.append(new_vals, curr_mid_val)
                curr_mid_time += TsIn
                
            curr_upp_ind = curr_low_ind + 1 # Move on - this empty interval is covered
 
        elif numOfCurPs == 1: # Just add the same data point
            new_times = np.append(new_times, curr_times[0])
            new_vals = np.append(new_vals, curr_vals[0])

        elif numOfCurPs > 1:
            new_time, new_val = filterData(curr_times, curr_vals, fCode)
            new_times = np.append(new_times, new_time)
            new_vals = np.append(new_vals, new_val)


    # -----------------------------------------------------------------------------
    # Build knot points

    # 1. Knots are data points at the begining. One could remove some of data
    # data points as well
    tIn = new_times;
    # 2. Remove first k-1 and last k-1
    tIn = np.delete(tIn, range(0, kIn-1, 1))
    tIn = np.delete(tIn, range(len(tIn)-kIn+1, len(tIn)))


    # -----------------------------------------------------------------------------
    # Interpolate
    sPerD = 100 # An averge squared error per data sample
    sIn = sPerD*len(xIn)
    xbIn = new_times[0]
    xeIn = new_times[-1]
    tckOut = splrep(new_times, new_vals, xb=xbIn, xe=xeIn, k=kIn, t=tIn, s=sIn, task=-1)

    return tckOut
  

# =============================================================================  
## Test data & code
#xIn = np.array([-0.1, 0.1, 1.1, 1.9, 6.1, 7.9, 8.1])
#yIn = np.array([2, 1.0, 1.8, 0.1, 6.5, 4.1, 2.3])
#tMin, tMax = -0.1, 8.1
#kIn = 3
#TsIn = 1.1
#fCode = 1
#tck = interpolateBS(xIn, yIn, tMin, tMax, kIn, TsIn, fCode)
#from scipy.interpolate import splev
#import matplotlib.pyplot as plt
#new_y = splev(xIn, tck)
#plt.figure(1)
#plt.title('interpolateBS test plot')
#plt.plot(xIn, yIn, color = 'b', label='Orig')
#plt.plot(xIn, new_y, color = 'r', label='Interp.')
#plt.legend()
#plt.show()


