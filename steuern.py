#
# Ziel: Berechnung der Lohnsteuer
#

import numpy as np
import matplotlib.pyplot as plt
import steuerberechnung

# Parameter Steuerberechnung 2015
#grenzsteuersaetze = [8472,13469,52881,250730]
#parameter_steuersatz = [0,[997.6,1400],[228.74,2397,948.68],[0.42,8261.29],[0.45,15783.19]]

# Parameter Steuerberechnung 2021
grenzsteuersaetze = [9744,14753,57918,274612]
parameter_steuersatz = [0,[995.21,1400],[208.85,2397,950.96],[0.42,9136.63],[0.45,17374.99]]


einkommen = np.linspace(0,200_000,41)
steuer = []
for i in range(len(einkommen)):
    steuer.append(steuerberechnung.steuerberechnung(einkommen[i], True, grenzsteuersaetze,parameter_steuersatz))
#plt.plot(einkommen,steuer)
steuersatz=steuer/einkommen
plt.plot(einkommen,steuersatz)