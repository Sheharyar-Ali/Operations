# %matplotlib inline
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB

turns = pd.DataFrame({
    'turn_no': [1, 2, 3, 4, 5],
    'from_country': ['GB', 'GB', 'US', 'TR', 'RU'],
    'to_country': ['CZ', 'CZ', 'CZ', 'FR', 'FR'],
    'plane_size': [2, 3, 2, 1, 1]
}, columns=['turn_no', 'plane_size', 'from_country', 'to_country'])

airport = pd.DataFrame({
    'terminal': ['A', 'A', 'A', 'B', 'C', 'C'],
    'gate': ['A1', 'A2', 'A3', 'B1', 'C1', 'C2'],
    'max_size': [3, 1, 2, 3, 1, 1]
}, columns=['terminal', 'gate', 'max_size'])

print(airport)
print(turns)

turn_list = turns.turn_no.values
print("Turns to allocate: ", turn_list)

gate_list = airport.gate.values
print("Available gates: ", gate_list)



########################
## Model A - Simple Static Model
########################


# 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost
# print("---------------------", prob)
# # 1. Objective Function (ignore for now)
# prob += 0

#Gu#
opt_model = gp.Model(name = "MIP Model")
objective = 0
objective +=0
opt_model.ModelSense = gp.GRB.MINIMIZE
opt_model.setObjective(objective)


# 2. Variable: x[i,j] = (0,1)
# Binary = turn_i allocated to gate_j
# x = {}
# for t in turn_list:
#     for g in gate_list:
#         x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)

#Gu#
x = {}
for t in turn_list:
    for g in gate_list:
        # x[t, g] = opt_model.addVar(vtype=gp.GRB.BINARY, name="t%i_g%s".format(t, g))
        x[t, g] = opt_model.addVar(vtype=gp.GRB.BINARY, name="t%i_g%s".format(t, g))



# 3. Constraints
# i. Each turn must be assigned to one gate
# for t in turn_list:
#     prob += lpSum(x[t, g] for g in gate_list) == 1
#
# # ii. Gates cannot have more than one turn/plane
# for g in gate_list:
#     prob += lpSum(x[t, g] for t in turn_list) <= 1

#Gu#

opt_model.addConstrs((gp.quicksum(x[t, g] for g in gate_list) == 1) for t in turn_list)
opt_model.addConstrs((gp.quicksum(x[t, g] for t in turn_list) <= 1) for g in gate_list)


# Formula
# print(prob)

#Gurobi Alternative to this#
opt_model.write("Output.lp")

# Solve
# prob.solve()


#Gu#
opt_model.optimize()

# Report
# print("Status: ", LpStatus[prob.status])
# print("Minimised Cost: ", value(prob.objective))

#Gu#
print("Model Status:",opt_model.Status)

# for alloc in x:
#     if x[alloc].varValue:
#         print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))

#Gu#
for alloc in x:
    if x[alloc].X:
        print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))





##Model B - Adding an Implicit Constraint (size of planes)#######

# Some gates may not be able to fit a plane
# Assume gate with max_size k can fit a plane_size of j <= k

compatible_gates = {}
for idx, row in turns.iterrows():
    gates_lst = airport[airport.max_size >= row.plane_size].gate.values
    compatible_gates[row.turn_no] = gates_lst

print("Compatible gates for each turn")
for k, v in compatible_gates.items():
    print(k, v)


################################
#Line 15 from Example - 1 Jupyter Github###
#############################


# 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost
#
# # 1. Objective Function (ignore for now)
# prob += 0

#Gu#
opt_model = gp.Model(name = "MIP Model")
objective = 0
opt_model.ModelSense = gp.GRB.MINIMIZE
opt_model.setObjective(objective)


# 2. Variable: x[i,j] = (0,1)
# Binary = turn_i allocated to gate_j
# x = {}
# for t in turn_list:
#     # The 'constraint' gets added implicitly by not creating a choice variable that
#     # connects turns to incompatible gates
#     # As opposed to adding it as a constraint
#     for g in compatible_gates[t]:
#         x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)


#Gu#
x = {}
for t in turn_list:
    for g in compatible_gates[t]:
        x[t, g] = opt_model.addVar(vtype=gp.GRB.BINARY, name="t%i_g%s".format(t, g))


# 3. Constraints
# i. Each turn must be assigned to one gate

