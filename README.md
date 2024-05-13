# bearings: Python tools for working with bearing lines

## What is it?

A hobby project. Proceed with caution.

This is a small, pure-Python (no dependencies, only uses standard library) package intended for working with bearing or azimuth lines (lines defined by a latitude, longitude, and azimuth in degrees from north). It uses great circle mathematical formulas, which means the earth is approximated as a sphere. It implements some formulas described in Ed Williams' [aviation formulary](https://www.edwilliams.org/avform147.htm).

The earth is not a sphere, and great circle calculations have known inaccuracies. Consider a tool like [geographiclib](https://geographiclib.sourceforge.io/) where super high accuracy matters.

<br>

## What can it do?

Currently, two main things:

  1. Given two bearing lines, defined by a latitude, longitude, azimuth, and optional declination, calculate approximately where they intersect (assuming they do).
  2. Given a bunch of intersection points (or user-defined points), figure out the minimum bounding box around those points (smallest rectangle that encompasses all points).

There are several options for either suppressing or raising errors on certain kinds of output (e.g., lines that probably diverge). I tried to choose sensible defaults, but have a look at the documentation for more detail.

<br>

## License
BSD 3-Clause License. See [LICENSE](https://github.com/c-mcst/bearings/blob/main/LICENSE).

<br>

## Installation

### Directly from github:

```shell
pip install git+https://github.com/c-mcst/bearings
```

### By cloning to your computer:

Clone the repository:
```shell
git clone https://github.com/c-mcst/bearings
```

Navigate to the directory where the cloned repo is and install it with `pip` (you can also do this offline):
```shell
pip install ./bearings
```

<br>

## A couple of examples

### What's up with that mountain?
You're on vacation and you see a really nice mountain in the distance, but you don't know what it's called. From a couple different angles, you take out your compass and sight a bearing to it. You have a declination corrected compass, so you don't have to worry about adding declination in the code. You enter your location and the bearing as below:

```python
>>> import bearings

>>> bearing_1 = bearings.BearingLine(37.86203, -119.43397, 122.9)

>>> bearing_2 = bearings.BearingLine(37.87366, -119.38145, 216.5)

>>> intersect = bearing_1.get_intersect(bearing_2)

>>> print(intersect)
(37.84765, -119.40582)
```

`37.84765, -119.40582` is the intersection of your two lines. When you plot this on a map, you may be able to identify the cool rock you saw. 


### Fireworks
You and several friends can all see some fireworks from your respective houses, but none of you knows where exactly they are. Everyone sends photos in the group chat. You check out the photo metadata and find that the latitude, longitude, and azimuth is recorded in every photo. You've got 5 such photos. 

You decide to calculate the pairwise intersection of all the photos and then get a bounding box around them so you can tell your friends where the fireworks are. Additionally, you want to make sure there aren't intersections way outside of your area caused by two lines pointing almost directly at each other, so you suppress any intersections more than 50km from any of the input points.

```python
>>> from bearings import BearingLine, bounding_box

>>> from itertools import combinations

>>> bearing_1 = BearingLine(41.76414, -70.49841, 187.2)

>>> bearing_2 = BearingLine(41.62724, -70.92775, 121.1)

>>> # this phone measures magnetic azimuth, so we adjust for declination

>>> bearing_3 = BearingLine(41.55812, -70.59693, 177.4, -14.1)

>>> bearing_4 = BearingLine(41.45129, -70.61861, 78.7)

>>> bearing_5 = BearingLine(41.64132, -70.23491, 233.7)

>>> lines = [bearing_1, bearing_2, bearing_3, bearing_4, bearing_5]

>>> pairs = list(combinations(lines, 2))

>>> intersections = [bearing.get_intersect(other_bearing, suppress_greater_than=50)\
...                  for bearing, other_bearing in pairs]

>>> [(x.latitude, x.longitude) for x in intersections if x is not None]
[(41.456, -70.55035), (41.44594, -70.55203), (41.46163, -70.5494), 
(41.46841, -70.54827), (41.45918, -70.55733), (41.46014, -70.55942), 
(41.46108, -70.56148), (41.46038, -70.5578), (41.46262, -70.5587), 
(41.45937, -70.56457)]

>>> bounding_box(intersections)
(-70.56457, -70.54827, 41.44594, 41.46841)

```

This box, which represents `(<minimum longitude>, <maximum longitude>, <minimum latitude>, <maximum latitude>)`, aka `(xmin, xmax, ymin, ymax)`, places a bounding box around the intersections of all the points. You've narrowed the location of the fireworks to a rectangle of a little over a square mile using a few phone photos. You tell your friends and they finally realize that you're the coolest one in the friend group.

<br>

## Documentation
See [DOCS.md](https://github.com/c-mcst/bearings/blob/main/DOCS.md)
