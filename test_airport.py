from airports import *   # o "from airports import *"

# 🔹 carregar aeroports del fitxer
airports = LoadAirports("Airports.txt")

print("Total airports carregats:", len(airports))
print()

# 🔹 mostrar-los
for airport in airports:
    PrintAirport(airport)
    print()

# 🔹 provar Schengen
print("---- Afegint Schengen ----")
for airport in airports:
    SetSchengen(airport)
    PrintAirport(airport)
    print()

print("Total ara:", len(airports))

print("---- Eliminant aeroport ----")

RemoveAirport(airports, "LEBL")

print("Total ara:", len(airports))