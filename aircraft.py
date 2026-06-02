import matplotlib.pyplot as plt
import math
from airports import *


# Definim la classe i establim les seves característiques
class Aircraft:
  def __init__(self):
      self.id = ""
      self.airline = ""
      self.origin = ""
      self.landing_time = ""


      # Version 4: departure information
      self.destination = ""
      self.departure_time = ""


# Revisa que una hora tingui el format correcte i estigui dins del dia.
def IsValidTime(time_text):
 parts = time_text.split(":")


 if len(parts) != 2:
     return False


 try:
     hour = int(parts[0])
     minute = int(parts[1])
 except:
     return False


 if hour < 0 or hour > 23:
     return False


 if minute < 0 or minute > 59:
     return False


 return True

# Converteix una hora hh:mm en minuts per poder comparar hores fàcilment.
def TimeToMinutes(time):
  parts = time.split(":")
  hours = int(parts[0])
  minutes = int(parts[1])
  return hours * 60 + minutes


# Llegeix el fitxer d’arribades i crea una llista d’Aircraft amb les dades vàlides.
def LoadArrivals(filename):
 aircrafts = []


 try:
     file = open(filename, "r")
 except FileNotFoundError:
     return aircrafts


 line = file.readline()   # llegim la capçalera i la ignorem
 line = file.readline()


 while line != "":
     parts = line.split()


     if len(parts) == 4:
         aircraftid = parts[0]
         origin = parts[1]
         landing_time = parts[2]
         airline = parts[3]


         if IsValidTime(landing_time):
             aircraft = Aircraft()
             aircraft.id = aircraftid
             aircraft.airline = airline
             aircraft.origin = origin
             aircraft.landing_time = landing_time
             aircrafts.append(aircraft)


     line = file.readline()


 file.close()
 return aircrafts


# Llegeix el fitxer de sortides de la V4 i guarda destinació i hora de sortida.
def LoadDepartures(filename):
  departures = []


  try:
      file = open(filename, "r")


      line = file.readline()
      line = file.readline()


      while line != "":
          parts = line.split()


          if len(parts) == 4 and IsValidTime(parts[2]) == True:
              aircraft = Aircraft()
              aircraft.id = parts[0]
              aircraft.destination = parts[1]
              aircraft.departure_time = parts[2]
              aircraft.airline = parts[3]
              departures.append(aircraft)


          line = file.readline()


      file.close()
      return departures, 0


  except FileNotFoundError:
      return departures, -1


# Uneix arribades i sortides del mateix avió per simular el dia complet.
# Si una sortida no té arribada associada, es considera un avió que ja era a LEBL.
def MergeMovements(arrivals, departures):
  movements = []


  if len(arrivals) == 0 or len(departures) == 0:
      return movements, -1


  # Marquem quines sortides ja hem fet servir per no repetir-les en dos avions.
  used_departures = [False] * len(departures)


  i = 0
  while i < len(arrivals):


      # Per cada arribada busquem la primera sortida posterior del mateix avió.
      found = False
      best_position = -1
      best_departure_time = 99999


      j = 0
      while j < len(departures):


          if used_departures[j] == False:


              if arrivals[i].id == departures[j].id:


                  arrival_minutes = TimeToMinutes(arrivals[i].landing_time)
                  departure_minutes = TimeToMinutes(departures[j].departure_time)


                  if arrival_minutes < departure_minutes:


                      if departure_minutes < best_departure_time:
                          best_departure_time = departure_minutes
                          best_position = j
                          found = True


          j = j + 1


      if found == True:
          aircraft = Aircraft()
          aircraft.id = arrivals[i].id
          aircraft.origin = arrivals[i].origin
          aircraft.landing_time = arrivals[i].landing_time
          aircraft.destination = departures[best_position].destination
          aircraft.departure_time = departures[best_position].departure_time
          aircraft.airline = arrivals[i].airline
          movements.append(aircraft)
          used_departures[best_position] = True
      else:
          movements.append(arrivals[i])


      i = i + 1


  # Les sortides que no s’han pogut relacionar amb cap arribada es mantenen com a avions que ja eren a l’aeroport.
  j = 0
  while j < len(departures):
      if used_departures[j] == False:
          movements.append(departures[j])
      j = j + 1


  return movements, 0


# Detecta avions que només surten: són avions que ja eren a l’aeroport de nit.
# Retorna els avions que no arriben durant el dia però sí que surten de LEBL.
def NightAircraft(aircrafts):
  night_aircrafts = []


  if len(aircrafts) == 0:
      return night_aircrafts, -1


  i = 0
  while i < len(aircrafts):
      if aircrafts[i].origin == "" and aircrafts[i].landing_time == "":
          if aircrafts[i].destination != "" and aircrafts[i].departure_time != "":
              night_aircrafts.append(aircrafts[i])
      i = i + 1


  return night_aircrafts, 0


