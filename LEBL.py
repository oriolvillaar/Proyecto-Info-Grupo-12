from aircraft import *
from airports import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


#Primerament, creem les classes necessàries


# Aeroport
class BarcelonaAP:
 def __init__(self):
     self.code = ""        # codi ICAO (ex: LEBL)
     self.terminals = []   # llista de terminals


# Terminal
class Terminal:
 def __init__(self):
     self.name = ""        # nom del terminal (T1, T2...)
     self.areas = []       # llista de BoardingArea
     self.airlines = []    # llista de codis ICAO d'aerolínies


# Zona d'embarcament
class BoardingArea:
 def __init__(self):
     self.name = ""        # nom de l’àrea (ex: T1BAA)
     self.area_type = ""   # tipus: Schengen o non-Schengen
     self.gates = []       # llista de portes (Gate)


# Porta d'embarcament
class Gate:
 def __init__(self):
     self.name = ""            # nom de la porta (ex: T1BAAG1)
     self.isOccupied = False  # indica si està ocupada
     self.aircraft_id = ""    # id de l’avió si està ocupada


# Funció per a crear les portes de cada àrea
# Crea totes les portes d’una àrea a partir del rang indicat al fitxer LEBL.
def SetGates(area, init_gate, end_gate, prefix):
 # Comprovem que els valors siguin correctes
 if end_gate < init_gate:
     return -1   # error: el final no pot ser més petit que l’inici


 # Calculem nombre de portes
 num_gates = end_gate - init_gate + 1


 # Creem la llista de portes
 area.gates = [None] * num_gates


 i = 0
 gate_number = init_gate


 # Fem el recorregut
 while gate_number <= end_gate:
     gate = Gate()   # creem nova porta


     # Assignem nom: prefix + número
     gate.name = prefix + str(gate_number)


     # Totes les portes comencen estant lliures
     gate.isOccupied = False
     gate.aircraft_id = ""


     # Guardem la porta
     area.gates[i] = gate


     # Avancem posició i número
     i = i + 1
     gate_number = gate_number + 1


 return 0

# Carrega els codis ICAO de les aerolínies que operen en una terminal concreta.
def LoadAirlines(terminal, t_name):
 # Escriure nom del fitxer
 filename = t_name + "_Airlines.txt"


 # Obrim el fitxer
 try:
     file = open(filename, "r")
 except FileNotFoundError:
     print ("File was not found")
     return -1   # Si el fitxer no existeix, dona error


 # Llegim totes les línies
 lines = file.readlines()
 file.close()


 # Creem la llista d’aerolínies
 terminal.airlines = [None] * len(lines)


 #Iniciem recorregut
 i = 0
 while i < len(lines):
     # Separem per tabulador
     parts = lines[i].split("\t")


     # Guardem només el codi ICAO
     code = parts[1].strip()
     terminal.airlines[i] = code


     i = i + 1


 return 0   # correcte


#Llegim el fitxer i creem tots els objectes necessaris per apoder treballar amb ells
def LoadAirportStructure(filename):
 # Obrim el fitxer
 try:
     file = open(filename, "r")
 except FileNotFoundError:
     print ("File was not found")
     return -1


 # Llegim primera línia
 line = file.readline()
 parts = line.split()


 # Creem objecte aeroport i assignem parts
 bcn = BarcelonaAP()
 bcn.code = parts[0]


 num_terminals = int(parts[1])
 bcn.terminals = [None] * num_terminals


 # Iniciem recorregut
 i = 0
 while i < num_terminals:


     # Llegim línia del terminal
     line = file.readline()
     parts = line.split()


     terminal = Terminal()
     terminal.name = parts[1]


     # Num d’àrees d’embarcament
     num_areas = int(parts[2])
     terminal.areas = [None] * num_areas


     # Carreguem aerolínies
     result = LoadAirlines(terminal, terminal.name)
     if result == -1:
         file.close()
         return -1


     # Iniciem recorregut
     j = 0
     while j < num_areas:


         # Llegim línia d’una àrea
         line = file.readline()
         parts = line.split()


         area = BoardingArea()


         # Construïm de l’àrea
         area_letter = parts[1]
         area.name = terminal.name + "BA" + area_letter


         # Assignem tipus
         area.area_type = parts[2]


         # Llegim rang de portes
         init_gate = int(parts[4])
         end_gate = int(parts[6])


         # Prefix per crear noms de portes
         prefix = area.name + "G"


         # Creem les portes de l’àrea
         result = SetGates(area, init_gate, end_gate, prefix)
         if result == -1:
             file.close()
             return -1


         # Guardem l’àrea dins el terminal
         terminal.areas[j] = area


         j = j + 1


     # Guardem el terminal dins l’aeroport
     bcn.terminals[i] = terminal


     i = i + 1


 file.close()
 return bcn


