#
# Ziel: Mieten vs Kaufen
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from steuerberechnung import steuerberechnung_immo, steuerberechnung_etf

################################################################################
#
# Eingabeparameter
#
################################################################################

#
# Allgemein
#
anlagehorizont = 30

#
# Steuern
#
alleinstehend = False
einkommen = 150_000
steuerjahr = 2021

#
# Immobilie
#
kaufpreis = 150_000
renovierungskosten = 1_000
kaufnebenkosten = 15_000
instandhaltungskosten = 2000
kostensteigerung = 0.02
unsicherheit_kostensteigerung = 1
wertsteigerung = 0.015
unsicherheit_wertsteigerung = 0.02
eigenkapital = 25_500

zinsbindung = 15
zinsatz = 0.0200
tilgungssatz = 0.03
anschlusszinssatz = 0.04
unsicherheit_anschlusszinssatz = 1

#
# Mieten
#
nettokaltmiete = 300
steigerung_nettokaltmiete = 0.02
unsicherheit_steigerung_nettokaltmiete = 0.02

#
# Alternative Anlagen
#
kapitalertragssteuer = 0.25
etf_rendite = 0.06
unsicherheit_etf_rendite = 1
verzinsung_ek = 0.02
unsicherheit_verzinsung_ek = 1

# 1. Berechnung: Immobilienvermögen p.a. + am Ende des Anlagehorizonts

# 2. Berechnung: ETF Vermögen (initiales EK + Kapital wenn
# Kosten der Immo > Kosten Miete) p.a. + am Ende des Anlagehorizonts

# 3. Berechnung: EK Vermögen p.a. (initiales EK + Kapital wenn
# Kosten der Immo > Kosten Miete) + am Ende des Anlagehorizonts


# Objekt
gesamtkosten = kaufpreis + kaufnebenkosten + renovierungskosten

# Finanzierung
darlehen = gesamtkosten - eigenkapital
kreditrate_jahr = darlehen * (zinsatz + tilgungssatz)

jahr_pj = [0]
wert_immo_pj = [kaufpreis + renovierungskosten]
hilfsfeld_rate_pj = [0]
anschlussrate_jahr = darlehen * (tilgungssatz + anschlusszinssatz)
zinssatz_pj = [0]
zins_pj = [0]
restschuld_pj = [darlehen]
kreditrate_pj = [0]
tilgung_pj = [0]
vermoegen_immo = [wert_immo_pj[0] - darlehen]
etf_vermoegen = [eigenkapital]
etf_vermoegen_versteuert = [eigenkapital]
verzinstes_ek_vermoegen = [eigenkapital]
cashflow = [kreditrate_jahr - nettokaltmiete - instandhaltungskosten]
etf_vermoegen_minus_neg_cashflows = [eigenkapital]
etf_vermoegen_minus_neg_cashflows_versteuert_pj = [eigenkapital]
vermoegen_immo_versteuert_pj = [wert_immo_pj[0] - darlehen]

nettokaltmiete_pa = [nettokaltmiete * 12]
instandhaltungskosten_pa = [instandhaltungskosten]

