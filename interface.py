import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from airports import *
from aircraft import *
from LEBL import *

# VISUAL STYLE
BG = "#0F172A"        # dark navy background
PANEL = "#1E293B"     # dark grey panels
TEXT = "#F8FAFC"      # main text
MUTED = "#CBD5E1"     # secondary text
BLUE = "#2563EB"      # main buttons
GREEN = "#22C55E"     # success
RED = "#EF4444"       # errors
ORANGE = "#F59E0B"    # warnings

FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_SECTION = ("Segoe UI", 10, "bold")
FONT_NORMAL = ("Segoe UI", 9)
FONT_BUTTON = ("Segoe UI", 9, "bold")

airports = []
aircrafts = []
departures = []
movements = []
night_aircrafts = []
bcn = None


# Actualitza la llista visual d’aeroports.
def UpdateAirportList():
  listbox_airports.delete(0, tk.END)
  i = 0
  while i < len(airports):
      text = airports[i].ICAO + " | " + str(airports[i].latitude) + " | " + str(airports[i].longitude) + " | " + str(airports[i].isSchengen)
      listbox_airports.insert(tk.END, text)
      i = i + 1


# Actualitza la llista visual de vols i moviments.
def UpdateAircraftList():
  listbox_aircrafts.delete(0, tk.END)
  i = 0
  while i < len(aircrafts):
      text = aircrafts[i].id + " | "
      if aircrafts[i].origin != "":
          text = text + aircrafts[i].origin + "->LEBL " + aircrafts[i].landing_time
      else:
          text = text + "No arrival"
      text = text + " | "
      if aircrafts[i].destination != "":
          text = text + "LEBL->" + aircrafts[i].destination + " " + aircrafts[i].departure_time
      else:
          text = text + "No departure"
      text = text + " | " + aircrafts[i].airline
      listbox_aircrafts.insert(tk.END, text)
      i = i + 1

# Actualitza la llista visual de portes.
def UpdateGateList():
  listbox_gates.delete(0, tk.END)
  if bcn == None:
      return
  gates = GateOccupancy(bcn)
  i = 0
  while i < len(gates):
      if gates[i][1] == True:
          status = "Occupied"
      else:
          status = "Free"
      text = gates[i][0] + "  " + status + "  " + gates[i][2]
      listbox_gates.insert(tk.END, text)
      i = i + 1

# Actualitza el resum superior amb comptadors generals.
def UpdateStats():
  num_airports = len(airports)
  num_flights = len(aircrafts)
  occupied = 0
  free = 0

  if bcn != None:
      gates = GateOccupancy(bcn)
      i = 0
      while i < len(gates):
          if gates[i][1] == True:
              occupied = occupied + 1
          else:
              free = free + 1

          i = i + 1

  stats_label.config(
      text="Airports.txt: " + str(num_airports) +
           "     Flights: " + str(num_flights) +
           "     Occupied Gates: " + str(occupied) +
           "     Free Gates: " + str(free)
  )

# Botó per carregar aeroports i assignar-los el valor Schengen.
def LoadButton():
  global airports
  filename = entry_file.get().strip()
  airports = LoadAirports(filename)
  i = 0
  while i < len(airports):
      SetSchengen(airports[i])
      i = i + 1
  UpdateAirportList()
  UpdateStats()
  label_result.config(text="Airports.txt loaded: " + str(len(airports)))

# Botó per afegir manualment un aeroport a la llista.
def AddButton():
  try:
      code = entry_code.get().strip().upper()
      lat = float(entry_lat.get())
      lng = float(entry_lng.get())
      airport = Airport(code, lat, lng)
      SetSchengen(airport)
      AddAirport(airports, airport)
      UpdateAirportList()
      UpdateStats()

      label_result.config(text="Airport processed")

  except:
      label_result.config(text="Error in airport data")


# Botó per eliminar l’aeroport escrit a la caixa de codi.
def RemoveButton():
  code = entry_code.get().strip().upper()
  result = RemoveAirport(airports, code)

  if result:
      UpdateAirportList()
      UpdateStats()
      label_result.config(text="Airport removed")
  else:
      label_result.config(text="Airport not found")