# Genera la gràfica del nombre d’arribades per cada hora del dia.
def PlotArrivals(aircrafts):
 if len(aircrafts) == 0:
     return None


 hours = [0] * 24
 i = 0
 while i < len(aircrafts):
     if aircrafts[i].landing_time != "":
         parts = aircrafts[i].landing_time.split(":")
         hour = int(parts[0])
         hours[hour] = hours[hour] + 1
     i = i + 1


 x = [0] * 24
 i = 0
 while i < 24:
     x[i] = i
     i = i + 1


 fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0F172A")
 ax.set_facecolor("#1E293B")
 ax.bar(x, hours, color="#2563EB", width=0.7)
 ax.set_xlabel("Hour", color="#CBD5E1", fontsize=11)
 ax.set_ylabel("Number of arrivals", color="#CBD5E1", fontsize=11)
 ax.set_title("Landing frequency during the day", color="#F8FAFC", fontsize=14, pad=12)
 ax.tick_params(colors="#CBD5E1")
 ax.grid(color="#334155", alpha=0.5, axis="y")
 for spine in ax.spines.values():
     spine.set_color("#334155")
 i = 0
 while i < 24:
     if hours[i] > 0:
         ax.text(x[i], hours[i] + 0.2, str(hours[i]), ha="center", color="#CBD5E1", fontsize=8)
     i = i + 1
 fig.tight_layout()
 return fig


# Desa la informació dels vols en un fitxer de text.
def SaveFlights(aircrafts, filename):
 if len(aircrafts) == 0:
     return False


 file = open(filename, "w")
 file.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")


 i = 0
 while i < len(aircrafts):
     aircraftid = aircrafts[i].id
     origin = aircrafts[i].origin
     landing_time = aircrafts[i].landing_time
     airline = aircrafts[i].airline


     if aircraftid == "":
         aircraftid = "-"
     if origin == "":
         origin = "-"
     if landing_time == "":
         landing_time = "-"
     if airline == "":
         airline = "-"


     file.write(aircraftid + " " + origin + " " + landing_time + " " + airline + "\n")
     i = i + 1


 file.close()
 return True