# Jährliche Betrachtung
for index_nr in range(1, anlagehorizont + 1):

    # index_nr = 1
    jahr_pj.append(index_nr)

    # Finanzierung
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
    zins_pj.append(restschuld_pj[index_nr - 1] * zinssatz_pj[index_nr])

    # Kreditrate
    if hilfsfeld_rate_pj[index_nr] > restschuld_pj[index_nr - 1]:
        kreditrate_pj.append(restschuld_pj[index_nr - 1] * (1 + zinssatz_pj[index_nr]))
    else:
        kreditrate_pj.append(hilfsfeld_rate_pj[index_nr])

    # Tilgung
    tilgung_pj.append(kreditrate_pj[index_nr] - zins_pj[index_nr])

    # Restschuld
    restschuld_pj.append(restschuld_pj[index_nr - 1] - tilgung_pj[index_nr])

    # Wert der Immobilie (p.a.)
    wert_immo_pj.append(wert_immo_pj[index_nr - 1] * (1 + wertsteigerung))

    # Immobilienvermögen (p.a.)
    vermoegen_immo.append(wert_immo_pj[index_nr] - restschuld_pj[index_nr])

    if wert_immo_pj[index_nr] > wert_immo_pj[0] and index_nr < 10:
        einkommenssteuer_einkommen = steuerberechnung_immo(
            jahreseinkommen=einkommen, splittingtarif=False, steuerjahr=steuerjahr,
        )
        einkommenssteuer_einkommen_immo = steuerberechnung_immo(
            jahreseinkommen=(wert_immo_pj[index_nr] - wert_immo_pj[0] + einkommen),
            splittingtarif=False,
            steuerjahr=steuerjahr,
        )

        vermoegen_immo_versteuert_pj.append(
            wert_immo_pj[index_nr]
            - restschuld_pj[index_nr]
            - (einkommenssteuer_einkommen_immo - einkommenssteuer_einkommen)
        )
    else:
        vermoegen_immo_versteuert_pj.append(
            wert_immo_pj[index_nr] - restschuld_pj[index_nr]
        )

    # ETF Vermögen (p.a.)
    if kreditrate_pj[index_nr] >= nettokaltmiete_pa[index_nr - 1]:
        etf_vermoegen.append(
            etf_vermoegen[index_nr - 1] * (etf_rendite + 1)
            + (kreditrate_pj[index_nr] - nettokaltmiete_pa[index_nr - 1])
            + instandhaltungskosten_pa[index_nr - 1]
        )

        cashflow.append(
            instandhaltungskosten_pa[index_nr - 1]
            + kreditrate_pj[index_nr]
            - nettokaltmiete_pa[index_nr - 1]
        )

        etf_vermoegen_minus_neg_cashflows_versteuert_pj.append(
            steuerberechnung_etf(
                investition=sum(np.array(cashflow)[np.array(cashflow) > 0]),
                endwert=etf_vermoegen[index_nr],
            )
            + sum(np.array(cashflow)[np.array(cashflow) < 0])
        )
    else:
        # Wenn die Netto-Kaltmiete höher ist als die Kreditrate sammeln wir die
        # höheren Kosten einfach als Ausgabe, die am Ende das Vermögen schmälert.
        # Es wird also davon ausgegangen, dass die Miete aus dem Cashflow bezahlt wird.
        # -> Dies Art der Berechnung bevorzugt aber die ETF Investition,
        # besser wäre es, soviel ETF Anteile zu verkaufen (unter Beachtung der Steuern)
        # das der negative Cashflow gedeckt ist.
        etf_vermoegen.append(
            etf_vermoegen[index_nr - 1] * (etf_rendite + 1)
            + instandhaltungskosten_pa[index_nr - 1]
        )

        cashflow.append(
            instandhaltungskosten_pa[index_nr - 1]
            + kreditrate_pj[index_nr]
            - nettokaltmiete_pa[index_nr - 1]
        )

        etf_vermoegen_minus_neg_cashflows_versteuert_pj.append(
            steuerberechnung_etf(
                investition=sum(np.array(cashflow)[np.array(cashflow) > 0]),
                endwert=etf_vermoegen[index_nr],
            )
            + sum(np.array(cashflow)[np.array(cashflow) < 0])
        )

    # Verzinstes EK Vermoegen (p.a.)
    if kreditrate_pj[index_nr] >= nettokaltmiete_pa[index_nr - 1]:
        verzinstes_ek_vermoegen.append(
            verzinstes_ek_vermoegen[index_nr - 1] * (verzinsung_ek + 1)
            + (kreditrate_pj[index_nr] - nettokaltmiete_pa[index_nr - 1])
            + instandhaltungskosten_pa[index_nr - 1]
        )
    else:
        verzinstes_ek_vermoegen.append(
            verzinstes_ek_vermoegen[index_nr - 1] * (verzinsung_ek + 1)
            - (nettokaltmiete_pa[index_nr - 1] - kreditrate_pj[index_nr])
            + instandhaltungskosten_pa[index_nr - 1]
        )

    # Steigerung Instandhaltungskosten
    instandhaltungskosten_pa.append(
        instandhaltungskosten_pa[index_nr - 1] * (1 + kostensteigerung)
    )
    nettokaltmiete_pa.append(
        nettokaltmiete_pa[index_nr - 1] * (1 + steigerung_nettokaltmiete)
    )

plt.plot(jahr_pj, etf_vermoegen, label="ETF Vermoegen")
plt.plot(jahr_pj, vermoegen_immo, label="Immo Vermoegen")
plt.plot(jahr_pj, vermoegen_immo_versteuert_pj, label="Immo Vermoegen versteuert")
# plt.plot(jahr_pj, verzinstes_ek_vermoegen, label="Verzinstes EK Vermoegen")
plt.plot(
    jahr_pj, etf_vermoegen_minus_neg_cashflows_versteuert_pj, label="ETF versteuert"
)
plt.title("Mieten vs. Kaufen")
plt.legend()
plt.show()
