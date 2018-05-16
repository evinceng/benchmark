# -*- coding: utf-8 -*-
"""
Created on Mon May 14 10:51:42 2018

@author: evin
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import config

import numpy as np
from scipy.interpolate import splev
from interpolate_funs import interpolateBS 

# query variables
userNames = [ "user2", "evina"] # "evina", "user2",
sessions = [ ] #  "evina2018-05-10 14:33:21.185000", "user22018-05-14 12:06:23.842000",
projectionFields = [ "userName", "relativeTime", "leftGaze:x", "leftGaze:y" ]
relativeTime = [ ] # start, end # it will get all times if not provided

# graph variables
xCoordVariable = "leftGaze:x"
yCoordVariable = "leftGaze:y"
timeStampVariable = "relativeTime"
colorUponVariable = "relativeTime"
userNameVariable = "userName"

def constructProjectionFileds(getID = False):
    fields = { }
    if not getID:
        fields["_id"] = 0
        
    for field in projectionFields:
        fields[field] = 1
        
    return fields

def constructQuery():
    query = { }
    
    if userNames:
        query["userName"] = { "$in": userNames }
        
    if sessions:
        query["sessionID"] = { "$in": sessions }
        
    if relativeTime:
        query["relativeTime"] = { "$gt": relativeTime[0], "$lt": relativeTime[1] }
        
    #print query
    
    return query

def interpolateAndPlot(xIn, yIn, tIn, tMin, tMax, k, Ts, fCode):
#    tIn = timeStamps#np.array(timeStamps)
#    xIn = coordX#np.array(coordX)
#    yIn = coordY#np.array(coordY)
    interpolatedXOnTime = interpolateBS(tIn, xIn, tMin, tMax, k, Ts, fCode)
    interpolatedYOnTime = interpolateBS(tIn, yIn, tMin, tMax, k, Ts, fCode)
    
    sampledTime = np.linspace(tMin, tMax, 1000)
    interpolatedXOnSampledTime = splev(sampledTime, interpolatedXOnTime)
    interpolatedYOnSampledTime = splev(sampledTime, interpolatedYOnTime)
    
    fig = plt.figure()
    ax = fig.gca() 
    ax.scatter(xIn, yIn, c=tIn, cmap=cm.seismic)
    ax.plot(interpolatedXOnSampledTime, interpolatedYOnSampledTime, color='green')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    
    host = config.getConfig().get("SERVER", "Host")
    port = config.getConfig().getint("SERVER", "Port")
    
    try:
        
        client = MongoClient(host=host, port=port)
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
        
    dbh = client["mediaExposureTry"]
    collection = dbh["eyesRolling"]
    
    projection = constructProjectionFileds()
    query = constructQuery()
    
    resultList = list(collection.find( query, projection))
    
    noAction = 0
    # construct users empty dict-----------------------------------------------
    users = { }
    for userName in userNames:
        users[userName] = { }
        for field in projectionFields:
            if field != userNameVariable:
                users[userName][field] = [info[field] for info in resultList if info[userNameVariable] == userName]
                
#    #fill the users dict, a slower version   
#    for row in resultList:
#        currentUser = row[userNameVariable]
#        for field in projectionFields:
#            if field != userNameVariable:
#                users[currentUser][field].append(row[field])
 
    # end of construct users dict----------------------------------------------
    
#    colorUpon = [sensor[colorUponVariable] for sensor in resultList]
#    coordX = [sensor[xCoordVariable] for sensor in resultList]
#    coordY = [sensor[yCoordVariable] for sensor in resultList]
#    timeStamps = [sensor[timeStampVariable] for sensor in resultList]
    
    #gazeCoordxnpArray = np.array(gazeCoordx)
    #gazeCoordynpArray = np.array(gazeCoordy)
    
#    fig = plt.figure()
#    ax = fig.gca() 
#    ax.scatter(coordX, coordY, c=colorUpon, cmap=cm.seismic)
#    ax.legend()
#    plt.show()
    
    # evina Configuration----------------------------------------------------------
    userName1 = "evina"
    Ts = 0.5 # Sampling frequency
    fCode = 1
    k = 3 
    tMin = 1.6
    tMax = 5
    xCoord = users[userName1][xCoordVariable]
    yCoord = users[userName1][yCoordVariable]
    timeStamps = users[userName1][timeStampVariable]
    #interpolateAndPlot(xCoord, yCoord, timeStamps, tMin, tMax, k, Ts, fCode)
    
#    interpolatedXOnTime = interpolateBS(timeStamps, xCoord, tMin, tMax, k, Ts, fCode)
#    interpolatedYOnTime = interpolateBS(timeStamps, yCoord, tMin, tMax, k, Ts, fCode)
#    
#    sampledTime = np.linspace(tMin, tMax, 1000)
#    interpolatedXOnSampledTime = splev(sampledTime, interpolatedXOnTime)
#    interpolatedYOnSampledTime = splev(sampledTime, interpolatedYOnTime)
    
    # end of evina Configuration---------------------------------------------------
    
    # user2 Configuration----------------------------------------------------------
    userName2 = "user2"
    TsUser = 0.5 # Sampling frequency
    fCodeUser = 1
    kUser = 3 
    tMinUser = 3 # 1.49
    tMaxUser = 10 # 10.2
    xCoordUser = users[userName2][xCoordVariable]
    yCoordUser = users[userName2][yCoordVariable]
    timeStampsUser = users[userName2][timeStampVariable]
    
    shift = timeStamps[-1]
    shiftedSampledTimeUser =  [time.__add__(shift) for time in timeStampsUser]

    totalTimeStamps = timeStamps + shiftedSampledTimeUser
    totalxCoord = xCoord + xCoordUser
    totalyCoord = yCoord + yCoordUser
    
    plt.figure(1)
    plt.title('Check')
    plt.plot(totalTimeStamps) #), xIn, color='blue')
    #plt.plot(t, x, color='red')
    plt.show()
    
    #interpolateAndPlot(xCoordUser, yCoordUser, timeStampsUser, tMinUser, tMaxUser, kUser, TsUser, fCodeUser)
    interpolatedXOnTimeUser = interpolateBS(totalTimeStamps, totalxCoord, tMin, tMaxUser, kUser, TsUser, fCodeUser)
    interpolatedYOnTimeUser = interpolateBS(totalTimeStamps, totalyCoord, tMin, tMaxUser, kUser, TsUser, fCodeUser)
    
    sampledTimeUser = np.linspace(tMin, tMaxUser, 1000)
    
    
    interpolatedXOnSampledTimeUser = splev(sampledTimeUser, interpolatedXOnTimeUser)
    interpolatedYOnSampledTimeUser = splev(sampledTimeUser, interpolatedYOnTimeUser)
    
    
    # end of evina Configuration---------------------------------------------------
    
    fig = plt.figure()
    ax = fig.gca() 
    #ax.scatter(xCoord, yCoord, c=timeStamps, cmap=cm.seismic)
    ax.scatter(totalxCoord, totalyCoord, c=totalTimeStamps, cmap=cm.PiYG)
    #ax.plot(interpolatedXOnSampledTime, interpolatedYOnSampledTime, color='green')
    ax.plot(interpolatedXOnSampledTimeUser, interpolatedYOnSampledTimeUser, color='yellow')
    ax.legend()
    plt.show()
#    plt.figure(2)
#    plt.title('Gap filled?')
#    plt.plot(tIn, xIn, 'ro', color='blue')
#    plt.plot(t, x, color='red')
#    plt.show()
    
            
#    plt.figure(1)
#    plt.title('Check')
#    plt.plot(timeStampsUser) #), xIn, color='blue')
#    #plt.plot(t, x, color='red')
#    plt.show()