from data_sort import Transfer_time, Arr, Dep, ArrInt, DepInt, Pax, Type, ac_types
import numpy as np


class x:
    def __init__(self, i, j, k):
        self.i = i  # international or not
        self.j = j  # Type of aircraft
        self.k = k  # Assigned to gate


class g:
    def __init__(self, i, j, k, l):
        self.i = i  # Type of aircraft it can support
        self.j = j  # Type (I,N,R,S)
        self.k = k  # Does it have a bridge ( 1= yes , 0 = no)
        self.l = l  # flight that it is assigned to


F = []  # collection of pending flights
Fd = []  # collection of single flights

### Filling F and Fd with the x class
for i in range(0, len(Type)):
    Class = x(ArrInt[i], Type[i], 0)
    if Transfer_time[i] != 0:
        F.append(Class)
    else:
        Fd.append(Class)
        F.append(Class)

####################### Sorting out gates ############
# total of 83 gates
Gates = []
gate_types = {
    "I": "1",
    "N": "2",
    "R": "3",
    "S": "4"
}
#### Reading gate data ##########
file = open("Gate_data.csv", "r")
for lines in file.readlines():
    lines = lines[:-1]
    columns = lines.split(",")
    gate = g(1, 1, 1, 1)
    number = int(columns[1].strip())
    aircraft_type = columns[0][0].strip()
    for words, replacement in ac_types.items():
        aircraft_type = aircraft_type.replace(words, replacement)
    gate.i = int(aircraft_type)  # Assigning aircraft type
    gate_type = columns[0][1].strip()
    for words, replacement in gate_types.items():
        gate_type = gate_type.replace(words, replacement)
    gate.j = int(gate_type)  # assigning gate type
    if gate_type == 3:  # seeing if it has a bridge or not
        gate.k = 0
    else:
        gate.k = 1
    for i in range(0, number):
        Gates.append(gate)
print(len(Gates))
