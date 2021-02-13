#
# Ziel: Nachbauen des Stiftung Warentest Tools
#

import numpy as np
import pandas as pd

################################################################################
#
# Eingabeparameter (Stiftung Warentest Tool)
#
################################################################################

# Objekt
baujahr = 1925
kaufpreis = 100_000
kaufpreis_grundstueck = 30_000
kaufpreis_sanierung = 7_000
kaufnebenkosten = 5_000
renovierungskosten = 1_000

mieteinnahmen = 3_000
instandhaltungskosten = 800
verwaltungskosten = 500
mietausfall = 0.02

mietsteigerung = 0.02
erste_mieterhoehung = 5
kostensteigerung = 0.015

# Finanzierung
eigenkapital = 6_500
zinsbindung = 15
disagio = 0
zinsatz = 0.0128
tilgungssatz = 0.03
anschlusszinssatz = 0.05

# Steuern
alleinstehend = 1  # 0/1 -> nein/ja
einkommen = 50_000

# Renditeberechnung
anlagehorizont = 15
verkaufsfaktor = 25

#
# Berechnungen Eingabemaske
#

# Objekt
gesamtkosten = kaufpreis + kaufnebenkosten + renovierungskosten
jahresreinertrag = (
    mieteinnahmen
    - instandhaltungskosten
    - verwaltungskosten
    - mieteinnahmen * mietausfall
)
kaufpreis_miet_verhaeltnis = (kaufpreis + renovierungskosten) / mieteinnahmen
anfangs_brutto_mietrendite = 1 / kaufpreis_miet_verhaeltnis
anfangs_netto_mietrendite = jahresreinertrag / gesamtkosten

# Finanzierung
darlehen = (gesamtkosten - eigenkapital) / (1 - disagio)
kreditrate_jahr = darlehen * (zinsatz + tilgungssatz)
anschlussrate_jahr = darlehen * (tilgungssatz + anschlusszinssatz)

# Steuern
bemessung_abschreibung = (
    kaufpreis
    + kaufnebenkosten
    - (kaufpreis_grundstueck + kaufpreis_sanierung) * (1 + kaufnebenkosten / kaufpreis)
)
abschreibungsart = "Linear 2,0%" if baujahr > 1924 else "Linear 2,5%"
bemessung_sonderabschreibung = kaufpreis_sanierung * gesamtkosten / kaufpreis

# Renditeberechnung <- ToDo
# verkaufspreis =
# objektrendite_nach_steuern =
# eigenkapitalrendite_nach_steuern =
