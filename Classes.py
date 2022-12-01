from data_sort import Transfer_time, Arr, Dep, ArrInt, DepInt, Pax, Type


class x:
    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k


F = []  # collection of pending flights
Fd = []  # collection of single flights

for i in range(0, len(Type)):
    Class = x(ArrInt[i], Type[i], 0)
    if Transfer_time[i] != 0:
        F.append(Class)
    else:
        Fd.append(Class)
        F.append(Class)