# Obtenim llista amb les portes i si estan ocupades o no i per qui
def GateOccupancy(bcn):
 # Comptem el nombre total de portes
 total_gates = 0


 # Iniciem recorregut terminals
 i = 0
 while i < len(bcn.terminals):
     terminal = bcn.terminals[i]


     # Iniciem recorregut àrees terminal
     j = 0
     while j < len(terminal.areas):
         area = terminal.areas[j]


         total_gates = total_gates + len(area.gates)


         j = j + 1


     i = i + 1


 # Creem la llista resultat amb mida fixa
 result = [None] * total_gates


 k = 0


 # Tornem a recórrer per guardar la info
 i = 0
 while i < len(bcn.terminals):
     terminal = bcn.terminals[i]


     j = 0
     while j < len(terminal.areas):
         area = terminal.areas[j]


         # Recrrem gates
         h = 0
         while h < len(area.gates):
             gate = area.gates[h]


             # Guardem la info en una llista
             result[k] = [gate.name, gate.isOccupied, gate.aircraft_id]


             k = k + 1
             h = h + 1


         j = j + 1


     i = i + 1


 return result


# Comprovem si una aerolínia és a la terminal
def IsAirlineInTerminal(terminal, name):


 # Comprovem si el nom és buit
 if name == "":
     return -1


 # Si la llista està buida
 if len(terminal.airlines) == 0:
     return False


 # Iniciem recorregut llista aerolínies
 i = 0
 while i < len(terminal.airlines):
     if terminal.airlines[i] == name:
         return True
     i = i + 1


 return False


# Busca en quin terminal opera una aerolínia
def SearchTerminal(bcn, name):


 # Si el nom és buit
 if name == "":
     return ""


 i = 0
 while i < len(bcn.terminals):
     terminal = bcn.terminals[i]


     # Fem servir la funció anterior
     result = IsAirlineInTerminal(terminal, name)


     if result == True:
         return terminal.name


     i = i + 1


 # Si no es troba en cap terminal
 return ""


# Comprova si un avió ja té porta assignada per evitar duplicats.
def IsAircraftAlreadyAssigned(bcn, aircraft_id):


  i = 0
  while i < len(bcn.terminals):


      terminal = bcn.terminals[i]


      j = 0
      while j < len(terminal.areas):


          area = terminal.areas[j]


          k = 0
          while k < len(area.gates):


              gate = area.gates[k]


              if gate.aircraft_id == aircraft_id:
                  return True


              k = k + 1


          j = j + 1


      i = i + 1


  return False


# Assigna la primera porta lliure compatible amb terminal i tipus de vol.
def AssignGate(bcn, aircraft):


  # Comprovem dades bàsiques de l’avió
  if aircraft.airline == "" or aircraft.id == "":
      return -1


  # Si aquest avió ja té porta, no el tornem a assignar
  if IsAircraftAlreadyAssigned(bcn, aircraft.id) == True:
      return -2


  # Per decidir si el vol és Schengen, en arribades mirem l’origen.
  # En avions nocturns, com no tenen origen del dia, fem servir la destinació de sortida.
  # Si és una arribada normal, fem servir origin
  if aircraft.origin != "":
      airport_code = aircraft.origin


  # Si és un night aircraft, fem servir destination
  elif aircraft.destination != "":
      airport_code = aircraft.destination


  else:
      return -1


  # Busquem el terminal de l’aerolínia
  terminal_name = SearchTerminal(bcn, aircraft.airline)


  # Si no existeix l’aerolínia
  if terminal_name == "":
      return -1


  # Mirem si l’aeroport és Schengen
  origin_airport = Airport(airport_code, 0, 0)
  SetSchengen(origin_airport)


  if origin_airport.isSchengen == True:
      flight_type = "Schengen"
  else:
      flight_type = "non-Schengen"


  # Busquem el terminal dins bcn
  i = 0
  found_terminal = False


  while i < len(bcn.terminals) and found_terminal == False:
      if bcn.terminals[i].name == terminal_name:
          found_terminal = True
      else:
          i = i + 1


  if found_terminal == False:
      return -1


  terminal = bcn.terminals[i]


  # Recorrem només les àrees compatibles amb el tipus de vol.
  # La primera porta lliure trobada queda ocupada per aquest avió.
  # Busquem porta lliure del tipus correcte
  j = 0
  while j < len(terminal.areas):
      area = terminal.areas[j]


      if area.area_type == flight_type:
          k = 0
          while k < len(area.gates):
              gate = area.gates[k]


              if gate.isOccupied == False:
                  gate.isOccupied = True
                  gate.aircraft_id = aircraft.id
                  return 0


              k = k + 1


      j = j + 1


  return -1


