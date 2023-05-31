import os
from mip import *
import time
import math as m
from mip.cbc import cbclib, ffi
ffi.cdef("int Cbc_getNodeCount(Cbc_Model *model);")


dir = "Instances_ULS"

files = []
relax_lin = []
status_array = []  # ok
best_value = []  # ok
ecart = []
noeuds = []
temps_res = []  # ok

for file in os.listdir(dir):
    files.append(file)
    with open(dir+"/"+file, "r") as file:
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

    model = Model(name="ULS", solver_name="CBC")
    # variable binaire valant 1 si on produit pendant la période i, et 0 sinon
    y = [model.add_var(name="y(" + str(i) + ")", lb=0, ub=1,
                       var_type=BINARY) for i in range(nbPeriodes+1)]

    # quantité produite dans le mois
    x = [model.add_var(name="x(" + str(i) + ")", lb=0, var_type=INTEGER)
         for i in range(nbPeriodes+1)]

    # quantité stockée a la fin du mois
    s = [model.add_var(name="s(" + str(i) + ")", lb=0, var_type=INTEGER)
         for i in range(nbPeriodes+1)]

    model.objective = minimize(xsum(
        x[i+1]*couts[i] + cfixes[i]*y[i+1] + cstock*s[i+1] for i in range(nbPeriodes)))

    for i in range(nbPeriodes):
        model.add_constr(s[0] == 0)
        model.add_constr(x[i+1] <= y[i+1]*sum(demandes[j]
                         for j in range(i, nbPeriodes)))
        model.add_constr(x[i+1] + s[i] >= demandes[i])
        model.add_constr(s[i+1] == x[i+1] + s[i] - demandes[i])

    model.write("test.lp")
    model.verbose = 0

    a = time.time()
    status = model.optimize(max_seconds=10)
    b = time.time() - a
    noeuds.append(cbclib.Cbc_getNodeCount(model.solver._model))
    status_array.append(status)
    temps_res.append(b)
    if model.num_solutions > 0:
        best_value.append(model.objective_value)
    else:
        best_value.append(None)

    model2 = Model(name="ULS", solver_name="CBC")
    # variable binaire valant 1 si on produit pendant la période i, et 0 sinon
    y = [model2.add_var(name="y(" + str(i) + ")", lb=0, ub=1,
                        var_type=BINARY) for i in range(nbPeriodes+1)]

    # quantité produite dans le mois
    x = [model2.add_var(name="x(" + str(i) + ")", lb=0, var_type=CONTINUOUS)
         for i in range(nbPeriodes+1)]

    # quantité stockée a la fin du mois
    s = [model2.add_var(name="s(" + str(i) + ")", lb=0, var_type=CONTINUOUS)
         for i in range(nbPeriodes+1)]

    model2.objective = minimize(xsum(
        x[i+1]*couts[i] + cfixes[i]*y[i+1] + cstock*s[i+1] for i in range(nbPeriodes)))

    for i in range(nbPeriodes):
        model2.add_constr(s[0] == 0)
        model2.add_constr(x[i+1] <= y[i+1]*sum(demandes[j]
                                               for j in range(i, nbPeriodes)))
        model2.add_constr(x[i+1] + s[i] >= demandes[i])
        model2.add_constr(s[i+1] == x[i+1] + s[i] - demandes[i])

    model2.write("test.lp")
    model2.verbose = 0

    model2.optimize(max_seconds=10)
    relax_lin.append(model2.objective_value)

for i in range(len(relax_lin)):
    ecart.append(m.fabs((relax_lin[i]-best_value[i])*100/best_value[i]))
print(files)
print("\n")
print(relax_lin)
print("\n")
print(status_array)
print("\n")
print(best_value)
print("\n")
print(ecart)
print("\n")
print(noeuds)
print("\n")
print(temps_res)