# Botó per recalcular el camp Schengen de tots els aeroports.
def SetSchengenButton():
  i = 0
  while i < len(airports):
      SetSchengen(airports[i])
      i = i + 1
  UpdateAirportList()
  UpdateStats()
  label_result.config(text="Schengen updated")


# Botó per guardar els aeroports Schengen en un fitxer.
def SaveButton():
  filename = entry_save.get().strip()
  result = SaveSchengenAirports(airports, filename)

  if result:
      label_result.config(text="Schengen airports saved")
  else:
      label_result.config(text="Error saving file")


# Obre una finestra nova per mostrar una figura de Matplotlib dins Tkinter.
def ShowPlotWindow(fig, title):
  win = tk.Toplevel(root)
  win.title(title)
  win.configure(bg=BG)
  win.protocol("WM_DELETE_WINDOW", lambda: (plt.close(fig), win.destroy()))
  canvas = FigureCanvasTkAgg(fig, master=win)
  canvas.draw()
  canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=3)


# Botó de funcionalitat extra: calcula emissions estimades dels vols carregats.
def EmissionsButton():
  if len(aircrafts) == 0:
      label_result.config(text="Load flights first")
      return
  if len(airports) == 0:
      label_result.config(text="Load airports first")
      return

  result = CalculateEmissions(aircrafts, airports)

  if result is None:
      label_result.config(text="Could not calculate (LEBL not found in airports)")
      return

  text_output.delete("1.0", tk.END)
  text_output.insert(tk.END, "AVERAGE EMISSIONS CALCULATION\n")
  text_output.insert(tk.END, "=" * 42 + "\n\n")
  text_output.insert(tk.END, "Flights analyzed:          " + str(result['total_flights']) + "\n")
  text_output.insert(tk.END, "  Short haul  (<1500 km):  " + str(result['short_haul']) + "\n")
  text_output.insert(tk.END, "  Medium haul (1500-4000): " + str(result['medium_haul']) + "\n")
  text_output.insert(tk.END, "  Long haul   (>4000 km):  " + str(result['long_haul']) + "\n\n")
  text_output.insert(tk.END, "Avg distance / flight:     " + str(int(result['avg_distance_km'])) + " km\n")
  text_output.insert(tk.END, "Avg CO2 / flight:          " + str(int(result['avg_co2_kg'])) + " kg\n\n")
  text_output.insert(tk.END, "Total distance:            " + str(int(result['total_distance_km'])) + " km\n")
  text_output.insert(tk.END, "Total CO2 emissions:       " + str(round(result['total_co2_tons'], 1)) + " tonnes\n")

  label_result.config(text="Emissions: avg " + str(int(result['avg_co2_kg'])) + " kg CO2/flight  |  Total: " + str(round(result['total_co2_tons'], 1)) + " t")


def PlotButton():
  fig = PlotAirports(airports)
  if fig is not None:
      ShowPlotWindow(fig, "Airports - Schengen Distribution")
  label_result.config(text="Airport plot shown")

def MapButton():
  MapAirports(airports)
  label_result.config(text="Airport KML file created")

def ShowSelectedAirportButton():
  selected = listbox_airports.curselection()

  if len(selected) > 0:
      index = selected[0]
      airport = airports[index]
      text_output.delete("1.0", tk.END)
      text_output.insert(tk.END, "ICAO: " + airport.ICAO + "\n")
      text_output.insert(tk.END, "Latitude: " + str(airport.latitude) + "\n")
      text_output.insert(tk.END, "Longitude: " + str(airport.longitude) + "\n")
      text_output.insert(tk.END, "Schengen: " + str(airport.isSchengen) + "\n")

# Botó per carregar les arribades del dia.
def LoadArrivalsButton():
  global aircrafts

  filename = entry_arrivals_file.get().strip()
  aircrafts = LoadArrivals(filename)
  UpdateAircraftList()
  UpdateStats()
  label_result.config(text="Arrivals loaded: " + str(len(aircrafts)))

# Botó per carregar les sortides necessàries per a la V4.
def LoadDeparturesButton():
  global departures
  filename = entry_departures_file.get().strip()
  departures, error = LoadDepartures(filename)
  if error == -1:
      label_result.config(text="Error loading departures file")
  else:
      label_result.config(text="Departures loaded: " + str(len(departures)))


