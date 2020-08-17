''' 
    Mission flying algorithim:
        This is the most complete visualization tool as of now.
        The script is able to parse and display the mission but
        ther is not a planning algorithim being excuted.
'''
import sys
sys.path.append('C:/Users/santi/Desktop/Projects/path_planner/map_loader')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from loader import Loader
import numpy as np
import math
import json
import os


def main():
    mission = Loader('C:/Users/santi/Desktop/Projects/path_planner/maps/mission_map.json')

    wayPoints = mission.waypoints()
    boundary = mission.boundary()
    obstacles = mission.obstacles()


    xCoords, yCoords, radiuses = projectObstacles(obstacles)
    plotObstacles(xCoords, yCoords, radiuses)

    xCoords, yCoords = projectCoord(wayPoints)
#    adjustCoordinates(wayPoints, obstacles)
    plotWayPoints(xCoords, yCoords)
 

    xCoords, yCoords = projectCoord(boundary)
    plotBoundary(xCoords, yCoords)

    plt.show()




# Based on the abstocles aroun the mission,
# adjust waypoint coordinates to avoid them.
def adjustCoordinates(wayPoints, obstacles):
    xList, yList = projectCoord(wayPoints)

    # analyze each line segment of the map and determine 
    # if this intersects and obstacle
    for i in range(len(xList)-1):
        p1 = [xList[i], yList[i]]
        p2 = [xList[i+1], yList[i+1]]

        if(intersectsObstacle(p1, p2, obstacles)):
            print(" line intersects an obstacle x: %s  y: %s" % (p1,p2))
        else:
            print("x: %s  y: %s does not intercet any obstacle" % (p1,p2))
    

#def intersectsObstacle(p1, p2, obstacles):


# Plot wayPoints and boundaryPoints
def plotBoundary(xCoords, yCoords):
    plt.plot(xCoords, yCoords)
    plt.grid(True)
    plt.axis("equal")

def plotWayPoints(xCoords, yCoords):
    plt.plot(xCoords, yCoords)
    plt.grid(True)
    plt.axis("equal")


# Plot obstacles 
def plotObstacles(xCoords, yCoords, radiuses):
    fig, ax = plt.subplots()

    for i in range(len(xCoords)):
        circle = plt.Circle((xCoords[i],yCoords[i]), radiuses[i])
        ax.set_aspect(1)
        ax.add_artist(circle)
     



def projectCoord(list):
    m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
    xCoords = []
    yCoords = []

    for item in list:
        lat = item["latitude"]
        lon = item["longitude"]
        xpt,ypt = m(lon,lat)
        xCoords.append(xpt - 8641750)
        yCoords.append(ypt - 3725600)
    return xCoords, yCoords


def projectObstacles(list):
    m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
    xCoords = []
    yCoords = []
    radiuses = []
 
    for item in list:
        lat = item["latitude"]
        lon = item["longitude"]
        radius = item["radius"]
        xpt,ypt = m(lon, lat)
        xCoords.append(xpt - 8641750)
        yCoords.append(ypt - 3725600)
        radiuses.append(radius/3)
    return xCoords, yCoords, radiuses



if __name__ == '__main__':
    main()
