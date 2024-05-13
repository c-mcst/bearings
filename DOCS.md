# The BearingLine class:
## Constructor
`bearings.BearingLine(latitude, longitude, bearing, declination=0)`
|Parameter|Description|
|---|---|
|`latitude`|A latitude in decimal degrees. `float` or `int` type.|
|`longitude`|A longitude in decimal degrees.`float` or `int` type.|
|`bearing`|A bearing, either magnetic or true, in degrees from north. `float` or `int` type.|
|`declination`|If bearing is magnetic and requires correction, a declination adjustment. `float` or `int` type. Per convention, east declinations are positive and west are negative.|


<br>

## Attributes
|Attribute|Description|
|---|---|
|`BearingLine.latitude`|The latitude of the starting point of the BearingLine object in decimal degrees.|
|`BearingLine.longitude`|The longitude of the starting point of the BearingLine object in decimal degrees.|
|`BearingLine.latitude_radians`|The latitude of the starting point of the BearingLine object converted to radians.|
|`BearingLine.longitude_radians`|The longitude of the starting point of the BearingLine object converted to radians.|
|`BearingLine.bearing`|The bearing of the BearingLine object in degrees from north.|
|`BearingLine.declination`|The declination (offset from magnetic north) of the bearing. Optional, and defaults to 0, which assumes true bearings.|
|`BearingLine.true_bearing`|The bearing adjusted to true north using the declination.|
|`BearingLine.true_bearing_radians`|The true bearing converted to radians.|


<br>

## Instance Methods

### Haversine distance
`BearingLine.get_haversine_distance(lat2=None, lon2=None, other=None)`


|Argument|Description|
|---|---|
|`lat2`|A latitude in decimal degrees. `float` or `int` type.|
|`lon2`|A longitude in decimal degrees.`float` or `int` type.|
|`other`|A `BearingLine`|

<br>

If `lat2` and `lon2` provided, returns the haversine (great circle) distance between the starting point of the BearingLine and the provided point. If `other` (another `BearingLine`) provided, returns the haversine distance between starting point of both `BearingLine`s

<br>

### Intersection

`BearingLine.get_intersect(other, warn_probable_divergence=True, suppress_probable_divergence=False, suppress_greater_than=None, ignore_errors=False)`

|Argument|Description|
|---|---|
|`other`|Another `BearingLine` with which to calculate the intersection.|
|`warn_probable_divergence`|`bool` indicating whether to raise an error if the two bearing lines most likely diverge. Determined by checking if intersection is more than approx. 1/4 the circumerence of earth from both starting points, and both starting points aren't themseves more than 1/4 earth circumference apart. Default `True`. Divergence detection is a work in progress.|
|`suppress_probable_divergence`|`bool` indicating whether to suppress outputs (return `None`) where a likely divergence is detected. Mutually exclusive with `warn_probable_divergence`, and will take precedence if both are `True`. Default `False`.|
|`suppress_greater_than`|`int` or `float` indicating whether to suppress outputs (return `None`) where the intersection is more than `suppress_greater_than` kilometers from the starting point of either BearingLine. Useful, for example, if you want to automatically run a bunch of pairwise intersections in a constrained area but only want to keep results within that same general area. Default `None`.|
|`ignore_errors`|`bool` indicating whether to return `None` instead of raising errors that arise in the underlying intersection calculation, such as lines that are parallel (never intersect) or on top of each other (infinitely intersect). Again, useful if you want to automatically run a ton of intersections and simply ignore invalid ones.|

<br>

Given another `BearingLine`, returns either a `Point` representing the intersection of the two bearing lines, or `None`, depending on whether the output meets certain of the suppression criteria above. Note that suppressing certain errors will mean you get no indication if you are asking the library to compute invalid intersections. This is only desirable behavior in specific circumstances.


<br><br>

# The Point class:

## Constructor
`bearings.Point(latitude, longitude)`
|Parameters|Description|
|---|---|
|`latitude`|A latitude in decimal degrees. `float` or `int` type.|
|`longitude`|A longitude in decimal degrees.`float` or `int` type.|


<br>

## Attributes
|Attribute|Description|
|---|---|
|`Point.latitude`|The latitude of the starting point of the BearingLine object in decimal degrees.|
|`Point.longitude`|The longitude of the starting point of the BearingLine object in decimal degrees.|


<br>

## Instance Methods
None yet



<br><br>

# Functions
## Various geographic helpers

### Haversine distance

`bearings.haversine_distance(point_1, point_2)`


|Argument|Description|
|---|---|
|`point_1`|A `Point` from which to measure distance to `point_2`|
|`point_2`|A `Point` from which to measure distance to `point_1`|

<br>

Given two `Point`s, return the haversine distance between them in kilometers. 


<br>

### Bounding box

`bearings.bounding_box(point_list = [Point, Point, ... , Point])`

|Argument|Description|
|---|---|
|`point_list`|A `list` or `tuple` of `Point`s around which to calculate a minimum bounding box|

<br>

Given a list or tuple of `Point`s, return the smallest box that encompasses all points. Format is `(<minimum longitude>, <maximum longitude>, <minimum latitude>, <maximum latitude>)`, aka `(xmin, xmax, ymin, ymax)`.