# Botó per combinar arribades i sortides.
def MergeMovementsButton():
  global aircrafts
  global departures
  global movements
  global night_aircrafts

  # La fusió permet que un avió tingui arribada i sortida.
  movements, error = MergeMovements(aircrafts, departures)
  if error == -1:
      label_result.config(text="Load arrivals and departures first")
  else:
      night_aircrafts, error_night = NightAircraft(movements)
      aircrafts = movements
      UpdateAircraftList()
      UpdateStats()
      label_result.config(
          text="Movements merged: " + str(len(movements)) +
               " | Night aircraft: " + str(len(night_aircrafts))
      )

def SaveFlightsButton():
  filename = entry_arrivals_save.get().strip()
  result = SaveFlights(aircrafts, filename)
  if result:
      label_result.config(text="Flights saved")
  else:
      label_result.config(text="Error saving flights")


def PlotArrivalsButton():
  fig = PlotArrivals(aircrafts)
  if fig is not None:
      ShowPlotWindow(fig, "Arrivals by Hour")
  label_result.config(text="Arrivals plot shown")


def PlotAirlinesButton():
  fig = PlotAirlines(aircrafts)
  if fig is not None:
      ShowPlotWindow(fig, "Flights per Airline")
  label_result.config(text="Airlines plot shown")


def PlotFlightsTypeButton():
  if len(airports) == 0:
      label_result.config(text="Load airports first")
      return
  fig = PlotFlightsType(aircrafts, airports)
  if fig is not None:
      ShowPlotWindow(fig, "Schengen vs Non-Schengen")
  label_result.config(text="Flights type plot shown")


def MapFlightsButton():
  if len(airports) == 0:
      label_result.config(text="Load airports first")
      return

  MapFlights(aircrafts, airports)
  label_result.config(text="Flights KML file created")

def ShowLongDistanceButton():
  global aircrafts

  if len(airports) == 0:
      label_result.config(text="Load airports first")
      return

  aircrafts = LongDistanceArrivals(aircrafts, airports)

  UpdateAircraftList()
  UpdateStats()
  label_result.config(text="Long distance flights shown: " + str(len(aircrafts)))

def ShowSelectedAircraftButton():
  selected = listbox_aircrafts.curselection()

  if len(selected) > 0:
      index = selected[0]
      aircraft = aircrafts[index]
      text_output.delete("1.0", tk.END)
      text_output.insert(tk.END, "Aircraft ID: " + aircraft.id + "\n")
      text_output.insert(tk.END, "Airline: " + aircraft.airline + "\n\n")

      # Arrival information
      if aircraft.origin != "" and aircraft.landing_time != "":
          text_output.insert(tk.END, "ARRIVAL FLIGHT\n")
          text_output.insert(tk.END, "Route: " + aircraft.origin + " -> LEBL\n")
          text_output.insert(tk.END, "Landing time at LEBL: " + aircraft.landing_time + "\n\n")
      else:
          text_output.insert(tk.END, "ARRIVAL FLIGHT\n")
          text_output.insert(tk.END, "No arrival during this day\n\n")

      # Departure information
      if aircraft.destination != "" and aircraft.departure_time != "":
          text_output.insert(tk.END, "DEPARTURE FLIGHT\n")
          text_output.insert(tk.END, "Route: LEBL -> " + aircraft.destination + "\n")
          text_output.insert(tk.END, "Departure time from LEBL: " + aircraft.departure_time + "\n")
      else:
          text_output.insert(tk.END, "DEPARTURE FLIGHT\n")
          text_output.insert(tk.END, "No departure during this day\n")


def LoadLEBLButton():
  global bcn
  filename = entry_lebl_file.get().strip()
  bcn = LoadAirportStructure(filename)
  if bcn == -1:
      bcn = None
      label_result.config(text="Error loading LEBL structure")
  else:
      UpdateGateList()
      UpdateStats()
      label_result.config(text="LEBL structure loaded")


