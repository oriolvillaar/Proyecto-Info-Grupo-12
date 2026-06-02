#Definim la classe i establim les seves característiques
class Airport:
  def __init__(self, ICAO, lat, lng):
      self.ICAO = ICAO
      self.latitude = lat
      self.longitude = lng
      self.isSchengen = False


# Determina si un aeroport és Schengen a partir dels dos primers caràcters ICAO.
def IsSchengenAirport(airport):
  if airport.ICAO == "":
      airport.isSchengen = False #Si introduïm un codi buit el considerem No Schengen
  else:
      prefijo = airport.ICAO[:2] #Establum que el prefeix que determina si és o no Schengen són els dos primers caràcters


      if prefijo == 'LO':
          airport.isSchengen = True


      elif prefijo == 'EB':
          airport.isSchengen = True


      elif prefijo == 'LK':
          airport.isSchengen = True


      elif prefijo == 'LC':
          airport.isSchengen = True


      elif prefijo == 'EK':
          airport.isSchengen = True


      elif prefijo == 'EE':
          airport.isSchengen = True


      elif prefijo == 'EF':
          airport.isSchengen = True


      elif prefijo == 'LF':
          airport.isSchengen = True


      elif prefijo == 'ED':
          airport.isSchengen = True


      elif prefijo == 'LG':
          airport.isSchengen = True


      elif prefijo == 'EH':
          airport.isSchengen = True


      elif prefijo == 'LH':
          airport.isSchengen = True


      elif prefijo == 'BI':
          airport.isSchengen = True


      elif prefijo == 'LI':
          airport.isSchengen = True


      elif prefijo == 'EV':
          airport.isSchengen = True


      elif prefijo == 'EY':
          airport.isSchengen = True


      elif prefijo == 'EL':
          airport.isSchengen = True


      elif prefijo == 'LM':
          airport.isSchengen = True


      elif prefijo == 'EN':
          airport.isSchengen = True


      elif prefijo == 'EP':
          airport.isSchengen = True


      elif prefijo == 'LP':
          airport.isSchengen = True


      elif prefijo == 'LZ':
          airport.isSchengen = True


      elif prefijo == 'LJ':
          airport.isSchengen = True


      elif prefijo == 'LE':
          airport.isSchengen = True


      elif prefijo == 'ES':
          airport.isSchengen = True


      elif prefijo == 'LS':
          airport.isSchengen = True


      else:
          airport.isSchengen = False


#Apliquem la característica de Schengen als codis que compleixin la condició
def SetSchengen(airport):
  IsSchengenAirport(airport)


#Imprimim les dades de cada aeroport
def PrintAirport(airport):
  print("ICAO:", airport.ICAO)
  print("Latitude:", airport.latitude)
  print("Longitude:", airport.longitude)
  print("Schengen:", airport.isSchengen)


# Carrega aeroports des d’un fitxer i converteix coordenades DMS a graus decimals.
def LoadAirports(filename):
  airports = [] #Creem una llista buida on anirem posant les dades que llegim


  try:
      file = open(filename, "r")
  except FileNotFoundError:
      return airports #Si no trobem el fitxer retorna una llista buida


  line = file.readline()   # Llegir la capçalera del fitxer ignorar-la
#Continuem llegint linía per línia
  line = file.readline()
  while line != "":
      parts = line.split() #Separem el tipus de dada del fitxer separades per espais


      codigo = parts[0] #Assignem cada tipus de dada a cada tros de la línia del fitxer separat per espais
      lat_text = parts[1]
      lng_text = parts[2]
#Convertim el contingut de les parts de coordenades a graus
      if lat_text[0] == "N" or lat_text[0] == "S":
          grados = int(lat_text[1:3])
          minutos = int(lat_text[3:5])
          segundos = int(lat_text[5:7])
          lat = grados + minutos / 60 + segundos / 3600
          if lat_text[0] == 'S':
              lat = -lat


      if lng_text[0] == 'E' or lng_text[0] == 'W':
          grados = int(lng_text[1:4])
          minutos = int(lng_text[4:6])
          segundos = int(lng_text[6:8])
          lng = grados + minutos / 60 + segundos / 3600
          if lng_text[0] == 'W':
              lng = -lng


      airport = Airport(codigo, lat, lng) #Creem una línia a la llista per cada aeroport acompanyat de les dades que hem extret
      IsSchengenAirport(airport) #Assignem si és o no Schengen
      airports.append(airport) #Afegim la informació a la llista


      line = file.readline() #Continuem llegint


  file.close()
  return airports #Obtenim la llista amb tot el que hi hem escrit


# Desa en un fitxer només els aeroports marcats com a Schengen.
def SaveSchengenAirports(airports, filename):
  # Si la llista està buida no es pot escrure
  if len(airports) == 0:
      return False
#Obrim fitxer per escriure i n'escrivim la capçalera
  file = open(filename, "w")
  file.write("CODE LAT LON\n")
#Iniciem recorregut i comptador
  i = 0
  written = 0
  while i < len(airports):
      #Comprovem que és Schengen i determinem la latitud i longitud
      if airports[i].isSchengen == True:
          lat = airports[i].latitude
          lng = airports[i].longitude


          if lat >= 0:
              lat_dir = "N"
          else:
              lat_dir = "S"
              lat = -lat


          if lng >= 0:
              lng_dir = "E"
          else:
              lng_dir = "W"
              lng = -lng
