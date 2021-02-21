#
# Ziel: Berechnung der Rendite einer Immobilie
#

import numpy as np
import pandas as pd


################################################################################
#
# Eingabeparameter
#
################################################################################

# Objekt
baujahr = 1925
kaufpreis = 100_000
kaufpreis_grundstueck = 30_000
kaufpreis_sanierung = 7_000
kaufnebenkosten = 5_000
renovierungskosten = 1_000

mieteinnahmen = 5_000           # pro Jahr
instandhaltungskosten = 800     # pro Jahr
verwaltungskosten = 500         # pro Jahr
mietausfall = 0.02              # Vieflaches der Nettokaltmiete

mietsteigerung = 0.02
erste_mieterhoehung = 5         # Jahr ab dem die Mieterhöhung erfolgt >1
kostensteigerung = 0.015

# Finanzierung
eigenkapital = 6_500
zinsbindung = 15
disagio = 0.01
zinsatz = 0.0128
tilgungssatz = 0.03
anschlusszinssatz = 0.05

# Steuern
alleinstehend = 1  # 0/1 -> nein/ja
einkommen = 50_000 # zu versteuerndes Jahreseinkommen

# Renditeberechnung
anlagehorizont = 30
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

################################################################################
#
# Berechnung
#
################################################################################


jahr_pj = []
mieteinnahmen_pj = []  # pj -> pro jahr
nicht_umlegbare_kosten_pj = []
mietausfall_pj = []
jahresreinertrag_pj = []
hilfsfeld_rate_pj = []
kreditrate_pj = []
zinssatz_pj = []
zins_pj = []
tilgung_pj = []
restschult_pj = []
bemessung_afa_gebaeude_pj = []
afasatz_gebaeude_pj = []
afa_gebaeude_pj = []
bemessung_afa_sanierung_pj = []
afasatz_sanierung_pj = []
afa_sanierung_pj = []
werbungskosten_pj=[]
steuerliches_ergebnis_pj = []



for index_nr in range (0,anlagehorizont):

    # Jahr
    jahr_pj.append(index_nr + 1)

    # Mieteinahmen
    if jahr_pj[index_nr] < erste_mieterhoehung:
        mieteinnahmen_pj.append(mieteinnahmen)
    elif jahr_pj[index_nr] == erste_mieterhoehung:
        mieteinnahmen_pj.append(mieteinnahmen * (1 + mietsteigerung))
    else:
        mieteinnahmen_pj.append(mieteinnahmen_pj[-1] * (1 + mietsteigerung))

    # nicht umlegbare Kosten
    if jahr_pj[index_nr] == 1:
        nicht_umlegbare_kosten_pj.append(instandhaltungskosten + verwaltungskosten)
    else:
        nicht_umlegbare_kosten_pj.append(nicht_umlegbare_kosten_pj[-1] * (1 + kostensteigerung))

    # Pauschale für Mietausfall
    mietausfall_pj.append(mieteinnahmen_pj[index_nr]*mietausfall)

    # Jahresreinertrag
    jahresreinertrag_pj.append(mieteinnahmen_pj[index_nr]-nicht_umlegbare_kosten_pj[index_nr]-mietausfall_pj[index_nr])


    # Hilfsfeld Rate
    if jahr_pj[index_nr] <= zinsbindung:
        hilfsfeld_rate_pj.append(kreditrate_jahr)
    else:
        hilfsfeld_rate_pj.append(anschlussrate_jahr)

    # Zinssatz
    if jahr_pj[index_nr] <= zinsbindung:
        zinssatz_pj.append(zinsatz)
    else:
        zinssatz_pj.append(anschlusszinssatz)

    # Zins
    if jahr_pj[index_nr] == 1:
        zins_pj.append(darlehen*zinssatz_pj[index_nr])
    else:
        zins_pj.append(restschult_pj[index_nr-1]*zinssatz_pj[index_nr])

    # Kreditrate
    if jahr_pj[index_nr] == 1:
        if hilfsfeld_rate_pj[index_nr] > darlehen:
            kreditrate_pj.append(darlehen*(1+zinssatz_pj[index_nr]))
        else:
            kreditrate_pj.append(hilfsfeld_rate_pj[index_nr])
    else:
        if hilfsfeld_rate_pj[index_nr] > restschult_pj[index_nr-1]:
            kreditrate_pj.append(restschult_pj[index_nr-1]*(1+zinssatz_pj[index_nr]))
        else:
            kreditrate_pj.append(hilfsfeld_rate_pj[index_nr])

    # Tilgung
    tilgung_pj.append(kreditrate_pj[index_nr]-zins_pj[index_nr])

    # Restschuld
    if jahr_pj[index_nr] == 1:
        restschult_pj.append(darlehen-tilgung_pj[index_nr])
    else:
        restschult_pj.append(restschult_pj[index_nr-1]-tilgung_pj[index_nr])

    # Bemessung für Afa
    bemessung_afa_gebaeude_pj.append(bemessung_abschreibung)

    # Afasatz Gebäude
    if baujahr > 1924:
        afasatz_gebaeude_pj.append(0.02)
    else:
        afasatz_gebaeude_pj.append(0.025)

    # Afa Gebäude
    afa_gebaeude_pj.append(bemessung_afa_gebaeude_pj[index_nr]*afasatz_gebaeude_pj[index_nr])
    
    # Bemessung Afa Sanierung
    if jahr_pj[index_nr] < 13:
        bemessung_afa_sanierung_pj.append(bemessung_sonderabschreibung)
    else:
        bemessung_afa_sanierung_pj.append(0)
    
    # Afa-Satz Sanierung
    if jahr_pj[index_nr] < 9:
        afasatz_sanierung_pj.append(0.09)
    elif jahr_pj[index_nr] < 13:
        afasatz_sanierung_pj.append(0.07)
    else:
        afasatz_sanierung_pj.append(0)

    # Afa Sanierung
    afa_sanierung_pj.append(bemessung_afa_sanierung_pj[index_nr]*afasatz_sanierung_pj[index_nr])

    # Werbungskosten (Sofortabzug)
    if jahr_pj[index_nr] == 1:
        if jahr_pj[index_nr] <= zinsbindung:
            if disagio > 0.05:
                werbungskosten_pj.append(renovierungskosten + disagio*darlehen/zinsbindung)
            else:
                werbungskosten_pj.append(renovierungskosten + disagio*darlehen)
        else:
            werbungskosten_pj.append(renovierungskosten + 0)
    else:
        if jahr_pj[index_nr] <= zinsbindung:
            if disagio > 0.05:
                werbungskosten_pj.append(disagio*darlehen/zinsbindung)
            else:
                werbungskosten_pj.append(0)
        else:
            werbungskosten_pj.append(0)

    # Steuerliches Ergebnis
    steuerliches_ergebnis_pj.append(jahresreinertrag_pj[index_nr] - zins_pj[index_nr] - afa_gebaeude_pj[index_nr] - afa_sanierung_pj[index_nr] - werbungskosten_pj[index_nr])

   