# Assigna portes a tots els vols carregats sense simular l’evolució horària.
def AssignGatesButton():
  if bcn == None:
      label_result.config(text="Load LEBL structure first")
      return

  if len(aircrafts) == 0:
      label_result.config(text="Load arrivals first")
      return
  assigned = 0
  errors = 0

  i = 0
  while i < len(aircrafts):
      result = AssignGate(bcn, aircrafts[i])

      if result == 0:
          assigned = assigned + 1
      else:
          errors = errors + 1

      i = i + 1

  UpdateGateList()
  UpdateStats()

  label_result.config(
      text="Assigned: " + str(assigned) +
           " | Errors: " + str(errors)
  )


# Assigna portes als avions que ja estaven a LEBL abans de començar el dia.
def AssignNightGatesButton():
  global bcn
  global night_aircrafts

  if bcn == None:
      label_result.config(text="Load LEBL structure first")
      return

  if len(night_aircrafts) == 0:
      label_result.config(text="Merge movements first")
      return

  assigned = AssignNightGates(bcn, night_aircrafts)

  if assigned == -1:
      label_result.config(text="No night aircraft to assign")
  else:
      UpdateGateList()
      UpdateStats()
      label_result.config(text="Night aircraft assigned: " + str(assigned))


# Botó per processar una hora concreta a la V4.
def AssignGatesAtHourButton():
  global bcn
  global movements
  if bcn == None:
      label_result.config(text="Load LEBL structure first")
      return

  if len(movements) == 0:
      label_result.config(text="Merge movements first")
      return
  time = entry_hour.get().strip()

  if IsValidTime(time) == False:
      label_result.config(text="Invalid time format. Use hh:mm")
      return

  not_assigned = AssignGatesAtTime(bcn, movements, time)

  UpdateGateList()
  UpdateStats()

  if not_assigned > 0:
      label_result.config(
          text="Hour " + time + " processed | Not assigned: " + str(not_assigned) +
               "\nSome airlines were not found in terminal files."
      )
  else:
      label_result.config(
          text="Hour " + time + " processed | All aircraft assigned"
      )

# Botó per simular i representar l’ocupació de tot el dia.
def PlotDayOccupancyButton():
  global bcn
  global movements
  global night_aircrafts

  if bcn == None:
      label_result.config(text="Load LEBL structure first")
      return

  if len(movements) == 0:
      label_result.config(text="Merge movements first")
      return

  filename = entry_lebl_file.get().strip()
  bcn = LoadAirportStructure(filename)

  if bcn == -1:
      bcn = None
      label_result.config(text="Error loading LEBL structure")
      return

  # Abans de simular el dia, col·loquem els avions que ja estaven a l’aeroport.
  AssignNightGates(bcn, night_aircrafts)

  fig = PlotDayOccupancy(bcn, movements)

  if fig == -1:
      label_result.config(text="Error plotting day occupancy")
  else:
      ShowPlotWindow(fig, "Day Gate Occupancy")
      UpdateGateList()
      label_result.config(text="Day occupancy plot shown")

def ShowSelectedGateButton():
  if bcn == None:
      label_result.config(text="Load LEBL structure first")
      return

  selected = listbox_gates.curselection()
  if len(selected) > 0:
      index = selected[0]
      gates = GateOccupancy(bcn)
      gate = gates[index]

      if gate[1] == True:
          status = "Occupied"
      else:
          status = "Free"

      text_output.delete("1.0", tk.END)
      text_output.insert(tk.END, "Gate: " + gate[0] + "\n")
      text_output.insert(tk.END, "Status: " + status + "\n")
      text_output.insert(tk.END, "Aircraft ID: " + gate[2] + "\n")

def PlotGateOccupancyButton():
  if bcn == None:
      label_result.config(text="Load LEBL structure first")
      return
  fig = PlotGateOccupancy(bcn)
  if fig != -1:
      ShowPlotWindow(fig, "Gate Occupancy")
  label_result.config(text="Gate occupancy plot shown")


# Botó ràpid per carregar tots els fitxers principals.
def LoadAllButton():
  # Carrega tots els fitxers principals amb un sol botó.
  # També fa el merge perquè a la llista apareguin les sortides.
  LoadButton()
  LoadArrivalsButton()
  LoadDeparturesButton()

  if len(aircrafts) > 0 and len(departures) > 0:
      MergeMovementsButton()

  LoadLEBLButton()

  UpdateStats()

  if len(movements) > 0:
      label_result.config(
          text="All files loaded and merged | Airports: " + str(len(airports)) +
               " | Movements: " + str(len(movements)) +
               " | Departures: " + str(len(departures))
      )
  else:
      label_result.config(
          text="All files loaded | Airports: " + str(len(airports)) +
               " | Flights: " + str(len(aircrafts)) +
               " | Departures: " + str(len(departures)) +
               " | Press Merge Movements"
      )


