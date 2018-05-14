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

# query variables
users = [ ] # "evina", "user2",
sessions = [ ] #  "evina2018-05-10 14:33:21.185000", "user22018-05-14 12:06:23.842000",
projectionFields = [ "userName", "relativeTime", "leftGaze:x", "leftGaze:y" ]
relativeTime = [ ] # start, end

# graph variables
xCoordVariable = "leftGaze:x"
yCoordVariable = "leftGaze:y"
colorUponVariable = "relativeTime"

def constructProjectionFileds(getID = False):
    fields = { }
    if not getID:
        fields["_id"] = 0
        
    for field in projectionFields:
        fields[field] = 1
    
    return fields

def constructQuery():
    query = { }
    
    if users:
        query["userName"] = { "$in": users }
        
    if sessions:
        query["sessionID"] = { "$in": sessions }
        
    if relativeTime:
        query["relativeTime"] = { "$gt": relativeTime[0], "$lt": relativeTime[1] }
        
    #print query
    
    return query

if __name__ == "__main__":
    try:
        client = MongoClient(host="localhost", port=27017)
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
        
    dbh = client["mediaExposureTry"]
    collection = dbh["eyesRolling"]
    
    projection = constructProjectionFileds()
    query = constructQuery()
    
    resultList = list(collection.find( query, projection))
    
    colorUpon = [sensor[colorUponVariable] for sensor in resultList]
    Coordx = [sensor[xCoordVariable] for sensor in resultList]
    Coordy = [sensor[yCoordVariable] for sensor in resultList]
    
    #gazeCoordxnpArray = np.array(gazeCoordx)
    #gazeCoordynpArray = np.array(gazeCoordy)
    
    fig = plt.figure()
    ax = fig.gca() 
    ax.scatter(Coordx, Coordy, c=colorUpon, cmap=cm.seismic)
    ax.legend()
    
    plt.show()