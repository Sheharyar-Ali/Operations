import pandas as pd

file = open("Operations_data.csv", "r")
Name = []
Transfer_time = []
Arr = []
Dep = []
Type = []
ArrInt = []
DepInt = []
Pax = []


for lines in file.readlines():
    lines = lines[:-1]
    columns = lines.split(",")
    Transfer_time.append(columns[0].strip())
    Arr.append(columns[1].strip())
    Dep.append(columns[2].strip())
    Type.append(columns[3].strip())
    ArrInt.append(columns[4].strip())
    DepInt.append(columns[5].strip())
    Pax.append(int(columns[6].strip()))

# Fixing ArrInt and DepInt
for i in range(0, len(ArrInt)):
    if ArrInt[i] == "":
        ArrInt[i] = 0
    elif ArrInt[i] == "1":
        ArrInt[i] = 1
for i in range(0, len(DepInt)):
    if DepInt[i] == "":
        DepInt[i] = 0
    elif DepInt[i] == "1":
        DepInt[i] = 1
for i in range(0, len(DepInt)):
    if DepInt[i] == 1 or ArrInt[i] == 1:
        DepInt[i] = 1
        ArrInt[i] = 1

# Calculating time spent on ground in minutes
for i in range(0, len(Transfer_time)):
    Name.append(i+1)
    Value = Transfer_time[i]
    Time = (int(Value[0] + Value[1]) * 60) + (int(Value[-2] + Value[-1]))
    Transfer_time[i] = Time

## Filtering out overnight flights

for i in range(0, len(Dep)):
    ValArr = Arr[i]
    ValDep = Dep[i]
    ArrTime = int(ValArr[0] + ValArr[1])
    DepTime = int(ValDep[0] + ValDep[1])
    if ArrTime > DepTime:
        Dep[i] = "OO:OO"
        Transfer_time[i] = 0

## Changing aircraft types to numbers
ac_types={
    "A":"1",
    "B":"2",
    "C":"3",
    "D":"4",
    "E":"5",
    "F":"6",
    "M":"7"
}
for i in range(0,len(Type)):
    for word,replacement in ac_types.items():
        Type[i] = Type[i].replace(word,replacement)
    Type[i]= int(Type[i])

#Adding to pandas
aircraft_data = pd.DataFrame({}, columns=['Name','Arr', 'Dep','transfer_time','Type','Int?','Pax'])
aircraft_data['Name'] =Name
aircraft_data["Arr"] = Arr
aircraft_data['Dep'] = Dep
aircraft_data["transfer_time"] = Transfer_time
aircraft_data["Type"] = Type
aircraft_data["Int?"] = ArrInt
aircraft_data["Pax"] = Pax

#### Reading gate data ##########

AC_supported =[]
Gate_type = []
Bridge =[]
name = []
gate_types = {
    "I": "1",
    "N": "2",
    "R": "3",
    "S": "4"
}
file = open("Gate_data.csv", "r")

for lines in file.readlines():
    bridge_check=0
    lines = lines[:-1]
    columns = lines.split(",")
    number = int(columns[1].strip()) #Seeing how many of this gate exists
    aircraft_type = columns[0][0].strip()
    for words, replacement in ac_types.items():
        aircraft_type = (aircraft_type.replace(words, replacement))

    gate_type = columns[0][1].strip()
    for words, replacement in gate_types.items():
        gate_type = (gate_type.replace(words, replacement))
    if gate_type == 3:  # seeing if it has a bridge or not
        bridge_check = 0
    else:
        bridge_check = 1
    count = 0
    for i in range(0, number):
        gate_name = str(columns[0].strip() + str(count + 1))
        count+=1
        name.append(gate_name)
        AC_supported.append(int(aircraft_type))
        Gate_type.append(int(gate_type))
        Bridge.append(bridge_check)

Gates = pd.DataFrame({}, columns=['name', 'ac_supported', 'type', 'bridge?'])
Gates["name"] = name
Gates['ac_supported'] = AC_supported
Gates['type'] = Gate_type
Gates["bridge?"] = Bridge


## Compatible gates ##
compatible_gates = {}
for idx,rows in aircraft_data.iterrows():
    gates_list = Gates[Gates.ac_supported <= rows.Type].name.values
    compatible_gates[rows.Name] = gates_list