# Assigna portes als avions que han passat la nit a l’aeroport.
def AssignNightGates(bcn, aircrafts):
  # Si la llista és buida, retornem error
  if len(aircrafts) == 0:
      return -1


  assigned = 0
  i = 0


  while i < len(aircrafts):


      # Només assignem aircrafts que no tenen dades d'arribada
      # però sí dades de sortida
      if aircrafts[i].origin == "" and aircrafts[i].landing_time == "":
          if aircrafts[i].destination != "" and aircrafts[i].departure_time != "":


              result = AssignGate(bcn, aircrafts[i])


              if result == 0:
                  assigned = assigned + 1


      i = i + 1


  return assigned


# Allibera la porta on es troba l’avió indicat.
def FreeGate(bcn, id):


  # Recorrem terminals
  i = 0
  while i < len(bcn.terminals):


      terminal = bcn.terminals[i]


      # Recorrem àrees
      j = 0
      while j < len(terminal.areas):


          area = terminal.areas[j]


          # Recorrem portes
          k = 0
          while k < len(area.gates):


              gate = area.gates[k]


              # Si trobem l'avió
              if gate.aircraft_id == id:


                  # Alliberem la porta
                  gate.isOccupied = False
                  gate.aircraft_id = ""


                  return 0


              k = k + 1


          j = j + 1


      i = i + 1


  # Si no s'ha trobat l'avió
  return -1


# Comprova si una hora cau dins una franja d’una hora.
def IsTimeInPeriod(aircraft_time, period_time):


  aircraft_minutes = TimeToMinutes(aircraft_time)
  period_minutes = TimeToMinutes(period_time)


  if aircraft_minutes >= period_minutes and aircraft_minutes < period_minutes + 60:
      return True
  else:
      return False


# Allibera tots els avions que ja han sortit abans d’una hora determinada.
def FreeDepartedAircrafts(bcn, aircrafts, time):


  # Convertim l’hora límit a minuts per comparar sortides sense problemes de format.
  limit_minutes = TimeToMinutes(time)


  i = 0
  while i < len(aircrafts):


      if aircrafts[i].departure_time != "":
          departure_minutes = TimeToMinutes(aircrafts[i].departure_time)


          if departure_minutes <= limit_minutes:
              FreeGate(bcn, aircrafts[i].id)


      i = i + 1


# Assigna la primera porta lliure compatible amb terminal i tipus de vol.
# Processa una franja horària: primer allibera sortides i després assigna arribades.
def AssignGatesAtTime(bcn, aircrafts, time):


  not_assigned = 0


  if len(aircrafts) == 0:
      return -1


  # Primer alliberem avions que ja han sortit abans de començar aquesta hora.
  FreeDepartedAircrafts(bcn, aircrafts, time)


  i = 0
  while i < len(aircrafts):


      # Només assignem avions que tenen arribada
      if aircrafts[i].landing_time != "":


          # Comprovem si aterren dins la franja [time, time + 1h)
          if IsTimeInPeriod(aircrafts[i].landing_time, time) == True:


              # Abans d'assignar aquest avió, alliberem sortides anterior a la seva hora exacta d'arribada
              FreeDepartedAircrafts(bcn, aircrafts, aircrafts[i].landing_time)


              result = AssignGate(bcn, aircrafts[i])


              if result == -1:
                  not_assigned = not_assigned + 1
      i = i + 1


  return not_assigned


# Compta quantes portes ocupades té una terminal.
def CountOccupiedTerminal(terminal):


  count = 0


  i = 0
  while i < len(terminal.areas):


      area = terminal.areas[i]


      j = 0
      while j < len(area.gates):


          if area.gates[j].isOccupied == True:
              count = count + 1


          j = j + 1


      i = i + 1


  return count


