#
# Ziel: Berechnung der Lohnsteuer
#

import numpy as np


################################################################################
#
# Steuerberechnung
#
################################################################################

# die Steuerberechnung erfolgt nach Einkommensteuergesetz (EStG)
# § 32a Einkommensteuertarif
# https://www.gesetze-im-internet.de/estg/__32a.html


def steuerberechnung_immo(jahreseinkommen, splittingtarif, steuerjahr):
    """Funktion berechnet die Einkommenssteuer

    Args:
        jahreseinkommen ([float]): [description]
        splittingtarif ([boolean]): [description]
        steuerjahr ([integer]): [description]

    Returns:
        einkommenssteuer: [description]
    """

    # Parameter für die Steuerberechnung
    if steuerjahr == 2015:
        grenzsteuersaetze = [8472, 13469, 52881, 250730]
        parameter_steuersatz = [
            0,
            [997.6, 1400],
            [228.74, 2397, 948.68],
            [0.42, 8261.29],
            [0.45, 15783.19],
        ]
    elif steuerjahr == 2021:
        grenzsteuersaetze = [9744, 14753, 57918, 274612]
        parameter_steuersatz = [
            0,
            [995.21, 1400],
            [208.85, 2397, 950.96],
            [0.42, 9136.63],
            [0.45, 17374.99],
        ]
    elif steuerjahr == 2023:
        grenzsteuersaetze = [10908, 15999, 62809, 277825]
        parameter_steuersatz = [
            0,
            [979.18, 1400],
            [192.59, 2397, 966.53],
            [0.42, 9972.98],
            [0.45, 18307.73],
        ]

    if splittingtarif:
        jahreseinkommen = jahreseinkommen / 2

    x = np.floor(jahreseinkommen)
    y = (x - grenzsteuersaetze[0]) / 10000
    z = (x - grenzsteuersaetze[1]) / 10000

    if jahreseinkommen <= grenzsteuersaetze[0]:
        einkommenssteuer = parameter_steuersatz[0]
    elif jahreseinkommen <= grenzsteuersaetze[1]:
        einkommenssteuer = (
            parameter_steuersatz[1][0] * y + parameter_steuersatz[1][1]
        ) * y
    elif jahreseinkommen <= grenzsteuersaetze[2]:
        einkommenssteuer = (
            parameter_steuersatz[2][0] * z + parameter_steuersatz[2][1]
        ) * z + parameter_steuersatz[2][2]
    elif jahreseinkommen <= grenzsteuersaetze[3]:
        einkommenssteuer = parameter_steuersatz[3][0] * x - parameter_steuersatz[3][1]
    else:
        einkommenssteuer = parameter_steuersatz[4][0] * x - parameter_steuersatz[4][1]

    einkommenssteuer = np.floor(einkommenssteuer)

    if splittingtarif:
        einkommenssteuer = einkommenssteuer * 2

    return einkommenssteuer

def steuerberechnung_etf(investition, endwert, kapitalertragssteuer=0.26375):
    endwert_versteuert = endwert - (endwert - investition) * kapitalertragssteuer
    return endwert_versteuert
    