# for t in turn_list:
#     prob += lpSum(x[t, g] for g in gate_list if (t, g) in x) == 1
#
# # ii. Gates cannot have more than one turn/plane
# for g in gate_list:
#     prob += lpSum(x[t, g] for t in turn_list if (t, g) in x) <= 1

#Gu#
opt_model.addConstrs((gp.quicksum(x[t, g] for g in gate_list if (t, g) in x) == 1) for t in turn_list)
opt_model.addConstrs((gp.quicksum(x[t, g] for t in turn_list if (t, g) in x) <= 1 ) for g in gate_list)


# Formula
# print(prob)

# Solve
# prob.solve()

#Gu#
opt_model.optimize()

# Report
# print("Status: ", LpStatus[prob.status])
# print("Minimised Cost: ", value(prob.objective))

#Gu#
print("Model Status:",opt_model.Status)


# for alloc in x:
#     if x[alloc].varValue:
#         print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))

#Gu#
for alloc in x:
    if x[alloc].X:
        print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))





## Model C - Adding a Time Dimension #######

# Let's add some more flights
extra_flights = pd.DataFrame({
    'turn_no':[6,7,8,9,10],
    'from_country':['FR','CZ','US','FR','RU'],
    'to_country':['GB','GB','GB','FR','RU'],
    'plane_size':[1,3,1,1,1]
    }, columns=['turn_no', 'plane_size', 'from_country', 'to_country'])

# turns2 = turns.append(extra_flights, ignore_index = True) #depreciated
turns2 = pd.concat([turns,extra_flights])

# Add some flight-times
turns2['inbound_arrival'] = pd.to_datetime([
        "02/01/2016 06:05",
        "02/01/2016 06:05",
        "02/01/2016 09:10",
        "02/01/2016 09:10",
        "02/01/2016 09:10",
        "02/01/2016 12:15",
        "02/01/2016 12:15",
        "02/01/2016 15:20",
        "02/01/2016 16:20",
        "02/01/2016 16:30"])

turns2['outbound_departure'] = pd.to_datetime([
        "02/01/2016 07:05",
        "02/01/2016 09:05",
        "02/01/2016 15:10",
        "02/01/2016 13:10",
        "02/01/2016 17:10",
        "02/01/2016 15:15",
        "02/01/2016 15:15",
        "02/01/2016 21:20",
        "02/01/2016 21:20",
        "02/01/2016 17:30"])

print("------------here now-------")
print(turns2)
print("------------here now-------")

turn_list = turns2.turn_no.values
print("New turns to allocate: ", turn_list)

compatible_gates = {}
for idx, row in turns2.iterrows():
    gates_lst = airport[airport.max_size >= row.plane_size].gate.values
    compatible_gates[row.turn_no] = gates_lst

print("Compatible gates for each turn")
for k, v in compatible_gates.items():
    print(k, v)




## HeatMap Plotting Code #######

# Let's see how many planes we have at any one time
# We want to reshape our data to have an index of e.g 5 min intervals
# Columns are binary variables corresponding to whether the turn is at the airport

# Using discrete time-buckets
min_bucket = 5

# Create time-series between arrival of first plane and departure of last
time_series = pd.Series(True, index=pd.date_range(
    start=turns2.inbound_arrival.min(),
    end=turns2.outbound_departure.max(),
    freq=pd.offsets.Minute(min_bucket)))


# Truncate full time-series to [inbound_arrival, outbound_departure]
def trunc_ts(series):
    return time_series.truncate(series['inbound_arrival'], series['outbound_departure'])


heatmapdf = turns2.apply(trunc_ts, axis=1).T

# Convert columns from index to turn_no
heatmapdf.columns = turns2['turn_no'].values
# Cast to integer
heatmapdf = heatmapdf.fillna(0).astype(int)
heatmapdf.index = heatmapdf.index.time

heatmapdf.head()

# Only care about overlaps
# If gate only has one turn then don't need constraint that it must have one turn ...
heatmapdf['tot'] = heatmapdf.sum(axis=1)
heatmapdf = heatmapdf[heatmapdf.tot > 1]
heatmapdf.drop(['tot'], axis=1, inplace=True)
heatmapdf.head()

# Plot the turns in the airport
sns.set()
plt.figure(figsize=(20, 10))

snsdf = heatmapdf.T
g = sns.heatmap(snsdf, rasterized=True, xticklabels=10, linewidths=1)
# plt.show()

