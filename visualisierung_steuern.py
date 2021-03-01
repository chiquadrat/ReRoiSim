#
# Ziel: Berechnung der Lohnsteuer
#

import numpy as np
import matplotlib.pyplot as plt
import steuerberechnung


einkommen = np.linspace(0,200_000,41)
steuer = []
for i in range(len(einkommen)):
    steuer.append(steuerberechnung.steuerberechnung(einkommen[i], True, 2015))
plt.plot(einkommen,steuer)
#steuersatz=steuer/einkommen
#plt.plot(einkommen,steuersatz)