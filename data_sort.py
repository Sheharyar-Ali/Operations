file = open("Operations_data.csv", "r")
Transfer_time = []
Arr = []
Dep = []
Span = []
ArrInt = []
DepInt = []
Pax = []
for lines in file.readlines():
    lines = lines[:-1]
    columns = lines.split(",")
    Transfer_time.append(columns[0].strip())
    Arr.append(columns[1].strip())
    Dep.append(columns[2].strip())
    Span.append(columns[3].strip())
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
for i in range(0,len(DepInt)):
    if DepInt[i] == 1 or ArrInt[i] ==1:
        DepInt[i] = 1
        ArrInt[i] = 1



# Calculating time spent on ground in minutes
for i in range(0, len(Transfer_time)):
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


