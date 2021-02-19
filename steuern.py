#
# Ziel: Berechnung der Lohnsteuer
#

import numpy as np
import matplotlib.pyplot as plt

#Todo: Splitting integrieren und mit Stiftung Warentest vergleichen

################################################################################
#
# Steuerberechnung
#
################################################################################

# die Steuerberechnung erfolgt nach Einkommensteuergesetz (EStG)
# § 32a Einkommensteuertarif
# https://www.gesetze-im-internet.de/estg/__32a.html
grenzsteuersaetze_2015 = [8472,13469,52881,250730]
parameter_steuersatz_2015 = [0,[997.6,1400],[228.74,2397,948.68],[0.42,8261.29],[0.45,15783.19]]
grenzsteuersaetze_2021 = [9744,14753,57918,274612]
parameter_steuersatz_2021 = [0,[995.21,1400],[208.85,2397,950.96],[0.42,9136.63],[0.45,17374.99]]



def steuerberechnung (jahreseinkommen, grenzsteuersaetze, parameter_steuersatz):
    x = np.floor(jahreseinkommen)
    y = (x-grenzsteuersaetze[0])/10000
    z = (x-grenzsteuersaetze[1])/10000
    if jahreseinkommen <= grenzsteuersaetze[0]:
        einkommenssteuer = parameter_steuersatz_2021[0]
    elif jahreseinkommen <= grenzsteuersaetze[1]:
        einkommenssteuer = (parameter_steuersatz[1][0] * y + parameter_steuersatz[1][1]) * y
    elif jahreseinkommen <= grenzsteuersaetze[2]:
        einkommenssteuer = (parameter_steuersatz[2][0] * z + parameter_steuersatz[2][1]) * z + parameter_steuersatz[2][2]
    elif jahreseinkommen <= grenzsteuersaetze[3]:
        einkommenssteuer = parameter_steuersatz[3][0] * x - parameter_steuersatz[3][1]
    else:
        einkommenssteuer = parameter_steuersatz[4][0] * x - parameter_steuersatz[4][1]
    return (einkommenssteuer)

einkommen = np.linspace(0,495_000,100)
steuer = []
for i in range(len(einkommen)):
    steuer.append(steuerberechnung(einkommen[i], grenzsteuersaetze_2021,parameter_steuersatz_2021))
#plt.plot(einkommen,steuer)
steuersatz=steuer/einkommen
plt.plot(einkommen,steuersatz)