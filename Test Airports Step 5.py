from airports import *

airports = LoadAirports("Airports.txt")

i = 0
while i < len(airports):
    SetSchengen(airports[i])
    i = i + 1

PlotAirports(airports)

from airports import *

airports = LoadAirports("Airports.txt")

i = 0
while i < len(airports):
    SetSchengen(airports[i])
    i = i + 1

MapAirports(airports)
print("KML creat")