# Window
root = tk.Tk()
root.title("LEBL Airport Operations Dashboard - Version 4")
root.configure(bg=BG)
root.state("zoomed")

def StyleFrame(frame):
  frame.configure(bg=PANEL, fg=TEXT, font=FONT_SECTION, padx=12, pady=12)

def StyleLabel(label):
  label.configure(bg=PANEL, fg=MUTED, font=FONT_NORMAL)

def StyleButton(button):
  button.configure(
      bg=BLUE,
      fg="white",
      font=FONT_BUTTON,
      relief="flat",
      padx=6,
      pady=3,
      width=14,
      activebackground="#1D4ED8",
      activeforeground="white",
      borderwidth=0
  )

def StyleSecondaryButton(button):
  button.configure(
      bg="#475569",
      fg="white",
      font=FONT_BUTTON,
      relief="flat",
      padx=6,
      pady=3,
      width=14,
      activebackground="#334155",
      activeforeground="white",
      borderwidth=0
  )

def StyleEntry(entry):
  entry.configure(
      bg="#334155",
      fg=TEXT,
      insertbackground=TEXT,
      relief="flat",
      font=FONT_NORMAL
  )

def StyleListbox(listbox):
  listbox.configure(
      bg="#020617",
      fg=TEXT,
      selectbackground=BLUE,
      selectforeground="white",
      relief="flat",
      font=("Consolas", 10)
  )

# Main title
title_label = tk.Label(
  root,
  text="LEBL AIRPORT OPERATIONS DASHBOARD",
  bg=BG,
  fg=TEXT,
  font=FONT_TITLE
)

title_label.grid(row=0, column=0, columnspan=2, pady=4, sticky="w", padx=8)
button_load_all = tk.Button(root, text="Load All Files", command=LoadAllButton)
button_load_all.grid(row=0, column=2, padx=8, pady=4, sticky="e")
StyleButton(button_load_all)

stats_label = tk.Label(
  root,
  text="Airports.txt: 0     Flights: 0     Occupied Gates: 0     Free Gates: 0",
  bg=BG,
  fg="#CBD5E1",
  font=("Segoe UI", 9)
)

stats_label.grid(row=1, column=0, columnspan=3, pady=(0,4))

root.grid_columnconfigure(0, minsize=380, weight=1)
root.grid_columnconfigure(1, minsize=480, weight=2)
root.grid_columnconfigure(2, minsize=260, weight=1)

# Frames
frame_airports = tk.LabelFrame(root, text=" Airports.txt ", bg=PANEL, fg=TEXT, font=FONT_SECTION)
frame_airports.grid(row=2, column=0, padx=8, pady=6, sticky="nsew")

frame_flights = tk.LabelFrame(root, text=" Flights and Movements ", bg=PANEL, fg=TEXT, font=FONT_SECTION)
frame_flights.grid(row=2, column=1, padx=8, pady=6, sticky="nsew")

frame_gates = tk.LabelFrame(root, text=" LEBL Gates - Version 4 ", bg=PANEL, fg=TEXT, font=FONT_SECTION)
frame_gates.grid(row=2, column=2, padx=8, pady=6, sticky="nsew")

frame_details = tk.LabelFrame(root, text=" Details / Event Log ", bg=PANEL, fg=TEXT, font=FONT_SECTION)
frame_details.grid(row=3, column=0, columnspan=3, padx=8, pady=6, sticky="nsew")

# Listboxes s'expandeixen per omplir l'espai disponible
frame_airports.grid_rowconfigure(6, weight=1)
frame_airports.grid_columnconfigure(0, weight=1)
frame_airports.grid_columnconfigure(1, weight=1)
frame_airports.grid_columnconfigure(2, weight=1)

frame_flights.grid_rowconfigure(7, weight=1)
frame_flights.grid_columnconfigure(0, weight=1)
frame_flights.grid_columnconfigure(1, weight=1)
frame_flights.grid_columnconfigure(2, weight=1)

