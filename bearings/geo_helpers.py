"""

Copyright (c) 2024 c-mcst

License: BSD 3-Clause License. See LICENSE at root of original repository.

These are helper functions to do useful calculations with some of the classes
in this library.

"""

from bearings.point import Point
from bearings._errors import AmbiguousBoxError
from typing import Union
import math

def bounding_box(point_list: Union[list, tuple]):
    """
    Return the minimum bounding box around all Points in a list or tuple of Points
    
    Args:
        - point_list: a list or tuple of Points
        
    Returns:
        - the minimum bounding box around all Points as a tuple of
            (min_lon, max_lon, min_lat, max_lat)
    """

    if not isinstance(point_list, (list, tuple)):
        raise TypeError('point_list must be of type list or tuple.')
    elif not all([isinstance(x, Point) for x in point_list]):
        raise TypeError('All points in point_list must be of Point type.')
    else:
        latitudes = [point.latitude for point in point_list]
        longitudes = [point.longitude for point in point_list]
        min_lon = min(longitudes)
        max_lon = max(longitudes)
        min_lat = min(latitudes)
        max_lat = max(latitudes)

        if any([min_lon==max_lon, min_lat==max_lat]):
            raise AmbiguousBoxError('''Bounding box ambiguous. Check that not 
                                    all inputs have the same min and max lat or lon.''')
        
        else:
            return (min_lon, max_lon, min_lat, max_lat)
        

def haversine_distance(point_1: Point, 
                       point_2: Point):
    """
    Calculate the haversine distance between base point of bearing line 
    and either root point of anotherbearing line or a different point 
    specified by latitude and longitude.

    Args:
        - point_1: a Point
        - point_2: a Point

    Returns:
        - the haversine distance between the two input points
    """
    if not all([isinstance(point_1, Point), isinstance(point_2, Point)]):
        raise TypeError("Both input points must be of type Point.")
    
    else:
        lat1 = math.radians(point_1.latitude)
        lon1 = math.radians(point_1.longitude)
        lat2 = math.radians(point_2.latitude)
        lon2 = math.radians(point_2.longitude)

    # approx. radius of earth in km
    radius = 6371
    
    # implementing haversine formula
    # calculate h
    h = (math.sin((lat2-lat1)/2)**2) + (math.cos(lat1) * math.cos(lat2) * (math.sin((lon2-lon1)/2)**2))
    # h can't be greater than 1 (this happens due to rounding error sometimes)
    h = min(1, h)
    # calculate the distance using h
    distance = round(2 * radius * math.asin(math.sqrt(h)), 4)
    return distance