# Simula el dia complet i genera la gràfica d’ocupació per hores.
def PlotDayOccupancy(bcn, aircrafts):


  if len(aircrafts) == 0:
      return -1


  hours = []
  not_assigned = []
  terminal_occupancy = []


  i = 0
  while i < len(bcn.terminals):
      terminal_occupancy.append([])
      i = i + 1


  hour = 0
  while hour < 24:
      if hour < 10:
          time = "0" + str(hour) + ":00"
      else:
          time = str(hour) + ":00"


      hours.append(hour)
      failed = AssignGatesAtTime(bcn, aircrafts, time)
      not_assigned.append(failed)


      i = 0
      while i < len(bcn.terminals):
          occupied = CountOccupiedTerminal(bcn.terminals[i])
          terminal_occupancy[i].append(occupied)
          i = i + 1


      hour = hour + 1


  palette = ["#2563EB", "#22C55E", "#F59E0B", "#EF4444"]


  fig, ax = plt.subplots(figsize=(11, 5), facecolor="#0F172A")
  ax.set_facecolor("#1E293B")


  i = 0
  while i < len(bcn.terminals):
      ax.plot(hours, terminal_occupancy[i], marker="o",
              label=bcn.terminals[i].name,
              color=palette[i % len(palette)], linewidth=2, markersize=5)
      i = i + 1


  ax.plot(hours, not_assigned, marker="x", label="Not assigned",
          color="#94A3B8", linewidth=1.5, linestyle="--")


  ax.set_title("LEBL gate occupancy during the day", color="#F8FAFC", fontsize=14, pad=12)
  ax.set_xlabel("Hour", color="#CBD5E1", fontsize=11)
  ax.set_ylabel("Aircraft / occupied gates", color="#CBD5E1", fontsize=11)
  ax.tick_params(colors="#CBD5E1")
  ax.grid(color="#334155", alpha=0.5)
  for spine in ax.spines.values():
      spine.set_color("#334155")
  ax.legend(facecolor="#1E293B", labelcolor="#CBD5E1", edgecolor="#334155")
  fig.tight_layout()
  return fig