frame_gates.grid_rowconfigure(4, weight=1)
frame_gates.grid_columnconfigure(0, weight=1)
frame_gates.grid_columnconfigure(1, weight=1)
frame_gates.grid_columnconfigure(2, weight=1)

root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=0)

# Airports.txt
label = tk.Label(frame_airports, text="Load airports file:")
label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_file = tk.Entry(frame_airports, width=20)
entry_file.grid(row=0, column=1, padx=5, pady=3)
entry_file.insert(0, "Airports.txt")
StyleEntry(entry_file)

button = tk.Button(frame_airports, text="Load Airports.txt", command=LoadButton)
button.grid(row=0, column=2, padx=5, pady=3)
StyleButton(button)

label = tk.Label(frame_airports, text="ICAO:")
label.grid(row=1, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_code = tk.Entry(frame_airports, width=10)
entry_code.grid(row=1, column=1, padx=5, pady=3)
StyleEntry(entry_code)

label = tk.Label(frame_airports, text="Latitude:")
label.grid(row=2, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_lat = tk.Entry(frame_airports, width=10)
entry_lat.grid(row=2, column=1, padx=5, pady=3)
StyleEntry(entry_lat)

label = tk.Label(frame_airports, text="Longitude:")
label.grid(row=3, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_lng = tk.Entry(frame_airports, width=10)
entry_lng.grid(row=3, column=1, padx=5, pady=3)
StyleEntry(entry_lng)

button = tk.Button(frame_airports, text="Add Airport", command=AddButton)
button.grid(row=4, column=0, padx=5, pady=3)
StyleButton(button)

button = tk.Button(frame_airports, text="Remove Airport", command=RemoveButton)
button.grid(row=4, column=1, padx=5, pady=3)
StyleButton(button)

button = tk.Button(frame_airports, text="Set Schengen", command=SetSchengenButton)
button.grid(row=4, column=2, padx=5, pady=3)
StyleButton(button)

label = tk.Label(frame_airports, text="Save airports file:")
label.grid(row=5, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_save = tk.Entry(frame_airports, width=20)
entry_save.grid(row=5, column=1)

entry_save.insert(0, "SchengenAirports.txt")
StyleEntry(entry_save)

button = tk.Button(frame_airports, text="Save Schengen", command=SaveButton)
button.grid(row=5, column=2, padx=5, pady=3)
StyleSecondaryButton(button)
button = tk.Button(frame_airports, text="Plot Airports.txt", command=PlotButton)
button.grid(row=9, column=0, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_airports, text="Map Airports.txt", command=MapButton)
button.grid(row=9, column=1, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_airports, text="Show Selected Airport", command=ShowSelectedAirportButton)
button.grid(row=9, column=2, padx=5, pady=3)
StyleSecondaryButton(button)

listbox_airports = tk.Listbox(frame_airports, width=65, height=8)
listbox_airports.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=4, pady=2)
StyleListbox(listbox_airports)

# Flights
label = tk.Label(frame_flights, text="Load arrivals file:")
label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_arrivals_file = tk.Entry(frame_flights, width=20)
entry_arrivals_file.grid(row=0, column=1, padx=5, pady=3)
entry_arrivals_file.insert(0, "Arrivals.txt")
StyleEntry(entry_arrivals_file)

button = tk.Button(frame_flights, text="Load Arrivals", command=LoadArrivalsButton)
button.grid(row=0, column=2, padx=5, pady=3)
StyleButton(button)

label = tk.Label(frame_flights, text="Load departures file:")
label.grid(row=1, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_departures_file = tk.Entry(frame_flights, width=20)
entry_departures_file.grid(row=1, column=1, padx=5, pady=3)
entry_departures_file.insert(0, "Departures.txt")
StyleEntry(entry_departures_file)

button = tk.Button(frame_flights, text="Load Departures", command=LoadDeparturesButton)
button.grid(row=1, column=2, padx=5, pady=3)
StyleButton(button)

button = tk.Button(frame_flights, text="Merge Movements", command=MergeMovementsButton)
button.grid(row=2, column=0, padx=5, pady=3)
StyleSecondaryButton(button)

label = tk.Label(frame_flights, text="Save flights file:")
label.grid(row=3, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_arrivals_save = tk.Entry(frame_flights, width=20)
entry_arrivals_save.grid(row=3, column=1, padx=5, pady=3)
entry_arrivals_save.insert(0, "output_arrivals.txt")
StyleEntry(entry_arrivals_save)

button = tk.Button(frame_flights, text="Save Flights", command=SaveFlightsButton)
button.grid(row=3, column=2, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_flights, text="Plot Arrivals", command=PlotArrivalsButton)
button.grid(row=4, column=0, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_flights, text="Plot Airlines", command=PlotAirlinesButton)
button.grid(row=4, column=1, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_flights, text="Plot Flights Type", command=PlotFlightsTypeButton)
button.grid(row=4, column=2, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_flights, text="Map Flights", command=MapFlightsButton)
button.grid(row=5, column=0, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_flights, text="Filter Long Distance", command=ShowLongDistanceButton)
button.grid(row=5, column=1, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_flights, text="Show Selected Flight", command=ShowSelectedAircraftButton)
button.grid(row=5, column=2, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_flights, text="Emissions", command=EmissionsButton)
button.grid(row=6, column=0, padx=5, pady=3)
StyleSecondaryButton(button)

listbox_aircrafts = tk.Listbox(frame_flights, width=75, height=8)
listbox_aircrafts.grid(row=7, column=0, columnspan=3, sticky="nsew", padx=4, pady=2)
StyleListbox(listbox_aircrafts)

# Gates
label = tk.Label(frame_gates, text="LEBL file:")
label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_lebl_file = tk.Entry(frame_gates, width=16)
entry_lebl_file.grid(row=0, column=1, padx=5, pady=3)
entry_lebl_file.insert(0, "LEBL.txt")
StyleEntry(entry_lebl_file)

button = tk.Button(frame_gates, text="Load LEBL", command=LoadLEBLButton)
button.grid(row=0, column=2, padx=5, pady=3)
StyleButton(button)

button = tk.Button(frame_gates, text="Assign All Gates", command=AssignGatesButton)
button.grid(row=1, column=0, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_gates, text="Assign Night Gates", command=AssignNightGatesButton)
button.grid(row=1, column=1, padx=5, pady=3)
StyleSecondaryButton(button)

label = tk.Label(frame_gates, text="Hour:")
label.grid(row=2, column=0, padx=5, pady=3, sticky="w")
StyleLabel(label)

entry_hour = tk.Entry(frame_gates, width=10)
entry_hour.grid(row=2, column=1, padx=5, pady=3)
entry_hour.insert(0, "04:00")
StyleEntry(entry_hour)

button = tk.Button(frame_gates, text="Assign At Hour", command=AssignGatesAtHourButton)
button.grid(row=2, column=2, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_gates, text="Show Gate", command=ShowSelectedGateButton)
button.grid(row=3, column=0, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_gates, text="Plot Gates", command=PlotGateOccupancyButton)
button.grid(row=3, column=1, padx=5, pady=3)
StyleSecondaryButton(button)

button = tk.Button(frame_gates, text="Plot Day", command=PlotDayOccupancyButton)
button.grid(row=3, column=2, padx=5, pady=3)
StyleSecondaryButton(button)

listbox_gates = tk.Listbox(frame_gates, width=55, height=8)
listbox_gates.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=4, pady=2)
StyleListbox(listbox_gates)

# Details
text_output = tk.Text(
  frame_details,
  width=160,
  height=5,
  bg="#020617",
  fg=TEXT,
  insertbackground=TEXT,
  relief="flat",
  font=("Consolas", 10)
)

text_output.insert(
  tk.END,
  "LEBL AIRPORT OPERATIONS DASHBOARD\n\n"
  "Select an airport, flight or gate to display detailed information."
)

text_output.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

status_label = tk.Label(
  frame_details,
  text="Ready",
  bg=PANEL,
  fg=GREEN,
  font=("Segoe UI", 10, "bold")
)

status_label.grid(row=1, column=0, sticky="w", padx=5, pady=3)
label_result = status_label

root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=4)
root.grid_columnconfigure(2, weight=3)

root.grid_rowconfigure(2, weight=3)
root.grid_rowconfigure(3, weight=1)

root.mainloop()