# Dibuixa el nombre de vols per aerolínia i agrupa les petites a Others.
def PlotAirlines(aircrafts):
 if len(aircrafts) == 0:
     return None


 airlines = []
 counts = []


 i = 0
 while i < len(aircrafts):
     company = aircrafts[i].airline
     found = False
     j = 0
     while j < len(airlines) and found == False:
         if airlines[j] == company:
             counts[j] = counts[j] + 1
             found = True
         j = j + 1
     if found == False:
         airlines.append(company)
         counts.append(1)
     i = i + 1


 airlines2 = []
 counts2 = []
 others = 0


 i = 0
 while i < len(airlines):
     if counts[i] >= 10:
         airlines2.append(airlines[i])
         counts2.append(counts[i])
     else:
         others = others + counts[i]
     i = i + 1


 if others > 0:
     airlines2.append("Others")
     counts2.append(others)


 palette = ["#2563EB", "#22C55E", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#EC4899", "#10B981"]
 bar_colors = []
 i = 0
 while i < len(airlines2):
     bar_colors.append(palette[i % len(palette)])
     i = i + 1


 fig, ax = plt.subplots(figsize=(11, 5), facecolor="#0F172A")
 ax.set_facecolor("#1E293B")
 ax.bar(airlines2, counts2, color=bar_colors, width=0.65)
 ax.set_xlabel("Airline", color="#CBD5E1", fontsize=11)
 ax.set_ylabel("Number of flights", color="#CBD5E1", fontsize=11)
 ax.set_title("Flights per airline", color="#F8FAFC", fontsize=14, pad=12)
 ax.tick_params(colors="#CBD5E1")
 ax.grid(color="#334155", alpha=0.5, axis="y")
 for spine in ax.spines.values():
     spine.set_color("#334155")
 i = 0
 while i < len(airlines2):
     ax.text(i, counts2[i] + 0.5, str(counts2[i]), ha="center", color="#CBD5E1", fontsize=9)
     i = i + 1
 plt.xticks(rotation=30, ha="right")
 fig.tight_layout()
 return fig

# Compta si les arribades venen d’aeroports Schengen o non-Schengen i ho mostra en una barra apilada.
def PlotFlightsType(aircrafts, airports):
 if len(aircrafts) == 0:
     return None


 schengen = 0
 nonschengen = 0


 i = 0
 while i < len(aircrafts):
     origin_code = aircrafts[i].origin
     found = False
     j = 0
     while j < len(airports) and found == False:
         if airports[j].ICAO == origin_code:
             if airports[j].isSchengen == True:
                 schengen = schengen + 1
             else:
                 nonschengen = nonschengen + 1
             found = True
         j = j + 1
     i = i + 1


 fig, ax = plt.subplots(figsize=(6, 5), facecolor="#0F172A")
 ax.set_facecolor("#1E293B")
 ax.bar(["Arrivals"], [schengen], label="Schengen", color="#22C55E", width=0.5)
 ax.bar(["Arrivals"], [nonschengen], bottom=[schengen], label="Non-Schengen", color="#EF4444", width=0.5)
 ax.set_ylabel("Number of flights", color="#CBD5E1", fontsize=11)
 ax.set_title("Schengen vs Non-Schengen arrivals", color="#F8FAFC", fontsize=14, pad=12)
 ax.tick_params(colors="#CBD5E1")
 ax.grid(color="#334155", alpha=0.5, axis="y")
 for spine in ax.spines.values():
     spine.set_color("#334155")
 if schengen > 0:
     ax.text(0, schengen / 2, str(schengen), ha="center", va="center", color="white", fontsize=12, fontweight="bold")
 if nonschengen > 0:
     ax.text(0, schengen + nonschengen / 2, str(nonschengen), ha="center", va="center", color="white", fontsize=12, fontweight="bold")
 ax.legend(facecolor="#1E293B", labelcolor="#CBD5E1", edgecolor="#334155")
 fig.tight_layout()
 return fig

# Crea un fitxer KML amb les rutes des de l’origen fins a Barcelona.
def MapFlights(aircrafts, airports):
 if len(aircrafts) == 0:
     return


 foundLEBL = False
 i = 0
 while i < len(airports) and foundLEBL == False:
     if airports[i].ICAO == "LEBL":
         lebl_longitude = airports[i].longitude
         lebl_latitude = airports[i].latitude
         foundLEBL = True
     i = i + 1


 if foundLEBL == False:
     return


 file = open("flights.kml", "w")
 file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
 file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
 file.write("<Document>\n")
 file.write("<name>Flights to LEBL</name>\n")


 file.write("<Style id=\"schengenStyle\">\n")
 file.write("<LineStyle>\n")
 file.write("<color>ff00ff00</color>\n")
 file.write("<width>2</width>\n")
 file.write("</LineStyle>\n")
 file.write("</Style>\n")


 file.write("<Style id=\"nonSchengenStyle\">\n")
 file.write("<LineStyle>\n")
 file.write("<color>ff0000ff</color>\n")
 file.write("<width>2</width>\n")
 file.write("</LineStyle>\n")
 file.write("</Style>\n")


 i = 0
 while i < len(aircrafts):
     origin_code = aircrafts[i].origin


     foundAirport = False
     j = 0
     while j < len(airports) and foundAirport == False:
         if airports[j].ICAO == origin_code:
             origin_longitude = airports[j].longitude
             origin_latitude = airports[j].latitude
             origin_schengen = airports[j].isSchengen
             foundAirport = True
         j = j + 1


     if foundAirport == True:
         file.write("<Placemark>\n")
         file.write("<name>" + aircrafts[i].id + "</name>\n")


         if origin_schengen == True:
             file.write("<styleUrl>#schengenStyle</styleUrl>\n")
         else:
             file.write("<styleUrl>#nonSchengenStyle</styleUrl>\n")


         file.write("<LineString>\n")
         file.write("<tessellate>1</tessellate>\n")
         file.write("<coordinates>\n")
         file.write(str(origin_longitude) + "," + str(origin_latitude) + ",0 ")
         file.write(str(lebl_longitude) + "," + str(lebl_latitude) + ",0\n")
         file.write("</coordinates>\n")
         file.write("</LineString>\n")
         file.write("</Placemark>\n")


     i = i + 1


 file.write("</Document>\n")
 file.write("</kml>\n")
 file.close()


# Calcula la distància aproximada entre dos punts de la Terra amb la fórmula de Haversine.
def HaversineDistance(lat1, lon1, lat2, lon2):
 R = 6371.0


 lat1 = math.radians(lat1)
 lon1 = math.radians(lon1)
 lat2 = math.radians(lat2)
 lon2 = math.radians(lon2)


 dlat = lat2 - lat1
 dlon = lon2 - lon1


 a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) * math.sin(dlon / 2)
 c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


 distance = R * c
 return distance

