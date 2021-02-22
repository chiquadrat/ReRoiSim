#
# Ziel: Berechnung der Lohnsteuer
#

import numpy as np
import matplotlib.pyplot as plt


################################################################################
#
# Steuerberechnung
#
################################################################################

# die Steuerberechnung erfolgt nach Einkommensteuergesetz (EStG)
# § 32a Einkommensteuertarif
# https://www.gesetze-im-internet.de/estg/__32a.html


def steuerberechnung (jahreseinkommen, splittingtarif, grenzsteuersaetze, parameter_steuersatz):
    
    if splittingtarif:
        jahreseinkommen = jahreseinkommen / 2

    x = np.floor(jahreseinkommen)
    y = (x-grenzsteuersaetze[0]) / 10000
    z = (x-grenzsteuersaetze[1]) / 10000

    if jahreseinkommen <= grenzsteuersaetze[0]:
        einkommenssteuer = parameter_steuersatz[0]
    elif jahreseinkommen <= grenzsteuersaetze[1]:
        einkommenssteuer = (parameter_steuersatz[1][0] * y + parameter_steuersatz[1][1]) * y
    elif jahreseinkommen <= grenzsteuersaetze[2]:
        einkommenssteuer = (parameter_steuersatz[2][0] * z + parameter_steuersatz[2][1]) * z + parameter_steuersatz[2][2]
    elif jahreseinkommen <= grenzsteuersaetze[3]:
        einkommenssteuer = parameter_steuersatz[3][0] * x - parameter_steuersatz[3][1]
    else:
        einkommenssteuer = parameter_steuersatz[4][0] * x - parameter_steuersatz[4][1]

    einkommenssteuer = np.floor(einkommenssteuer)

    if splittingtarif:
        einkommenssteuer = einkommenssteuer * 2

    return (einkommenssteuer)

