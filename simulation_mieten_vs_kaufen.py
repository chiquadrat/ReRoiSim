#
# Ziel: Mieten vs Kaufen
#

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from steuerberechnung import steuerberechnung_immo, steuerberechnung_etf

################################################################################
#
# Eingabeparameter
#
################################################################################


def mieten_kaufen(
    
    sim_runs = 200,

    #
    # Allgemein
    #
    anlagehorizont = 15,
    eigenkapital = 20_000,

    #
    # Kennzahlen Immobilie
    #
    kaufpreis = 150_000,
    renovierungskosten = 1_000,
    kaufnebenkosten = 15_000,
    instandhaltungskosten = 2000,
    kostensteigerung = 0.02,
    unsicherheit_kostensteigerung = 1,
    wertsteigerung = 0.015,
    unsicherheit_wertsteigerung = 0.02,

    #
    # Finanzierung Immobilie
    #
    zinsbindung = 15,
    zinsatz = 0.0200,
    tilgungssatz = 0.03,
    anschlusszinssatz = 0.04,
    unsicherheit_anschlusszinssatz = 1,

    #
    # Mieten
    #
    nettokaltmiete = 3600,
    steigerung_nettokaltmiete = 0.02,
    unsicherheit_steigerung_nettokaltmiete = 0.02,

    #
    # Steuern
    #
    alleinstehend = False,
    kapitalertragssteuer = 0.26375,


    #
    # Alternative Anlagen
    #
    etf_rendite = 0.06,
    unsicherheit_etf_rendite = 1,
    fest_verzinst = 0.02,
    unsicherheit_fest_verzinst = 1,
    
    ):
    

    # Objekt
    gesamtkosten = kaufpreis + kaufnebenkosten + renovierungskosten

    # Finanzierung
    darlehen = gesamtkosten - eigenkapital
    kreditrate_jahr = darlehen * (zinsatz + tilgungssatz)
    
    # Simulation
    vermoegen_immo_pj_runs = []
    etf_vermoegen_pj_runs = []
    etf_vermoegen_versteuert_pj_runs = []
    etf_vermoegen_immo_pj_runs = []
    etf_vermoegen_immo_versteuert_pj_runs = []
    festgeld_vermoegen_pj_runs = []
    festgeld_vermoegen_immo_pj_runs = []
    festgeld_vermoegen_versteuert_pj_runs = []
    festgeld_vermoegen_immo_versteuert_pj_runs = []
    festgeld_vermoegen_initial_pj_runs = []
    festgeld_vermoegen_initial_versteuert_pj_runs = []
    etf_vermoegen_initial_pj_runs = []
    etf_vermoegen_initial_versteuert_pj_runs = []

    kostensteigerung = np.random.normal(
        kostensteigerung, unsicherheit_kostensteigerung, sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs) 
    
    wertsteigerung = np.random.normal(
        wertsteigerung, unsicherheit_wertsteigerung,  sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)
    
    anschlusszinssatz = np.random.normal(
        anschlusszinssatz, unsicherheit_anschlusszinssatz,  sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)    
    
    steigerung_nettokaltmiete = np.random.normal(
        steigerung_nettokaltmiete, unsicherheit_steigerung_nettokaltmiete,  sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)        
    
    etf_rendite = np.random.normal(
        etf_rendite, unsicherheit_etf_rendite,  sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)    
    
    fest_verzinst = np.random.normal(
        fest_verzinst, unsicherheit_fest_verzinst,  sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)    
    
    # Simulation
    for run in range(sim_runs):
        jahr_pj = [0]
        wert_immo_pj = [kaufpreis + renovierungskosten]
        hilfsfeld_rate_pj = [0]
        anschlussrate_jahr = darlehen * (tilgungssatz + anschlusszinssatz[0, run])
        zinssatz_pj = [0]
        zins_pj = [0]
        restschuld_pj = [darlehen]
        kreditrate_pj = [0]
        tilgung_pj = [0]
        vermoegen_immo_pj = [
            wert_immo_pj[0] - darlehen
        ]  # MJ: vermoegen_immo --> vermoegen_immo_pj
        etf_vermoegen_pj = [eigenkapital]  # MJ: etf_vermoegen --> etf_vermoegen_pj
        etf_vermoegen_versteuert_pj = [eigenkapital]
        verzinstes_ek_vermoegen_pj = [eigenkapital]
        cashflow_pj = [kreditrate_jahr + instandhaltungskosten - nettokaltmiete]
        # etf_vermoegen_minus_neg_cashflows_pj = [eigenkapital]
        # etf_vermoegen_minus_neg_cashflows_versteuert_pj = [eigenkapital]

        nettokaltmiete_pj = [
            0,
            nettokaltmiete,
        ]  # MJ: nettokaltmiete_pa --> nettokaltmiete_pa_pj, sollte der erste Eintrag nicht auch nettokaltmiete_pa_pj= [0] sein und dann nettokaltmiete_pa_pj.append(nettokaltmiete * 12), dann ist der Index konstistent
        instandhaltungskosten_pj = [0, instandhaltungskosten]

        etf_vermoegen_immo_pj = [0]
        etf_vermoegen_immo_versteuert_pj = [0]

        festgeld_vermoegen_pj = [eigenkapital]
        festgeld_vermoegen_versteuert_pj = [eigenkapital]

        festgeld_vermoegen_immo_pj = [0]
        festgeld_vermoegen_immo_versteuert_pj = [0]

        festgeld_vermoegen_initial_pj = [eigenkapital]
        festgeld_vermoegen_initial_versteuert_pj = [eigenkapital]
        etf_vermoegen_initial_pj = [eigenkapital]
        etf_vermoegen_initial_versteuert_pj = [eigenkapital]


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
                zinssatz_pj.append(anschlusszinssatz[index_nr - 1, run])

            # Zins
            zins_pj.append(restschuld_pj[index_nr - 1] * zinssatz_pj[index_nr])

            # Kreditrate
            #print(hilfsfeld_rate_pj[index_nr])
            #print(restschuld_pj[index_nr - 1])
            if hilfsfeld_rate_pj[index_nr] > restschuld_pj[index_nr - 1]:
                kreditrate_pj.append(restschuld_pj[index_nr - 1] * (1 + zinssatz_pj[index_nr]))
            else:
                kreditrate_pj.append(hilfsfeld_rate_pj[index_nr])

            # Tilgung
            tilgung_pj.append(kreditrate_pj[index_nr] - zins_pj[index_nr])

            # Restschuld
            restschuld_pj.append(restschuld_pj[index_nr - 1] - tilgung_pj[index_nr])

            # Wert der Immobilie (p.a.)
            wert_immo_pj.append(wert_immo_pj[index_nr - 1] * (1 + wertsteigerung[index_nr - 1, run]))

            # Immobilienvermögen (p.a.)
            vermoegen_immo_pj.append(wert_immo_pj[index_nr] - restschuld_pj[index_nr])

            festgeld_vermoegen_initial_pj.append(
                festgeld_vermoegen_initial_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
            )

            festgeld_vermoegen_initial_versteuert_pj.append(
                festgeld_vermoegen_initial_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                - (festgeld_vermoegen_initial_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run]))
                * kapitalertragssteuer
            )

            etf_vermoegen_initial_pj.append(
                etf_vermoegen_initial_pj[index_nr - 1] * (etf_rendite[index_nr - 1, run] + 1)
            )

            etf_vermoegen_initial_versteuert_pj.append(
                steuerberechnung_etf(
                    investition=eigenkapital,
                    endwert=etf_vermoegen_initial_pj[index_nr],
                    kapitalertragssteuer=kapitalertragssteuer,
                )
            )

            # ETF Vermögen (p.a.)
            if cashflow_pj[index_nr - 1] > 0:
                etf_vermoegen_pj.append(
                    etf_vermoegen_pj[index_nr - 1] * (etf_rendite[index_nr - 1, run] + 1)
                    + cashflow_pj[index_nr - 1]
                )

                festgeld_vermoegen_pj.append(
                    festgeld_vermoegen_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                    + cashflow_pj[index_nr - 1]
                )

                festgeld_vermoegen_versteuert_pj.append(
                    festgeld_vermoegen_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                    - (festgeld_vermoegen_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run]))
                    * kapitalertragssteuer
                    + cashflow_pj[index_nr - 1]
                )

                etf_vermoegen_immo_pj.append(
                    etf_vermoegen_immo_pj[index_nr - 1] * (etf_rendite[index_nr - 1, run] + 1)
                )

                festgeld_vermoegen_immo_pj.append(
                    festgeld_vermoegen_immo_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                )

                festgeld_vermoegen_immo_versteuert_pj.append(
                    festgeld_vermoegen_immo_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                    - (festgeld_vermoegen_immo_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run]))
                    * kapitalertragssteuer
                )

            else:
                etf_vermoegen_pj.append(etf_vermoegen_pj[index_nr - 1] * (etf_rendite[index_nr - 1, run] + 1))

                festgeld_vermoegen_pj.append(
                    festgeld_vermoegen_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                )

                festgeld_vermoegen_versteuert_pj.append(
                    festgeld_vermoegen_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                    - (festgeld_vermoegen_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run]))
                    * kapitalertragssteuer
                )

                etf_vermoegen_immo_pj.append(
                    etf_vermoegen_immo_pj[index_nr - 1] * (etf_rendite[index_nr - 1, run] + 1)
                    + (cashflow_pj[index_nr - 1] * -1)
                )

                festgeld_vermoegen_immo_pj.append(
                    festgeld_vermoegen_immo_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                    + (cashflow_pj[index_nr - 1] * -1)
                )

                festgeld_vermoegen_immo_versteuert_pj.append(
                    festgeld_vermoegen_immo_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run] + 1)
                    - (festgeld_vermoegen_immo_versteuert_pj[index_nr - 1] * (fest_verzinst[index_nr - 1, run]))
                    * kapitalertragssteuer
                    + (cashflow_pj[index_nr - 1] * -1)
                )

            etf_vermoegen_versteuert_pj.append(
                steuerberechnung_etf(
                    investition=sum(np.array(cashflow_pj)[np.array(cashflow_pj) > 0])
                    + eigenkapital,
                    endwert=etf_vermoegen_pj[index_nr],
                    kapitalertragssteuer=kapitalertragssteuer,
                )
            )

            etf_vermoegen_immo_versteuert_pj.append(
                steuerberechnung_etf(
                    investition=(sum(np.array(cashflow_pj)[np.array(cashflow_pj) < 0]) * -1)
                    + etf_vermoegen_immo_versteuert_pj[0],
                    endwert=etf_vermoegen_immo_pj[index_nr],
                    kapitalertragssteuer=kapitalertragssteuer,
                )
            )

            # Steigerung Instandhaltungskosten
            instandhaltungskosten_pj.append(
                instandhaltungskosten_pj[index_nr] * (1 + kostensteigerung[index_nr - 1, run])
            )
            #print(instandhaltungskosten_pj)
            nettokaltmiete_pj.append(
                nettokaltmiete_pj[index_nr] * (1 + steigerung_nettokaltmiete[index_nr - 1, run])
            )

            cashflow_pj.append(
                instandhaltungskosten_pj[index_nr + 1]
                + kreditrate_pj[index_nr]
                - nettokaltmiete_pj[index_nr + 1]
            )
        
        vermoegen_immo_pj_runs.append(vermoegen_immo_pj)
        etf_vermoegen_pj_runs.append(etf_vermoegen_pj)
        etf_vermoegen_versteuert_pj_runs.append(etf_vermoegen_versteuert_pj)
        etf_vermoegen_immo_pj_runs.append(etf_vermoegen_immo_pj)
        etf_vermoegen_immo_versteuert_pj_runs.append(etf_vermoegen_immo_versteuert_pj)
        festgeld_vermoegen_pj_runs.append(festgeld_vermoegen_pj)
        festgeld_vermoegen_immo_pj_runs.append(festgeld_vermoegen_immo_pj)
        festgeld_vermoegen_versteuert_pj_runs.append(festgeld_vermoegen_versteuert_pj)
        festgeld_vermoegen_immo_versteuert_pj_runs.append(festgeld_vermoegen_immo_versteuert_pj)
        festgeld_vermoegen_initial_pj_runs.append(festgeld_vermoegen_initial_pj)
        festgeld_vermoegen_initial_versteuert_pj_runs.append(festgeld_vermoegen_initial_versteuert_pj)
        etf_vermoegen_initial_pj_runs.append(etf_vermoegen_initial_pj)
        etf_vermoegen_initial_versteuert_pj_runs.append(etf_vermoegen_initial_versteuert_pj)
        #print(vermoegen_immo_pj_runs)
        
        #print(cashflow_pj)
    #print(etf_vermoegen_pj_runs)
    return {
        "jahr_pj":jahr_pj,
        "vermoegen_immo_pj":vermoegen_immo_pj_runs,
        
        "etf_vermoegen_pj":etf_vermoegen_pj_runs,
        "etf_vermoegen_versteuert_pj":etf_vermoegen_versteuert_pj_runs,
    
        "etf_vermoegen_immo_pj":etf_vermoegen_immo_pj_runs,
        "etf_vermoegen_immo_versteuert_pj":etf_vermoegen_immo_versteuert_pj_runs,
        
        "festgeld_vermoegen_pj":festgeld_vermoegen_pj_runs,
        "festgeld_vermoegen_immo_pj":festgeld_vermoegen_immo_pj_runs,
        "festgeld_vermoegen_versteuert_pj":festgeld_vermoegen_versteuert_pj_runs,
        "festgeld_vermoegen_immo_versteuert_pj":festgeld_vermoegen_immo_versteuert_pj_runs,
        "festgeld_vermoegen_initial_pj":festgeld_vermoegen_initial_pj_runs,
        "festgeld_vermoegen_initial_versteuert_pj":festgeld_vermoegen_initial_versteuert_pj_runs,
        
        "etf_vermoegen_initial_pj":etf_vermoegen_initial_pj_runs,
        "etf_vermoegen_initial_versteuert_pj":etf_vermoegen_initial_versteuert_pj_runs,
        "anschlusszinssatz": anschlusszinssatz,
        "kostensteigerung": kostensteigerung, 
        "wertsteigerung":wertsteigerung,
        "mietsteigerung":steigerung_nettokaltmiete,
        "zinssatz": fest_verzinst,
    }

#bla = mieten_kaufen()
#test = np.array(bla["vermoegen_immo_pj"]) 

# 2 runs 5 jahre

# print(test)
# print(test.shape)
# print(np.median(test, axis=0))
# print(np.quantile(test,q=.05, axis=0))
# print(np.quantile(test,q=.95, axis=0))




#plt.plot(jahr_pj, etf_vermoegen, label="ETF Vermoegen")
# plt.plot(jahr_pj, vermoegen_immo, label="Immo Vermoegen")
# plt.plot(jahr_pj, vermoegen_immo_versteuert_pj, label="Immo Vermoegen versteuert")
# # plt.plot(jahr_pj, verzinstes_ek_vermoegen, label="Verzinstes EK Vermoegen")
# plt.plot(
#     jahr_pj, etf_vermoegen_minus_neg_cashflows_versteuert_pj, label="ETF versteuert"
# )
# plt.title("Mieten vs. Kaufen")
# plt.legend()
# plt.show()


