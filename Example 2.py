# %matplotlib inline
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
from data_sort import aircraft_data, Gates,compatible_gates

## Model F - Explicit Desires (want a certain terminal) #######

# 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost
#
# # 1. Objective Function (ignore for now)
# prob += 0

# Gu#
opt_model = gp.Model(name="MIP Model")
objective = 0
objective += 0
opt_model.ModelSense = gp.GRB.MINIMIZE
opt_model.setObjective(objective)

###Extra code to avoid compilation error while testing
########################################################################################################################

# turns = pd.DataFrame({
#     'Name': [1, 2, 3, 4, 5],  # aircraft number
#     'from_country': ['GB', 'GB', 'US', 'TR', 'RU'],  # arrival country
#     'to_country': ['CZ', 'CZ', 'CZ', 'FR', 'FR'],  # departure country
#     'plane_size': [2, 3, 2, 1, 1]  # size delegation
# }, columns=['Name', 'plane_size', 'from_country', 'to_country'])

# Gates = pd.DataFrame({
#     'terminal': ['A', 'A', 'A', 'B', 'C', 'C'],
#     'gate': ['A1', 'A2', 'A3', 'B1', 'C1', 'C2'],
#     'max_size': [3, 1, 2, 3, 1, 1]
# }, columns=['terminal', 'gate', 'max_size'])

# turns = pd.DataFrame({
#     'Name': [1, 2, 3, 4, 5],
#     'from_country': ['GB', 'GB', 'US', 'TR', 'RU'],
#     'to_country': ['CZ', 'CZ', 'CZ', 'FR', 'FR'],
#     'plane_size': [2, 3, 2, 1, 1]
# }, columns=['Name', 'plane_size', 'from_country', 'to_country'])

# Gates = pd.DataFrame({
#     'terminal': ['A', 'A', 'A', 'B', 'C', 'C'],
#     'gate': ['A1', 'A2', 'A3', 'B1', 'C1', 'C2'],
#     'max_size': [3, 1, 2, 3, 1, 1]
# }, columns=['terminal', 'gate', 'max_size'])

print(Gates)
# print(turns)

ac_list = aircraft_data.Name.values
print("Turns to allocate: ", ac_list)

gate_list = Gates.name.values
print("Available gates: ", gate_list)

# # Let's add some more flights
# extra_flights = pd.DataFrame({
#     'Name': [6, 7, 8, 9, 10],
#     'from_country': ['FR', 'CZ', 'US', 'FR', 'RU'],
#     'to_country': ['GB', 'GB', 'GB', 'FR', 'RU'],
#     'plane_size': [1, 3, 1, 1, 1]
# }, columns=['Name', 'plane_size', 'from_country', 'to_country'])
#
# # aircraft_data = turns.append(extra_flights, ignore_index = True) #depreciated
# aircraft_data = pd.concat([turns, extra_flights])
#
# # Add some flight-times
# aircraft_data['Arr'] = pd.to_datetime([
#     "02/01/2016 06:05",
#     "02/01/2016 06:05",
#     "02/01/2016 09:10",
#     "02/01/2016 09:10",
#     "02/01/2016 09:10",
#     "02/01/2016 12:15",
#     "02/01/2016 12:15",
#     "02/01/2016 15:20",
#     "02/01/2016 16:20",
#     "02/01/2016 16:30"])
#
# aircraft_data['Dep'] = pd.to_datetime([
#     "02/01/2016 07:05",
#     "02/01/2016 09:05",
#     "02/01/2016 15:10",
#     "02/01/2016 13:10",
#     "02/01/2016 17:10",
#     "02/01/2016 15:15",
#     "02/01/2016 15:15",
#     "02/01/2016 21:20",
#     "02/01/2016 21:20",
#     "02/01/2016 17:30"])
#
# print("------------here now-------")
# print(aircraft_data)
# print("------------here now-------")

ac_list = aircraft_data.Name.values
print("New turns to allocate: ", ac_list)


# compatible_gates = {}  # replace with compatible gates list
# for idx, row in aircraft_data.iterrows():
#     gates_lst = Gates[airport.max_size >= row.plane_size].gate.values
#     compatible_gates[row.Name] = gates_lst
#
# print("Compatible gates for each turn")
# for k, v in compatible_gates.items():
#     print(k, v)


occupancy = pd.DataFrame({
    'gate': ['A3', 'A2'],
    'occupied_from': pd.to_datetime(["02/01/2016 15:15", "02/01/2016 13:15"]),
    'occupied_to': pd.to_datetime(["02/01/2016 19:15", "02/01/2016 14:15"]),
}, columns=['gate', 'occupied_from', 'occupied_to'])

###############################################################################################33


# 2. Variable: x[i,j] = (0,1)
# Binary = turn_i allocated to gate_j

x = {}
## IMPORTANT: Didnot make the following list in the previous example
# as it was not necessary.
# But here we might need it to cal
constraints_list = {}  # initializing a list for constraints