# Mostra un dibuix de portes
def PlotGateOccupancy(bcn):
 if bcn == None:
     return -1

 from matplotlib.patches import Rectangle, FancyBboxPatch, Patch

 # Colors coherents amb la interfície fosca
 bg_color = "#0F172A"
 panel_color = "#111827"
 border_color = "#334155"
 text_color = "#F8FAFC"
 muted_color = "#CBD5E1"
 free_color = "#1E293B"
 occupied_color = "#38BDF8"
 schengen_color = "#22C55E"
 nonschengen_color = "#F97316"

 fig, ax = plt.subplots(figsize=(15, 8.5), facecolor=bg_color)
 ax.set_facecolor(bg_color)
 ax.axis("off")

 # Comptadors globals
 total_gates = 0
 occupied_gates = 0

 i = 0
 while i < len(bcn.terminals):
     terminal = bcn.terminals[i]
     j = 0
     while j < len(terminal.areas):
         area = terminal.areas[j]
         k = 0
         while k < len(area.gates):
             total_gates = total_gates + 1
             if area.gates[k].isOccupied == True:
                 occupied_gates = occupied_gates + 1
             k = k + 1
         j = j + 1
     i = i + 1

 free_gates = total_gates - occupied_gates

 # Títol principal
 ax.text(
     0,
     0,
     "LEBL Gate Occupancy",
     fontsize=20,
     fontweight="bold",
     color=text_color,
     ha="left",
     va="top"
 )

 ax.text(
     0,
     -0.45,
     "Occupied: " + str(occupied_gates) + "   Free: " + str(free_gates) + "   Total: " + str(total_gates),
     fontsize=11,
     color=muted_color,
     ha="left",
     va="top"
 )

 # Mides del dibuix
 gate_size = 0.18
 gate_gap = 0.07
 gates_per_row = 10
 card_padding_x = 0.28
 card_padding_y = 0.28
 card_header = 0.78
 area_gap = 0.35
 terminal_gap = 1.10
 y_cursor = -1.35
 max_x = 0

 # Recorrem terminals
 i = 0
 while i < len(bcn.terminals):
     terminal = bcn.terminals[i]

     # Comptem terminal
     terminal_total = 0
     terminal_occupied = 0
     j = 0
     while j < len(terminal.areas):
         area = terminal.areas[j]
         k = 0
         while k < len(area.gates):
             terminal_total = terminal_total + 1
             if area.gates[k].isOccupied == True:
                 terminal_occupied = terminal_occupied + 1
             k = k + 1
         j = j + 1

     ax.text(
         0,
         y_cursor,
         terminal.name + "  ·  " + str(terminal_occupied) + "/" + str(terminal_total) + " occupied",
         fontsize=15,
         fontweight="bold",
         color=text_color,
         ha="left",
         va="top"
     )

     x_cursor = 0
     y_cards_top = y_cursor - 0.35
     max_card_height = 0

     j = 0
     while j < len(terminal.areas):
         area = terminal.areas[j]

         area_total = len(area.gates)
         area_occupied = 0
         k = 0
         while k < len(area.gates):
             if area.gates[k].isOccupied == True:
                 area_occupied = area_occupied + 1
             k = k + 1

         rows = (area_total + gates_per_row - 1) // gates_per_row
         cols = gates_per_row
         if area_total < gates_per_row:
             cols = area_total

         gate_grid_width = cols * gate_size + (cols - 1) * gate_gap
         gate_grid_height = rows * gate_size + (rows - 1) * gate_gap

         card_width = gate_grid_width + 2 * card_padding_x
         if card_width < 2.15:
             card_width = 2.15

         card_height = card_header + gate_grid_height + 2 * card_padding_y

         if card_height > max_card_height:
             max_card_height = card_height

         # Targeta de l'àrea
         card = FancyBboxPatch(
             (x_cursor, y_cards_top - card_height),
             card_width,
             card_height,
             boxstyle="round,pad=0.03,rounding_size=0.10",
             facecolor=panel_color,
             edgecolor=border_color,
             linewidth=1.0
         )
         ax.add_patch(card)

         # Barra superior segons tipus de zona
         if area.area_type == "Schengen":
             accent_color = schengen_color
         else:
             accent_color = nonschengen_color

         ax.add_patch(
             Rectangle(
                 (x_cursor, y_cards_top - 0.10),
                 card_width,
                 0.10,
                 facecolor=accent_color,
                 edgecolor=accent_color,
                 linewidth=0
             )
         )

         ax.text(
             x_cursor + card_padding_x,
             y_cards_top - 0.25,
             area.name,
             fontsize=10,
             fontweight="bold",
             color=text_color,
             ha="left",
             va="top"
         )

         ax.text(
             x_cursor + card_padding_x,
             y_cards_top - 0.57,
             area.area_type + " · " + str(area_occupied) + "/" + str(area_total),
             fontsize=8,
             color=muted_color,
             ha="left",
             va="top"
         )

         # Dibuixem portes com a graella ordenada
         grid_x = x_cursor + card_padding_x
         grid_y = y_cards_top - card_header - card_padding_y

         k = 0
         while k < len(area.gates):
             row = k // gates_per_row
             col = k % gates_per_row

             x = grid_x + col * (gate_size + gate_gap)
             y = grid_y - row * (gate_size + gate_gap)

             gate = area.gates[k]

             if gate.isOccupied == True:
                 face = occupied_color
                 edge = occupied_color
             else:
                 face = free_color
                 edge = "#64748B"

             square = Rectangle(
                 (x, y - gate_size),
                 gate_size,
                 gate_size,
                 facecolor=face,
                 edgecolor=edge,
                 linewidth=0.8
             )
             ax.add_patch(square)

             k = k + 1

         x_cursor = x_cursor + card_width + area_gap

         if x_cursor > max_x:
             max_x = x_cursor

         j = j + 1

     y_cursor = y_cards_top - max_card_height - terminal_gap
     i = i + 1

 # Llegenda
 legend_items = [
     Patch(facecolor=occupied_color, edgecolor=occupied_color, label="Occupied gate"),
     Patch(facecolor=free_color, edgecolor="#64748B", label="Free gate"),
     Patch(facecolor=schengen_color, edgecolor=schengen_color, label="Schengen area"),
     Patch(facecolor=nonschengen_color, edgecolor=nonschengen_color, label="Non-Schengen area")
 ]

 legend = ax.legend(
     handles=legend_items,
     loc="upper right",
     frameon=True,
     facecolor=panel_color,
     edgecolor=border_color,
     labelcolor=muted_color,
     fontsize=9
 )

 for text in legend.get_texts():
     text.set_color(muted_color)

 ax.set_xlim(-0.15, max_x + 0.15)
 ax.set_ylim(y_cursor + 0.25, 0.35)

 fig.tight_layout(pad=1.2)
 return fig


# Test


if __name__ == '__main__':
  print('----- TEST V4 FUNCTIONS -----')


  arrivals = LoadArrivals('Arrivals.txt')
  departures, error = LoadDepartures('Departures.txt')
  movements, error = MergeMovements(arrivals, departures)
  night, error = NightAircraft(movements)


  bcn = LoadAirportStructure('LEBL.txt')


  assigned_night = AssignNightGates(bcn, night)
  print('Assigned night aircraft:', assigned_night)
