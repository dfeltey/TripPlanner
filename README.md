TripPlanner
===========

A python based public transit app for planning bus travel in Anchorage Alaska.

TODO:
    - Implement a caching system so that things won't break when the live data
      is updating, and returns data that isn't parsed correctly.
    - In the same vein as above, implement exception handling so that when 
      things do break, they do so in a controlled manner.
    - Implement a graph-based structure containing bus stops based on the 
      route information and distance between each pair of stops. It should 
      then be possible to perform an A* search on this structure.    