# We don't need duplicate constraints (at different time buckets)
heatmapdf = heatmapdf.drop_duplicates()
heatmapdf.head()



################################
#Line 18 from Example - 1 Jupyter Github###
#############################

# 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost
#
# # 1. Objective Function (ignore for now)
# prob += 0

# 2. Variable: x[i,j] = (0,1)
# Binary = turn_i allocated to gate_j
x = {}
# for t in turn_list:
#     for g in compatible_gates[t]:
#         x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)

x = {}
for t in turn_list:
    for g in compatible_gates[t]:
        x[t, g] = opt_model.addVar(vtype=gp.GRB.BINARY, name="t%i_g%s".format(t, g))

# 3. Constraints
# i. Each turn must be assigned to one (compatible) gate
# for t in turn_list:
#     prob += lpSum(x[t, g] for g in gate_list if (t, g) in x) == 1

opt_model.addConstrs((gp.quicksum(x[t, g] for g in gate_list if (t,g) in x) == 1) for t in turn_list)


################################
#Line 19 from Example - 1 Jupyter Github###
#############################

#We can relax the constraint
# ii. Gates cannot have more than one turn/plane per time_bucket
for idx, row in heatmapdf.iterrows():
    # Get all the turns for time-bucket
    turns_in_time_bucket = set(dict(row[row==1]).keys())
    # For all gates
    for g in gate_list:
        # Constraints may be blank
        cons = [x[t, g] for t in turns_in_time_bucket if (t, g) in x]
        # Only need to impose constraint if there is an overlap
        if len(cons) > 1:

            # constraint_for_time_bucket = lpSum(cons) <= 1
            constraint_for_time_bucket = opt_model.addConstr((gp.quicksum(cons) <= 1))

            # These will occur when the plane overlaps change
            print(row.name, ":", constraint_for_time_bucket)
            # prob += constraint_for_time_bucket
            #Gu#
            #Need to make a list adding all the constraints to if you add the above line

################################
#Line 21 from Example - 1 Jupyter Github###
#############################


# Create a function that we can call to visualise
def plot_gantt_chart(allocated_turns, lp_variable_outcomes, min_bucket=5):
    # Assign gate
    for alloc in lp_variable_outcomes:
        if lp_variable_outcomes[alloc].varValue: #(Previously had to change varValue to "X" in lines 204 & 109)
            allocated_turns.set_value(allocated_turns['turn_no'] == alloc[0], 'gate', alloc[-1])

    # Create time-series between arrival of first plane and departure of last
    time_series = pd.Series(True, index=pd.date_range(
        start=turns2.inbound_arrival.min(),
        end=turns2.outbound_departure.max(),
        freq=pd.offsets.Minute(min_bucket)))

    # Truncate full time-series to [inbound_arrival, outbound_departure]
    def trunc_ts(series):
        return time_series.truncate(series['inbound_arrival'], series['outbound_departure'])

    # Allocations heat-map
    allocheatmapdf = allocated_turns.apply(trunc_ts, axis=1).T
    allocheatmapdf.columns = allocated_turns['turn_no'].get_values()
    allocheatmapdf = allocheatmapdf.fillna(0).astype(int)
    allocheatmapdf.index = allocheatmapdf.index.time

    # Replace values with col-names
    for col in list(allocheatmapdf.columns):
        allocheatmapdf.loc[allocheatmapdf[col] > 0, col] = col

    # Columns are now stands
    allocheatmapdf.columns = allocated_turns['gate'].get_values()
    trans = allocheatmapdf.T

    # These will never overlap given the constraints
    plt_df = trans.groupby(trans.index).sum()

    # Plot
    sns.set()
    plt.figure(figsize=(20, 10))
    g = sns.heatmap(plt_df, xticklabels=10, cmap='nipy_spectral')


    # Plot turn-gate assignment
    plot_gantt_chart(allocated_turns=turns2, lp_variable_outcomes=x)

#Gu#

#uncomment if needed

# for alloc in x:
#     if x[alloc].varValue:  #( for gurobi Previously had to change varValue to "X" in lines 204 & 109)
#         print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))




## Model D - More Implicit Constraints (occupancy of stands) #######

occupancy = pd.DataFrame({
    'gate':['A3', 'A2'],
    'occupied_from':pd.to_datetime(["02/01/2016 15:15", "02/01/2016 13:15"]),
    'occupied_to':pd.to_datetime(["02/01/2016 19:15", "02/01/2016 14:15"]),
    }, columns=['gate', 'occupied_from', 'occupied_to'])