# Selecciona els vols que venen de més de 2000 km de distància.
def LongDistanceArrivals(aircrafts, airports):
 longdistance = []


 foundLEBL = False
 i = 0
 while i < len(airports) and foundLEBL == False:
     if airports[i].ICAO == "LEBL":
         lebl_latitude = airports[i].latitude
         lebl_longitude = airports[i].longitude
         foundLEBL = True
     i = i + 1


 if foundLEBL == False:
     return longdistance


 i = 0
 while i < len(aircrafts):
     origin_code = aircrafts[i].origin


     foundAirport = False
     j = 0
     while j < len(airports) and foundAirport == False:
         if airports[j].ICAO == origin_code:
             origin_latitude = airports[j].latitude
             origin_longitude = airports[j].longitude
             foundAirport = True
         j = j + 1


     if foundAirport == True:
         distance = HaversineDistance(origin_latitude, origin_longitude, lebl_latitude, lebl_longitude)
         if distance > 2000:
             longdistance.append(aircrafts[i])


     i = i + 1


 return longdistance

# Funcionalitat extra: estima emissions segons distància i tipus de trajecte.
def CalculateEmissions(aircrafts, airports):
 lebl_lat = None
 lebl_lon = None
 i = 0
 while i < len(airports):
     if airports[i].ICAO == "LEBL":
         lebl_lat = airports[i].latitude
         lebl_lon = airports[i].longitude
     i = i + 1


 if lebl_lat is None:
     return None


 total_flights = 0
 total_distance = 0.0
 total_co2 = 0.0
 short_count = 0
 medium_count = 0
 long_count = 0


 i = 0
 while i < len(aircrafts):
     ac = aircrafts[i]


     if ac.origin != "" and ac.landing_time != "":
         found = False
         j = 0
         while j < len(airports) and found == False:
             if airports[j].ICAO == ac.origin:
                 dist = HaversineDistance(airports[j].latitude, airports[j].longitude, lebl_lat, lebl_lon)
                 if dist < 1500:
                     co2 = dist * 12.0
                     short_count = short_count + 1
                 elif dist < 4000:
                     co2 = dist * 16.0
                     medium_count = medium_count + 1
                 else:
                     co2 = dist * 22.0
                     long_count = long_count + 1
                 total_distance = total_distance + dist
                 total_co2 = total_co2 + co2
                 total_flights = total_flights + 1
                 found = True
             j = j + 1


     i = i + 1


 if total_flights == 0:
     return None


 result = {}
 result['total_flights'] = total_flights
 result['total_co2_tons'] = total_co2 / 1000.0
 result['avg_co2_kg'] = total_co2 / total_flights
 result['avg_distance_km'] = total_distance / total_flights
 result['total_distance_km'] = total_distance
 result['short_haul'] = short_count
 result['medium_haul'] = medium_count
 result['long_haul'] = long_count
 return result


# TEST
if __name__ == "__main__":

    airports = LoadAirports("Airports.txt")

    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1

    aircrafts = LoadArrivals("Arrivals.txt")

    print("Flights loaded:", len(aircrafts))

    PlotArrivals(aircrafts)
    SaveFlights(aircrafts, "output_arrivals.txt")
    PlotAirlines(aircrafts)
    PlotFlightsType(aircrafts, airports)
    MapFlights(aircrafts, airports)

    longdistance = LongDistanceArrivals(aircrafts, airports)

    print("Long distance flights:", len(longdistance))

    print("----- TEST LoadDepartures -----")

    departures, error = LoadDepartures("Departures.txt")

    print("Error code:", error)
    print("Departures loaded:", len(departures))

    i = 0
    while i < len(departures) and i < 6:
        print(
            departures[i].id,
            departures[i].destination,
            departures[i].departure_time,
            departures[i].airline
        )
        i = i + 1

    print("----- TEST MergeMovements -----")

    arrivals = LoadArrivals("Arrivals.txt")
    departures, error_dep = LoadDepartures("Departures.txt")

    movements, error = MergeMovements(arrivals, departures)

    print("Error code:", error)
    print("Movements:", len(movements))

    i = 0
    while i < len(movements) and i < 10:
        print(
            movements[i].id,
            movements[i].origin,
            movements[i].landing_time,
            movements[i].destination,
            movements[i].departure_time,
            movements[i].airline
        )
        i = i + 1

    print("----- TEST NightAircraft -----")

    night, error = NightAircraft(movements)

    print("Error code:", error)
    print("Night aircraft:", len(night))

    i = 0
    while i < len(night) and i < 10:
        print(
            night[i].id,
            night[i].destination,
            night[i].departure_time,
            night[i].airline
        )

        i = i + 1

    airports = LoadAirports("Airports.txt")

    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1

    aircrafts = LoadArrivals("Arrivals.txt")
    print("Flights loaded:", len(aircrafts))

    departures, error = LoadDepartures("Departures.txt")
    movements, error = MergeMovements(aircrafts, departures)
    print("Movements:", len(movements))

    emissions = CalculateEmissions(movements, airports)
    if emissions is not None:
        print("Avg CO2 per flight:", int(emissions['avg_co2_kg']), "kg")
