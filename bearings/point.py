"""

Copyright (c) 2024 c-mcst

License: BSD 3-Clause License. See LICENSE at root of original repository.

A class for describing points on the earth using latitude and longitude.

"""

from typing import Union

class Point:
    def __init__(self, 
                 latitude: Union[float, int], 
                 longitude: Union[float, int]):
        self.latitude = latitude
        self.longitude = longitude

    
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

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.latitude}, {self.longitude})"

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"