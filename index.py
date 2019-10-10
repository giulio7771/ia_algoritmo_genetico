import numpy as np

def getPosition():
    return np.random.randint(20)

cities = []

for x in range(20):
  city = { "x": getPosition(), "y": getPosition() }
  cities.append(city)
  print("new city " + str(city.get("x")) + " - " + str(city.get("y")))