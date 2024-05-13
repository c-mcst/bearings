"""

Copyright (c) 2024 c-mcst

License: BSD 3-Clause License. See LICENSE at root of original repository.

This is a pure Python implementation of some classes and functions intended to 
calculate intersections between bearing lines. The main _intersect function is 
adapted from: https://www.edwilliams.org/avform147.htm#Intersection.
Also available at:
https://web.archive.org/web/20240119032952/https://www.edwilliams.org/avform147.htm#Intersection


Calculations performed by this code use a spherical approximation of the 
earth (great circle) and have all the known issues of great circle geospatial
approximations (and probably some other issues, too).

"""
from __future__ import annotations
import math
from typing import Union


from bearings._safe_math import euclidean_modulo, asin_safe, acos_safe
from bearings._errors import (IdenticalInputPointError, 
                              ProbableDivergenceError,
                              AmbiguousIntersectionError,
                              InfiniteIntersectionError)
from bearings.point import Point


# the main bearing line class
class BearingLine:
    def __init__(self, latitude, longitude, bearing, declination=0):
        self.latitude = latitude
        self.longitude = longitude
        self.latitude_radians = self._lat_to_radians()
        self.longitude_radians = self._lon_to_radians()
        self.bearing = bearing
        self.declination = declination
        self.true_bearing = self._bearing_to_true_bearing()
        self.true_bearing_radians = self._true_bearing_to_radians()

    
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('Latitude must be of int or float types and in decimal degrees.')
        elif not -90 <= value <= 90:
            raise ValueError('Latitude must be between -90 and 90 degrees.')
        else:
            self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('Longitude must be of int or float types and in decimal degrees.')
        elif not -180 <= value <= 180:
            raise ValueError('Longitude must be between -180 and 180 degrees.')
        else:
            self._longitude = value


    @property
    def bearing(self):
        return self._bearing

    @bearing.setter
    def bearing(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('Bearing must be of int or float types and in degrees.')
        elif not 0 <= value <= 360:
            raise ValueError('Bearing must be between 0 and 360 degrees.')
        else:
            self._bearing = value

    @property
    def declination(self):
        return self._declination

    @declination.setter
    def declination(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('Declination must be of int or float types and in degrees.')
        elif not -180 <= value <= 180:
            raise ValueError('Declination must be between -180 and 180 degrees (it should probably be a lot smaller).')
        else:
            self._declination = value


    def _bearing_to_true_bearing(self):
        return self.bearing + self.declination
        
    def _true_bearing_to_radians(self):
        return math.radians(self.true_bearing)

    def _lat_to_radians(self):
        return math.radians(self.latitude)

    def _lon_to_radians(self):
        return math.radians(self.longitude)
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"""{class_name}(latitude={self.latitude}, longitude={self.longitude}, 
        bearing={self.bearing}, declination={self.declination})"""

    def __str__(self):
        return f"BearingLine: ({self.latitude}, {self.longitude}) at {self.declination}° true"

    def get_haversine_distance(self, 
                           lat2: Union[float, int] = None, 
                           lon2: Union[float, int] = None, 
                           other: BearingLine = None):
        """
        Calculate the haversine distance between base point of bearing line 
        and either root point of anotherbearing line or a different point 
        specified by latitude and longitude.

        Args:
            - lat2: the latitude of the other point to measure distance to (if not passing another BearingLine in 'other')
            - lon2: the longitude of the other point to measure distance to (if not passing another BearingLine in 'other')
            - other: another BearingLine to measure distance to root point of

        Returns:
            - the haversine distance between the root point of this BearingLine and either the root point of the other BearingLine or
              the specified other point
        """
        if other is None and not all([lat2==None, lon2==None]):
            if not all([isinstance(x, (float, int)) for x in [lat2, lon2]]):
                raise TypeError('Latitude and longitude must be of int or float types and in decimal degrees.')
            elif not all([-90 <= lat2 <= 90, -180 <= lon2 <= 180]):
                raise ValueError('Check input values. Latitude must be between -90 and 90 degrees, and longitude must be between -180 and 180 degrees.')
            else:
                # set values, converting to radians
                lat1 = self.latitude_radians
                lon1 = self.longitude_radians
                lat2 = math.radians(lat2)
                lon2 = math.radians(lon2)
  
        elif other is not None and all([lat2==None, lon2==None]):
            if not isinstance(other, BearingLine):
                raise TypeError("'other' must be of type BearingLine.")
            else:
                # don't need to do type or value checking here because it's done by the class already
                # set values, using ones with radians
                lat1 = self.latitude_radians
                lon1 = self.longitude_radians
                lat2 = other.latitude_radians
                lon2 = other.longitude_radians

        elif all([other==None, lat2==None, lon2==None]):
            raise SyntaxError("No arguments provided. Enter either a lat and lon or another BearingLine")
        
        elif all([other!=None, lat2!=None, lon2!=None]):
            raise SyntaxError("Too many arguments. Enter either lat and lon or another BearingLine, not both.")

        # approx. radius of earth in km
        radius = 6371
        
        # implementing haversine formula
        # calculate h
        h = (math.sin((lat2-lat1)/2)**2) + (math.cos(lat1) * math.cos(lat2) * (math.sin((lon2-lon1)/2)**2))
        # h can't be greater than 1 (this happens due to rounding error sometimes)
        h = min(1, h)
        # calculate the distance using h
        distance = 2 * radius * math.asin(math.sqrt(h))
        return distance

    def _intersect(self, other: BearingLine, suppress_errors: bool = False):
        """
        Given two BearingLines, return their intersection, if it exists. 

        Args:
            - other: The other BearingLine with which to compute the intersection
            - suppress_errors: Whether to suppress errors that occur during caculation and return None instead.

        Returns:
            - either a tuple containing (latitude, longitude) of the intersection, or None, depending on your suppression choices
        """
        # type check 'other' and the rest of the inputs
        if not isinstance(other, BearingLine):
            raise TypeError("'other' must be of type BearingLine.")
        elif not isinstance(suppress_errors, bool):
            raise TypeError("'suppress_errors' must be of type bool (True or False)")
        
        # set the input values
        # this formula was made with west longitudes being positive (ugh), so flip the sign of the input longitudes
        # to align with convention
        lat1 = self.latitude_radians
        lon1 = -self.longitude_radians
        crs13 = self.true_bearing_radians
        lat2 = other.latitude_radians
        lon2 = -other.longitude_radians
        crs23 = other.true_bearing_radians
    
        # make sure the two points aren't identical
        if all([lat1==lat2, lon1==lon2]):
            if not suppress_errors:
                raise IdenticalInputPointError("""Root points of both input BearingLines 
                                               are identical. Calculation cannot be performed 
                                               (you're already at the intersection!)""")
            elif suppress_errors:
                return None
    
        # do the calculation
    
        # compute the distance between the two input points
        dst12=2*asin_safe(math.sqrt((math.sin((lat1-lat2)/2))**2+math.cos(lat1)*math.cos(lat2)*math.sin((lon1-lon2)/2)**2))
    
        # figure out which point is on which side
        if math.sin(lon2-lon1)<0:
            crs12=acos_safe((math.sin(lat2)-math.sin(lat1)*math.cos(dst12))/(math.sin(dst12)*math.cos(lat1)))
            crs21=2.*math.pi-acos_safe((math.sin(lat1)-math.sin(lat2)*math.cos(dst12))/(math.sin(dst12)*math.cos(lat2)))
        else:
            crs12=2.*math.pi-acos_safe((math.sin(lat2)-math.sin(lat1)*math.cos(dst12))/(math.sin(dst12)*math.cos(lat1)))
            crs21=acos_safe((math.sin(lat1)-math.sin(lat2)*math.cos(dst12))/(math.sin(dst12)*math.cos(lat2)))
    
        # find the angles between the line between our bearing lines and the line between the input points
        ang1=euclidean_modulo(crs13-crs12+math.pi,2.*math.pi)-math.pi
        ang2=euclidean_modulo(crs21-crs23+math.pi,2.*math.pi)-math.pi
    
        # figure out if there are either infinite or ambiguous intersections
        if (math.sin(ang1)==0 and math.sin(ang2)==0):
            # infinity of intersections
            if not suppress_errors:
                raise InfiniteIntersectionError('Infinite intersections. Are the lines on top of each other?')
            else:
                return None
            
        elif math.sin(ang1)*math.sin(ang2)<0:
            # ambiguous
            if not suppress_errors:
                raise AmbiguousIntersectionError('Ambiguous intersection. Are the lines parallel and never crossing?')
            else:
                return None
        else:
            # set the three angles of the spherical triangle
            ang1=abs(ang1)
            ang2=abs(ang2)
            ang3=acos_safe(-math.cos(ang1)*math.cos(ang2)+math.sin(ang1)*math.sin(ang2)*math.cos(dst12)) 
    
            # using the values so far calculated, determine latitude and longitude of intersection
            dst13=math.atan2(math.sin(dst12)*math.sin(ang1)*math.sin(ang2),math.cos(ang2)+math.cos(ang1)*math.cos(ang3))
            lat3=asin_safe(math.sin(lat1)*math.cos(dst13)+math.cos(lat1)*math.sin(dst13)*math.cos(crs13))
            dlon=math.atan2(math.sin(crs13)*math.sin(dst13)*math.cos(lat1),math.cos(dst13)-math.sin(lat1)*math.sin(lat3))
            lon3=euclidean_modulo(lon1-dlon+math.pi,2*math.pi)-math.pi
    
            # this formula was designed with west longitudes being positive (ugh), so flip the sign at output
            intersect = (round(math.degrees(lat3), 5), round(math.degrees(-lon3), 5))

            return intersect
        
    
    def get_intersect(self, 
                      other: BearingLine, 
                      warn_probable_divergence: bool = True, 
                      suppress_probable_divergence: bool = False, 
                      suppress_greater_than: Union[int, float] = None, 
                      ignore_errors: bool = False):
        """
        Given two BearingLines, calculate their intersection (if it exists), and return either
        the intersection or None depending on behavior set in input variables.

        Args:
            - other: The other BearingLine with which to compute the intersection
            - warn_probable_divergence: Whether to raise an error if the lines probably 
                diverge, or just return None.
            - suppress_probable_divergence: Whether to return None when lines probably 
                diverge, rather than the very far away intersection.
            - suppress_greater_than: A max value (in kilometers) for the distance 
                from any one input point to the intersection. Return None if 
                intersection is farther than this value from either input point.
            - ignore_errors: Whether to suppress errors that occur during caculation 
                and return None instead.

        Returns:
            - either a tuple containing (latitude, longitude) of the intersection 
                or None, depending on your suppression choices
        """
        # check inputs
        if not isinstance(warn_probable_divergence, bool):
            raise TypeError("'warn_probable_divergence' must be of type bool (True or False)")
        elif not isinstance(suppress_probable_divergence, bool):
            raise TypeError("'suppress_probable_divergence' must be of type bool (True or False)")
        elif not isinstance(suppress_greater_than, (float, int, type(None))):
            raise TypeError("'suppress_greater_than' must be of type float or int")
        
        # get the intersection
        intersection = self._intersect(other, suppress_errors=ignore_errors)

        # if no need to warn or suppress based on length, return intersection point
        if not any([warn_probable_divergence, suppress_probable_divergence, suppress_greater_than]):
            return intersection
        
        elif intersection is None:
            return None
        else:
            # do the distance calculations
            this_point_to_intersect = self.get_haversine_distance(*intersection)
            other_point_to_intersect = other.get_haversine_distance(*intersection)
            this_point_to_other = self.get_haversine_distance(other=other)
            max_point_to_intersect = max(this_point_to_intersect, other_point_to_intersect)

            if suppress_greater_than is not None and max_point_to_intersect > suppress_greater_than:
                return None
            
            # check for possible divergence conditions
            elif all([this_point_to_intersect > 10000, other_point_to_intersect > 10000, this_point_to_other < 10000]):
                if suppress_probable_divergence:
                    return None
                    
                elif warn_probable_divergence:
                    raise ProbableDivergenceError("""Lines probably diverge (i.e., intersection is 
                                                  more than about 1/4 an earth circumference away from 
                                                  both input points). Check input values.""")
                
            
            
            # return Point with latitude and longitude of intersection
            return Point(intersection[0], intersection[1])