occupancy

# 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost

# 1. Objective Function (ignore for now)
# prob += 0

#Gu#
opt_model = gp.Model(name = "MIP Model")
objective = 0
opt_model.ModelSense = gp.GRB.MINIMIZE
opt_model.setObjective(objective)

# 2. Variable: x[i,j] = (0,1)
# Binary = turn_i allocated to gate_j
x = {}
for t in turn_list:
    # For compatible gates
    for g in compatible_gates[t]:
        if g in occupancy.gate.values:

            t_dep = turns2.loc[turns2['turn_no'] == t, 'outbound_departure'].values[0]
            t_arr = turns2.loc[turns2['turn_no'] == t, 'inbound_arrival'].values[0]
            oc_from = occupancy.loc[occupancy['gate'] == g, 'occupied_from'].values[0]
            oc_to = occupancy.loc[occupancy['gate'] == g, 'occupied_to'].values[0]

            if (oc_to >= t_arr) and (oc_from <= t_dep):
                print("Gate %s is occupied during time of Turn %d" % (g, t))
                continue

        # Gate not occupied so create variable
        # x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)
        x[t, g] = opt_model.addVar(vtype=gp.GRB.BINARY, name="t%i_g%s".format(t, g))
        print("Created variable for gate %s for turn %d" % (g, t))

# 3. Constraints
# i. Each turn must be assigned to one compatible gate
for t in turn_list:
    # prob += lpSum(x[t, g] for g in gate_list if (t, g) in x) == 1
    opt_model.addConstr(gp.quicksum(x[t,g] for g in gate_list if (t,g) in x) ==1)
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
            #Gu#
            constraint_for_time_bucket = opt_model.addConstr((gp.quicksum(cons) <= 1))

            # These will occur when the plane overlaps change
            # prob += constraint_for_time_bucket
            #Gu#
            #Need to make a list adding all the constraints to if you add the above line

# Solve
# prob.solve()

opt_model.optimize()

# Report
# print("Status: ", LpStatus[prob.status])
# print("Minimised Cost: ", value(prob.objective))

#Gu#
print("Model Status:",opt_model.Status)


for alloc in x:
    if x[alloc].X:
        print("Turn %i assigned to gate %s" % (alloc[0], alloc[-1]))

## Model E - Explicit Constraints #######
#NOTE : This section is mostly same as the one before in syntax correction. Just the equations are a bit modified.

#
# # Imagine we cannot use gate C1 for any turn, instead of removing the variable as before
# # We can add it as an explicit constraint
# # The below follows just like before:
#
# # 0. Initialise model
# prob = LpProblem("Airport Gate Allocation", LpMinimize)  # minimize cost
#
# # 1. Objective Function (ignore for now)
# prob += 0
#
# # 2. Variable: x[i,j] = (0,1)
# # Binary = turn_i allocated to gate_j
# x = {}
# for t in turn_list:
#     # For compatible gates
#     for g in compatible_gates[t]:
#         if g in occupancy.gate.get_values():
#
#             t_dep = turns2.loc[turns2['turn_no'] == t, 'outbound_departure'].values[0]
#             t_arr = turns2.loc[turns2['turn_no'] == t, 'inbound_arrival'].values[0]
#             oc_from = occupancy.loc[occupancy['gate'] == g, 'occupied_from'].values[0]
#             oc_to = occupancy.loc[occupancy['gate'] == g, 'occupied_to'].values[0]
#
#             if (oc_to >= t_arr) and (oc_from <= t_dep):
#                 print("Gate %s is occupied during time of Turn %d" % (g, t))
#                 continue
#
#         # Gate not occupied so create variable
#         x[t, g] = LpVariable("t%i_g%s" % (t, g), 0, 1, LpBinary)
#         print("Created variable for gate %s for turn %d" % (g, t))
#
# # 3. Constraints
# # i. Each turn must be assigned to one compatible gate
# for t in turn_list:
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

# # Visualise outcome
# plot_gantt_chart(turns2, x)
#
#
# # Save for part 2
# pickle.dump(airport, open("airport.p", "wb"))
# pickle.dump(turns2, open("turns2.p", "wb"))
# pickle.dump(occupancy, open("occupancy.p", "wb"))
# pickle.dump(heatmapdf, open("heatmapdf.p", "wb"))