for t in ac_list:
    # For compatible gates
    for g in compatible_gates[t]:  # for every compatible gate for plane t
        if g in occupancy['gate'].values:  # if gate is in occupancy list
            t_dep = aircraft_data.loc[aircraft_data['Name'] == t, 'Dep'].values[
                0]  # get the departure time for flight t
            t_arr = aircraft_data.loc[aircraft_data['Name'] == t, 'Arr'].values[0]  # get the arrival time for flight t
            oc_from = occupancy.loc[occupancy['gate'] == g, 'occupied_from'].values[
                0]  # get when gate g is occupied from
            oc_to = occupancy.loc[occupancy['gate'] == g, 'occupied_to'].values[0]  # get when gate g is occupied to

            if (oc_to >= t_arr) and (oc_from <= t_dep):
                continue

        # Gate not occupied so create variable
        # x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)
        # x[t,g] = opt_model.addVar(Vtype=gp.GRB.BINARY, name = "t%i_g%s".format(t, g))

# 3. Constraints
# i. Each turn must be assigned to one compatible gate
for t in ac_list:
    # prob += lpSum(x[t, g] for g in gate_list if (t, g) in x) == 1
    constraints_list += opt_model.addConstrs((gp.quicksum(x[t, g] for g in gate_list if (t, g) in x) == 1))


# ii. Gates cannot have more than one turn/plane per time_bucket
for idx, row in heatmapdf.iterrows():
    # Get all the turns for time-bucket
    turns_in_time_bucket = set(dict(row[row == 1]).keys())
    # For all gates
    for g in gate_list:
        # Constraints may be blank
        cons = [x[t, g] for t in turns_in_time_bucket if (t, g) in x]
        if len(cons) > 1:
            # constraint_for_time_bucket = lpSum(cons) <= 1
            # Gu#
            constraint_for_time_bucket = opt_model.addConstr((gp.quicksum(cons) <= 1))

        # prob += constraint_for_time_bucket
        constraint_for_time_bucket += constraint_for_time_bucket

# Imagine we really like the E terminal and would prefer to use those gates
# Add all turns under those gates with a negative cost coefficient
neg_cost_coefficient = -5
# prob += lpSum(neg_cost_coefficient*x[t, g] for t, g in x if g.startswith('E'))
constraints_list += opt_model.addConstrs(gp.quicksum(neg_cost_coefficient * x[t, g] for t, g in x if g.startswith('E')))

# Solve
# prob.solve()

opt_model.optimize()

# Report
# print("Status: ", LpStatus[prob.status])
# print("Minimised Cost: ", value(prob.objective))

# We only get the desired 'E' gates
for alloc in x:
    # if x[alloc].varValue:
    if x[alloc].X:
        print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))

    # Visualise outcome
# plot_gantt_chart(aircraft_data, x)


## Model G - Minimise number of gates (Max Function) #######

# # 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost
#
# # 1. Objective Function (ignore for now)
# prob += 0

# 2. Variable: x[i,j] = (0,1)
# Binary = turn_i allocated to gate_j

x = {}
for t in ac_list:
    # For compatible gates
    for g in compatible_gates[t]:
        if g in occupancy.gate.values:
            # if g in occupancy.gate.get_values():

            t_dep = aircraft_data.loc[aircraft_data['Name'] == t, 'Dep'].values[0]
            t_arr = aircraft_data.loc[aircraft_data['Name'] == t, 'Arr'].values[0]
            oc_from = occupancy.loc[occupancy['gate'] == g, 'occupied_from'].values[0]
            oc_to = occupancy.loc[occupancy['gate'] == g, 'occupied_to'].values[0]

            if (oc_to >= t_arr) and (oc_from <= t_dep):
                continue

        # Gate not occupied so create variable
        # x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)
        x[t, g] = opt_model.addVar(Vtype=gp.GRB.BINARY, name="t%i_g%s".format(t, g))

# 3. Constraints
# i. Each turn must be assigned to one compatible gate
for t in ac_list:
    # prob += lpSum(x[t, g] for g in gate_list if (t, g) in x) == 1
    constraints_list += opt_model.addConstrs((gp.quicksum(x[t, g] for g in gate_list if (t, g) in x) == 1))

# ii. Gates cannot have more than one turn/plane per time_bucket
for idx, row in heatmapdf.iterrows():
    # Get all the turns for time-bucket
    turns_in_time_bucket = set(dict(row[row == 1]).keys())
    # For all gates
    for g in gate_list:
        # Constraints may be blank
        cons = [x[t, g] for t in turns_in_time_bucket if (t, g) in x]
        if len(cons) > 1:
            # constraint_for_time_bucket = lpSum(cons) <= 1

            # Gu#
            constraint_for_time_bucket = opt_model.addConstr((gp.quicksum(cons) <= 1))
            # These will occur when the plane overlaps change

            # prob += constraint_for_time_bucket
            constraint_for_time_bucket += constraint_for_time_bucket

