
datafileName = 'Instances_ULS/Toy_Instance.txt'

with open(datafileName, "r") as file:
    line = file.readline()  
    lineTab = line.split()    
    nbPeriodes = int(lineTab[0])
    
    line = file.readline()  
    lineTab = line.split()
    demandes = []
    for i in range(nbPeriodes):
        demandes.append(int(lineTab[i]))
        
    line = file.readline()  
    lineTab = line.split()
    couts = []
    for i in range(nbPeriodes):
        couts.append(int(lineTab[i]))

    line = file.readline()  
    lineTab = line.split()
    cfixes = []
    for i in range(nbPeriodes):
        cfixes.append(int(lineTab[i]))
    
    line = file.readline()  
    lineTab = line.split()    
    cstock = int(lineTab[0])

#print(nbPeriodes)
#print(demandes)
#print(couts)
#print(cfixes)
#print(cstock)

from mip import *
import time


model2 = Model(name = "ULS", solver_name="CBC")

y = [model2.add_var(name="y(" + str(i) + ")", lb=0, ub=1, var_type=BINARY) for i in range(nbPeriodes)]

x = [[model2.add_var(name="x(" + str(i) + str(j) +")", lb=0, ub=1, var_type=BINARY) for j in range(nbPeriodes)] for i in range(nbPeriodes)]

model2.objective = minimize(xsum((xsum((couts[i] + cstock*(j-i))*x[i][j]*demandes[j] for j in range(nbPeriodes)) + cfixes[i]*y[i]) for i in range(nbPeriodes)))

for i in range(nbPeriodes):
    model2.add_constr(xsum(x[i][j] for j in range(nbPeriodes)) <= nbPeriodes - xsum(xsum(x[k][j] for j in range(nbPeriodes)) for k in range(i)))

for j in range(nbPeriodes):
    model2.add_constr(xsum(x[i][j] for i in range(nbPeriodes)) == 1)
    for i in range(nbPeriodes):
        model2.add_constr(x[i][j] <= y[i])
        if (i>j):
            model2.add_constr(x[i][j] == 0)       
        




model2.write("test.lp")

status = model2.optimize()

print("\n----------------------------------")
if status == OptimizationStatus.OPTIMAL:
    print("Status de la résolution: OPTIMAL")
elif status == OptimizationStatus.FEASIBLE:
    print("Status de la résolution: TEMPS LIMITE et SOLUTION REALISABLE CALCULEE")
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print("Status de la résolution: TEMPS LIMITE et AUCUNE SOLUTION CALCULEE")
elif status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE:
    print("Status de la résolution: IRREALISABLE")
elif status == OptimizationStatus.UNBOUNDED:
    print("Status de la résolution: NON BORNE")
    
if model2.num_solutions>0:
    print("Solution calculée")
    print("-> Valeur de la fonction objectif de la solution calculée : ",  model2.objective_value)

    print("Prod\n")
    for i in range(nbPeriodes):
        print([x[i][j].x for j in range(nbPeriodes)])

    print("Besoin,Bool, Coût\n")
    for i in range(nbPeriodes):
        print(demandes[i], y[i].x, couts[i], "\n")

