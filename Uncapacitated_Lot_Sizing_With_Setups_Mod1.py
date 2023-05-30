

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

print("nbPeriodes: ",nbPeriodes)
print("demandes: ",demandes)
print("couts: ",couts)
print("cfixes: ",cfixes)
print("cstock: ",cstock)


from mip import *
import time

model = Model(name = "ULS", solver_name="CBC")
# variable binaire valant 1 si on produit pendant la période i, et 0 sinon
y = [model.add_var(name="y(" + str(i) + ")", lb=0, ub=1, var_type=BINARY) for i in range(nbPeriodes+1)]

# quantité produite dans le mois
x = [model.add_var(name="x(" + str(i) + ")", lb=0, var_type=INTEGER) for i in range(nbPeriodes+1)]

# quantité stockée a la fin du mois
s = [model.add_var(name="s(" + str(i) + ")", lb=0, var_type=INTEGER) for i in range(nbPeriodes+1)]

model.objective = minimize(xsum(x[i+1]*couts[i] + cfixes[i]*y[i+1] + cstock*s[i+1] for i in range(nbPeriodes)))

for i in range(nbPeriodes):
    model.add_constr(s[0] == 0)
    model.add_constr(x[i+1] <= y[i+1]*sum(demandes[j] for j in range(i,nbPeriodes)))
    model.add_constr(x[i+1] + s[i] >= demandes[i])
    model.add_constr(s[i+1] == x[i+1] + s[i] - demandes[i])

model.write("test.lp")

status = model.optimize()

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
    
if model.num_solutions>0:
    print("Solution calculée")
    print("-> Valeur de la fonction objectif de la solution calculée : ",  model.objective_value)

    print("Prod, Besoin, Stock, Bool, Coût\n")
    for i in range(nbPeriodes):
        print(x[i+1].x, demandes[i], s[i+1].x, y[i+1].x, couts[i], "\n")