gate_used_max = {}  # Dictionary to hold new variables

# Create the new variables
for g in gate_list:
    # gate_used_max[g] = LpVariable("gate_%s_used" % g, 0, 1, LpBinary)
    gate_used_max[g] = opt_model.addVar(Vtype=gp.GRB.BINARY, name="gate_%s_used".format(g))
    # Gate_A1_used = max(turn_1_to_A1, turn_2_to_A1, turn_3_to_A1, ...)
    # Set lower-bound
    for t in ac_list:
        if (t, g) in x:
            # prob += gate_used_max[g] >= x[t, g]
            constraints_list += gate_used_max[g] >= x[t, g]
    # Set upper-bound
    # prob += gate_used_max[g] <= lpSum(x[t, g] for t in ac_list if (t, g) in x)
    constraints_list += gate_used_max[g] <= opt_model.addConstr(gp.quicksum(x[t, g] for t in ac_list if (t, g) in x))

# Add with positive coefficient to objective
pos_cost_coeff = 5
# max_gates = lpSum(pos_cost_coeff * gate_used_max[g] for g in gate_used_max)
max_gates = opt_model.addConstr(gp.quicksum(pos_cost_coeff * gate_used_max[g] for g in gate_used_max))

print(max_gates)

# prob += max_gates
constraints_list += max_gates

# Solve
# prob.solve()

# # Report
# print("Status: ", LpStatus[prob.status])
# print("Minimised Cost: ", value(prob.objective))

for alloc in x:
    if x[alloc].varValue:  # replace .varValue by X if the code gives error here
        print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))

# This example uses just 5 gates (E5, A1, E9, E3, E10)
# plot_gantt_chart(aircraft_data, x)


## Model H - Maximise number of gates (Max Function) ##

## NOTE: The code correction is almost the same as the above, please cooperate and refer above

# # 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost
#
# # 1. Objective Function (ignore for now)
# prob += 0
#
# # 2. Variable: x[i,j] = (0,1)
# # Binary = turn_i allocated to gate_j
# x = {}
# for t in ac_list:
#     # For compatible gates
#     for g in compatible_gates[t]:
#         if g in occupancy.gate.get_values():
#
#             t_dep = aircraft_data.loc[aircraft_data['Name'] == t, 'Dep'].values[0]
#             t_arr = aircraft_data.loc[aircraft_data['Name'] == t, 'Arr'].values[0]
#             oc_from = occupancy.loc[occupancy['gate'] == g, 'occupied_from'].values[0]
#             oc_to = occupancy.loc[occupancy['gate'] == g, 'occupied_to'].values[0]
#
#             if (oc_to >= t_arr) and (oc_from <= t_dep):
#                 continue
#
#         # Gate not occupied so create variable
#         x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)
#
# # 3. Constraints
# # i. Each turn must be assigned to one compatible gate
# for t in ac_list:
#     prob += lpSum(x[t, g] for g in gate_list if (t, g) in x) == 1
#
# # ii. Gates cannot have more than one turn/plane per time_bucket
# for idx, row in heatmapdf.iterrows():
#     # Get all the turns for time-bucket
#     turns_in_time_bucket = set(dict(row[row == 1]).keys())
#     # For all gates
#     for g in gate_list:
#         # Constraints may be blank
#         cons = [x[t, g] for t in turns_in_time_bucket if (t, g) in x]
#         if len(cons) > 1:
#             constraint_for_time_bucket = lpSum(cons) <= 1
#             # These will occur when the plane overlaps change
#             prob += constraint_for_time_bucket
#
# gate_used_max = {}  # Dictionary to hold new variables
#
# # Create the new variables
# for g in gate_list:
#     gate_used_max[g] = LpVariable("gate_%s_used" % g, 0, 1, LpBinary)
#     # Gate_A1_used = max(turn_1_to_A1, turn_2_to_A1, turn_3_to_A1, ...)
#     # Set lower-bound
#     for t in ac_list:
#         if (t, g) in x:
#             prob += gate_used_max[g] >= x[t, g]
#     # Set upper-bound
#     prob += gate_used_max[g] <= lpSum(x[t, g] for t in ac_list if (t, g) in x)
#
# # Add with negative coefficient to objective
# neg_cost_coeff = -5
# max_gates = lpSum(neg_cost_coeff * gate_used_max[g] for g in gate_used_max)
#
# prob += max_gates
#
# # Solve
# prob.solve()
#
# # Report
# print("Status: ", LpStatus[prob.status])
# print("Minimised Cost: ", value(prob.objective))
#
# for alloc in x:
#     if x[alloc].varValue:
#         print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))
#
#     # This example uses all different gates for different turns
# plot_gantt_chart(aircraft_data, x)