#Convertim la latitud i longitud a graus, minuts i segons
          lat_deg = int(lat)
          lat_min_total = (lat - lat_deg) * 60
          lat_min = int(lat_min_total)
          lat_sec = int((lat_min_total - lat_min) * 60)


          lng_deg = int(lng)
          lng_min_total = (lng - lng_deg) * 60
          lng_min = int(lng_min_total)
          lng_sec = int((lng_min_total - lng_min) * 60)


          # LATITUD (2 dígits)
          if lat_deg < 10:
              lat_deg_text = "0" + str(lat_deg)
          else:
              lat_deg_text = str(lat_deg)


          if lat_min < 10:
              lat_min_text = "0" + str(lat_min)
          else:
              lat_min_text = str(lat_min)


          if lat_sec < 10:
              lat_sec_text = "0" + str(lat_sec)
          else:
              lat_sec_text = str(lat_sec)


          lat_text = lat_dir + lat_deg_text + lat_min_text + lat_sec_text


          # LONGITUD (3 dígits en graus)
          if lng_deg < 10:
              lng_deg_text = "00" + str(lng_deg)
          elif lng_deg < 100:
              lng_deg_text = "0" + str(lng_deg)
          else:
              lng_deg_text = str(lng_deg)


          if lng_min < 10:
              lng_min_text = "0" + str(lng_min)
          else:
              lng_min_text = str(lng_min)


          if lng_sec < 10:
              lng_sec_text = "0" + str(lng_sec)
          else:
              lng_sec_text = str(lng_sec)
#Escrivim la longitud i latitud després de les conversions
          lng_text = lng_dir + lng_deg_text + lng_min_text + lng_sec_text


          file.write(airports[i].ICAO + " " + lat_text + " " + lng_text + "\n")
          #Afegim al comptador
          written = written + 1


      i = i + 1


  file.close()


  # Si no s'ha escrit cap aeroport dona error
  if written == 0:
      return False
  else:
      return True


# Afegeix un aeroport si encara no existeix cap amb el mateix codi ICAO.
def AddAirport(airports, airport):
  #iniciem un recorregut i establim un boolea per considerar si ja existeix o no a la llista
  i = 0
  found = False
#Si no trobem l'aeroport a la llista l'afegim
  while i < len(airports) and not found:
      if airports[i].ICAO == airport.ICAO:
          found = True
      i = i + 1


  if not found:
      airports.append(airport)


# Elimina un aeroport buscant-lo pel seu codi ICAO.
def RemoveAirport(airports, code):
  i = 0
  found = False


  # Busquem l'aeroport
  while i < len(airports) and not found:
      if airports[i].ICAO == code:
          found = True
      else:
          i = i + 1


  if found:
      # Desplacem els elements una posició a l'esquerra i el sobreescribim
      while i < len(airports) - 1:
          airports[i] = airports[i + 1]
          i = i + 1


      # Eliminem l'últim element
      del airports[len(airports) - 1]


      return True   #eliminat correctament
  else:
      return False  #no trobat


import matplotlib.pyplot as plt


# Mostra una gràfica amb el nombre d’aeroports Schengen i no Schengen.
def PlotAirports(airports):
  schengen = 0
  no_schengen = 0
  i = 0
  while i < len(airports):
      if airports[i].isSchengen == True:
          schengen = schengen + 1
      else:
          no_schengen = no_schengen + 1
      i = i + 1


  fig, ax = plt.subplots(figsize=(6, 5), facecolor="#0F172A")
  ax.set_facecolor("#1E293B")
  ax.bar(["Airports"], [schengen], label="Schengen", color="#22C55E", width=0.5)
  ax.bar(["Airports"], [no_schengen], bottom=[schengen], label="No Schengen", color="#EF4444", width=0.5)
  ax.set_ylabel("Number of airports", color="#CBD5E1", fontsize=11)
  ax.set_title("Schengen / No Schengen airports", color="#F8FAFC", fontsize=14, pad=12)
  ax.tick_params(colors="#CBD5E1")
  ax.grid(color="#334155", alpha=0.5, axis="y")
  for spine in ax.spines.values():
      spine.set_color("#334155")
  if schengen > 0:
      ax.text(0, schengen / 2, str(schengen), ha="center", va="center", color="white", fontsize=12, fontweight="bold")
  if no_schengen > 0:
      ax.text(0, schengen + no_schengen / 2, str(no_schengen), ha="center", va="center", color="white", fontsize=12, fontweight="bold")
  ax.legend(facecolor="#1E293B", labelcolor="#CBD5E1", edgecolor="#334155")
  fig.tight_layout()
  return fig


# Crea un KML amb els aeroports perquè es puguin veure a Google Earth.
def MapAirports(airports):
  #Obrim el fitxer per escriure les dades
  file = open("airports.kml", "w")
#Escrivim la capçalera
  file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
  file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
  file.write('<Document>\n')
#Iniciem el recorregut
  i = 0
  while i < len(airports):
      #Creem un marcador que rep de nom el codi ICAO per cada aeroport
      file.write('<Placemark>\n')
      file.write('<name>' + airports[i].ICAO + '</name>\n')
#Definim els colors segons si son Schengen o no
      if airports[i].isSchengen == True:
          file.write('<Style>\n')
          file.write('<IconStyle>\n')
          file.write('<color>ff00ff00</color>\n')
          file.write('</IconStyle>\n')
          file.write('</Style>\n')
      else:
          file.write('<Style>\n')
          file.write('<IconStyle>\n')
          file.write('<color>ff0000ff</color>\n')
          file.write('</IconStyle>\n')
          file.write('</Style>\n')


      file.write('<Point>\n')
      file.write('<coordinates>' + str(airports[i].longitude) + ',' + str(airports[i].latitude) + ',0</coordinates>\n')
      file.write('</Point>\n')
      file.write('</Placemark>\n')


      i = i + 1


  file.write('</Document>\n')
  file.write('</kml>\n')


