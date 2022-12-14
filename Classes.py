from data_sort import Transfer_time, Arr, Dep, ArrInt, DepInt, Pax, Type, ac_types
import numpy as np


class x:
    def __init__(self, i, j, k, n, t, iden):
        self.ident = iden
        self.i = i  # international or not
        self.j = j  # Type of aircraft
        self.k = k  # Assigned to gate
        self.n = n  # number of passengers
        self.t = t  # transfer time


class g:
    def __init__(self, i, j, k, l, iden):
        self.ident = iden
        self.i = i  # Type of aircraft it can support
        self.j = j  # Type (I,N,R,S)
        self.k = k  # Does it have a bridge ( 1= yes , 0 = no)
        self.l = l  # flight that it is assigned to


F = []  # collection of pending flights
Fd = []  # collection of single flights

### Filling F and Fd with the x class
for i in range(0, len(Type)):
    Class = x(i=ArrInt[i], j=Type[i], k=0, n=0, t=0, iden=i)
    Class.n = Pax[i]
    Class.t = Transfer_time[i]
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
    gate = g(i=1, j=1, k=1, l=1, iden=0)
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
for i in range(0, len(Gates)):
    Gates[i].ident = i

##### Making compatible gates dataset ###############

compatible_gates = []
for i in range(0, len(F)):
    buffer = []
    type_aircraft = F[i].j
    for a in range(0, len(Gates)):
        gate_type = Gates[a].i
        if type_aircraft <= gate_type:
            buffer.append(Gates[a])
    compatible_gates.append(buffer)
