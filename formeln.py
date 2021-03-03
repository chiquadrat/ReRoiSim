#
# Ziel: Berechnung der Rendite einer Immobilie
#

import numpy as np
import numpy_financial as npf
import truncated_normal
import steuerberechnung

# Todo: Verkaufsfaktor durch Immobilienpreissteierung ersetzen


################################################################################
#
# Eingabeparameter
#
################################################################################


def renditerechner(
    # Objekt
    baujahr=1925,
    kaufpreis=100_000,
    kaufpreis_grundstueck=30_000,
    kaufpreis_sanierung=7_000,
    kaufnebenkosten=5_000,
    renovierungskosten=1_000,
    mieteinnahmen=5_000,
    instandhaltungskosten=800,
    verwaltungskosten=500,
    mietausfall=0.02,
    mietsteigerung=0.02,
    erste_mieterhoehung=5,
    kostensteigerung=0.015,
    # Finanzierung
    eigenkapital=6_500,
    zinsbindung=15,
    disagio=0.01,
    zinsatz=0.0128,
    tilgungssatz=0.03,
    anschlusszinssatz=0.05,
    # Steuern
    alleinstehend=False,  #
    einkommen=50_000,  # zu versteuerndes Jahreseinkommen
    steuerjahr=2021,  # nur 2015 und 2021 implementiert
    # Renditeberechnung
    anlagehorizont=30,
    verkaufsfaktor=25,
    # Simulation
    sim_runs=1,
    unsicherheit_mietsteigerung=0,
    unsicherheit_kostensteigerung=0,
    unsicherheit_mietausfall=0,
    unsicherheit_anschlusszinssatz=0,
    unsicherheit_verkaufsfaktor=0,
):
    """Funktion simuliert die Eigenkapitalrendite, Objektrendite und den 
    Verkaufspreis

    Args:
        baujahr (int, optional): [description]. Defaults to 1925.
        kaufpreis (float, optional): [description]. Defaults to 100_000.
        kaufpreis_grundstueck (float, optional): [description]. Defaults to 30_000.
        kaufpreis_sanierung (float, optional): [description]. Defaults to 7_000.
        kaufnebenkosten (float, optional): [description]. Defaults to 5_000.
        renovierungskosten (float, optional): [description]. Defaults to 1_000.
        mieteinnahmen (float, optional): [description]. Defaults to 5_000.
        instandhaltungskosten (float, optional): [description]. Defaults to 800.
        verwaltungskosten (float, optional): [description]. Defaults to 500.
        mietausfall (float, optional): [description]. Defaults to 0.02.
        mietsteigerung (float, optional): [description]. Defaults to 0.02.
        erste_mieterhoehung (int, optional): [description]. Defaults to 5.
        kostensteigerung (float, optional): [description]. Defaults to 0.015.
        eigenkapital (float, optional): [description]. Defaults to 6_500.
        zinsbindung (int, optional): [description]. Defaults to 15.
        disagio (float, optional): [description]. Defaults to 0.01.
        zinsatz (float, optional): [description]. Defaults to 0.0128.
        tilgungssatz (float, optional): [description]. Defaults to 0.03.
        anschlusszinssatz (float, optional): [description]. Defaults to 0.05.
        alleinstehend (bool, optional): [description]. Defaults to False.
        verkaufsfaktor (float, optional): [description]. Defaults to 25.
        sim_runs (int, optional): [description]. Defaults to 1.
        unsicherheit_mietsteigerung (float, optional): [description]. Defaults to 0.
        unsicherheit_kostensteigerung (float, optional): [description]. Defaults to 0.
        unsicherheit_mietausfall (float, optional): [description]. Defaults to 0.
        unsicherheit_anschlusszinssatz (float, optional): [description]. Defaults to 0.
        unsicherheit_verkaufsfaktor (float, optional): [description]. Defaults to 0.

    Returns:
        verkaufspreis: [description] 
        eigenkapitalrendite: [description] 
        objektrendite: [description]
    """

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
    # anschlussrate_jahr = darlehen * (tilgungssatz + anschlusszinssatz)

    # Steuern
    bemessung_abschreibung = (
        kaufpreis
        + kaufnebenkosten
        - (kaufpreis_grundstueck + kaufpreis_sanierung)
        * (1 + kaufnebenkosten / kaufpreis)
    )
    abschreibungsart = "Linear 2,0%" if baujahr > 1924 else "Linear 2,5%"
    bemessung_sonderabschreibung = kaufpreis_sanierung * gesamtkosten / kaufpreis

    verkaufspreis_runs = []
    eigenkapitalrendite_runs = []
    objektrendite_runs = []
    gewinn_runs = []
    minimaler_cashflow_runs = []

    # Unabhängige Simulation
    verkaufsfaktor = np.random.normal(
        verkaufsfaktor, unsicherheit_verkaufsfaktor, sim_runs
    )

    anschlusszinssatz = np.random.normal(
        anschlusszinssatz, unsicherheit_anschlusszinssatz, sim_runs
    )

    mietsteigerung = np.random.normal(
        mietsteigerung, unsicherheit_mietsteigerung, sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)

    kostensteigerung = np.random.normal(
        kostensteigerung, unsicherheit_kostensteigerung, sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)

    if unsicherheit_mietausfall == 0:
        mietausfall = np.random.normal(
            mietausfall, unsicherheit_mietausfall, sim_runs * anlagehorizont
        ).reshape(anlagehorizont, sim_runs)
    else:
        mietausfall = truncated_normal.trunc_samples(
        mu=mietausfall, sigma=unsicherheit_mietausfall,
        lower=0, upper=100, num_samples=sim_runs * anlagehorizont
    ).reshape(anlagehorizont, sim_runs)
   
    for run in range(sim_runs):
        jahr_pj = [0]
        mieteinnahmen_pj = [0]  # pj -> pro jahr
        nicht_umlegbare_kosten_pj = [0]
        mietausfall_pj = [0]
        jahresreinertrag_pj = [0]
        hilfsfeld_rate_pj = [0]
        kreditrate_pj = [0]
        zinssatz_pj = [0]
        zins_pj = [0]
        tilgung_pj = [0]
        restschuld_pj = [darlehen]
        bemessung_afa_gebaeude_pj = [0]
        afasatz_gebaeude_pj = [0]
        afa_gebaeude_pj = [0]
        bemessung_afa_sanierung_pj = [0]
        afasatz_sanierung_pj = [0]
        afa_sanierung_pj = [0]
        werbungskosten_pj = [0]
        steuerliches_ergebnis_ekr_pj = [0]
        einkommen_vorher_pj = [0]
        steuern_vorher_pj = [0]
        einkommen_nachher_ekr_pj = [0]
        steuern_nachher_ekr_pj = [0]
        steuerwirkung_ekr_pj = [0]
        ueberschuss_pj = [0]
        immobilienpreis_pj = [0]
        verkaufspreis_pj = [0]
        restschuld_faellig_pj = [0]
        ueberschuss_gesamt_pj = [-eigenkapital]
        steuerliches_ergebnis_objekt_pj = [0]
        einkommen_nachher_objekt_pj = [0]
        steuern_nachher_objekt_pj = [0]
        steuerwirkung_objekt_pj = [0]
        liquiditaet_pj = [-gesamtkosten]

        anschlussrate_jahr = darlehen * (tilgungssatz + anschlusszinssatz[run])

        for index_nr in range(1, anlagehorizont + 1):
            # index_nr = 1

            # Jahr
            jahr_pj.append(index_nr)

            # Mieteinahmen
            if jahr_pj[index_nr] < erste_mieterhoehung:
                mieteinnahmen_pj.append(mieteinnahmen)
            elif jahr_pj[index_nr] >= erste_mieterhoehung:
                mieteinnahmen_pj.append(
                    mieteinnahmen_pj[-1] * (1 + mietsteigerung[index_nr - 1, run])
                )

            # nicht umlegbare Kosten
            if jahr_pj[index_nr] == 1:
                nicht_umlegbare_kosten_pj.append(
                    instandhaltungskosten + verwaltungskosten
                )
            elif jahr_pj[index_nr] > 1:
                nicht_umlegbare_kosten_pj.append(
                    nicht_umlegbare_kosten_pj[-1]
                    * (1 + kostensteigerung[index_nr - 1, run])
                )

            # Pauschale für Mietausfall
            mietausfall_pj.append(
                mieteinnahmen_pj[index_nr] * mietausfall[index_nr - 1, run]
            )

            # Jahresreinertrag
            jahresreinertrag_pj.append(
                mieteinnahmen_pj[index_nr]
                - nicht_umlegbare_kosten_pj[index_nr]
                - mietausfall_pj[index_nr]
            )

            # Hilfsfeld Rate
            if jahr_pj[index_nr] <= zinsbindung:
                hilfsfeld_rate_pj.append(kreditrate_jahr)
            else:
                hilfsfeld_rate_pj.append(anschlussrate_jahr)

            # Zinssatz
            if jahr_pj[index_nr] <= zinsbindung:
                zinssatz_pj.append(zinsatz)
            else:
                zinssatz_pj.append(anschlusszinssatz[run])

            # Zins
            zins_pj.append(restschuld_pj[index_nr - 1] * zinssatz_pj[index_nr])

            # Kreditrate
            if hilfsfeld_rate_pj[index_nr] > restschuld_pj[index_nr - 1]:
                kreditrate_pj.append(
                    restschuld_pj[index_nr - 1] * (1 + zinssatz_pj[index_nr])
                )
            else:
                kreditrate_pj.append(hilfsfeld_rate_pj[index_nr])

            # Tilgung
            tilgung_pj.append(kreditrate_pj[index_nr] - zins_pj[index_nr])

            # Restschuld
            restschuld_pj.append(restschuld_pj[index_nr - 1] - tilgung_pj[index_nr])

            # Bemessung für Afa
            bemessung_afa_gebaeude_pj.append(bemessung_abschreibung)

            # Afasatz Gebäude
            if baujahr > 1924:
                afasatz_gebaeude_pj.append(0.02)
            else:
                afasatz_gebaeude_pj.append(0.025)

            # Afa Gebäude
            afa_gebaeude_pj.append(
                bemessung_afa_gebaeude_pj[index_nr] * afasatz_gebaeude_pj[index_nr]
            )

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
            afa_sanierung_pj.append(
                bemessung_afa_sanierung_pj[index_nr] * afasatz_sanierung_pj[index_nr]
            )

            # Werbungskosten (Sofortabzug)
            if jahr_pj[index_nr] == 1:
                if jahr_pj[index_nr] <= zinsbindung:
                    if disagio > 0.05:
                        werbungskosten_pj.append(
                            renovierungskosten + disagio * darlehen / zinsbindung
                        )
                    else:
                        werbungskosten_pj.append(
                            renovierungskosten + disagio * darlehen
                        )
                else:
                    werbungskosten_pj.append(renovierungskosten + 0)
            elif jahr_pj[index_nr] > 1:
                if jahr_pj[index_nr] <= zinsbindung:
                    if disagio > 0.05:
                        werbungskosten_pj.append(disagio * darlehen / zinsbindung)
                    else:
                        werbungskosten_pj.append(0)
                else:
                    werbungskosten_pj.append(0)

            # Steuerliches Ergebnis für die Berechnung der Eigenkapitalrendite
            steuerliches_ergebnis_ekr_pj.append(
                jahresreinertrag_pj[index_nr]
                - zins_pj[index_nr]
                - afa_gebaeude_pj[index_nr]
                - afa_sanierung_pj[index_nr]
                - werbungskosten_pj[index_nr]
            )

            # Einkommen vorher
            einkommen_vorher_pj.append(einkommen)

            # Steuern vorher
            steuern_vorher_pj.append(
                steuerberechnung.steuerberechnung(
                    einkommen_vorher_pj[index_nr], not (alleinstehend), steuerjahr
                )
            )

            # Einkommen nachher für die Berechnung der Eigenkapitalrendite
            einkommen_nachher_ekr_pj.append(
                einkommen_vorher_pj[index_nr] + steuerliches_ergebnis_ekr_pj[index_nr]
            )

            # Steuern nachher für die Berechnung der Eigenkapitalrendite
            steuern_nachher_ekr_pj.append(
                steuerberechnung.steuerberechnung(
                    einkommen_nachher_ekr_pj[index_nr], not (alleinstehend), steuerjahr
                )
            )

            # Steuerwirkung für die Berechnung der Eigenkapitalrendite
            steuerwirkung_ekr_pj.append(
                steuern_nachher_ekr_pj[index_nr] - steuern_vorher_pj[index_nr]
            )

            # Überschuss ohne Anfangsinvestition, Verkauf und Restschuld
            ueberschuss_pj.append(
                jahresreinertrag_pj[index_nr]
                - kreditrate_pj[index_nr]
                - steuerwirkung_ekr_pj[index_nr]
            )

            # Immobilienpreis
            immobilienpreis_pj.append(mieteinnahmen_pj[index_nr] * verkaufsfaktor[run])

            # Verkaufspreis am Ende des Anlagehorizontes
            if jahr_pj[index_nr] == anlagehorizont:
                verkaufspreis_pj.append(immobilienpreis_pj[index_nr])
            else:
                verkaufspreis_pj.append(0)

                # fällige Restschuld zum Ende des Anlagehorizontes
            if jahr_pj[index_nr] == anlagehorizont:
                restschuld_faellig_pj.append(restschuld_pj[index_nr])
            else:
                restschuld_faellig_pj.append(0)

            # Überschuss inkl. Verkauf und Restschuld
            ueberschuss_gesamt_pj.append(
                ueberschuss_pj[index_nr]
                + verkaufspreis_pj[index_nr]
                - restschuld_faellig_pj[index_nr]
            )

            # Steuerliches Ergebnis für die Berechnung der Objektrendite
            if jahr_pj[index_nr] == 1:
                steuerliches_ergebnis_objekt_pj.append(
                    jahresreinertrag_pj[index_nr]
                    - afa_gebaeude_pj[index_nr]
                    - afa_sanierung_pj[index_nr]
                    - renovierungskosten
                )
            elif jahr_pj[index_nr] > 1:
                steuerliches_ergebnis_objekt_pj.append(
                    jahresreinertrag_pj[index_nr]
                    - afa_gebaeude_pj[index_nr]
                    - afa_sanierung_pj[index_nr]
                )

            # Einkommen nachher für die Berechnung der Objektrendite
            einkommen_nachher_objekt_pj.append(
                einkommen_vorher_pj[index_nr]
                + steuerliches_ergebnis_objekt_pj[index_nr]
            )

            # Steuern nachher für die Berechnung der Objektrendite
            steuern_nachher_objekt_pj.append(
                steuerberechnung.steuerberechnung(
                    einkommen_nachher_objekt_pj[index_nr],
                    not (alleinstehend),
                    steuerjahr,
                )
            )

            # Steuerwirkung für die Berechnung der Objektrendite
            steuerwirkung_objekt_pj.append(
                steuern_nachher_objekt_pj[index_nr] - steuern_vorher_pj[index_nr]
            )

            # Liquidität
            liquiditaet_pj.append(
                jahresreinertrag_pj[index_nr]
                - steuerwirkung_objekt_pj[index_nr]
                + verkaufspreis_pj[index_nr]
            )

        # Verkaufspreis
        # print(verkaufspreis_pj)
        verkaufspreis_runs.append(sum(verkaufspreis_pj))

        # Berechnung der Eigenkapitalrendite : interner Zinsfuß der Zahlungsreihe ueberschuss_gesamt_pj
        eigenkapitalrendite_runs.append(npf.irr(ueberschuss_gesamt_pj))
        # print(ueberschuss_gesamt_pj)

        # Berechnung der Objektrendite : interner Zinsfuß der Zahlungsreihe liquiditaet_pj
        objektrendite_runs.append(npf.irr(liquiditaet_pj))

        # Gewinn (Summe über die Cashflows)
        gewinn_runs.append(sum(ueberschuss_gesamt_pj))
        minimaler_cashflow_runs.append(min(ueberschuss_gesamt_pj[1:]))

    return {
        "verkaufspreis": verkaufspreis_runs,
        "eigenkapitalrendite": eigenkapitalrendite_runs,
        "objektrendite": objektrendite_runs,
        "gewinn": gewinn_runs,
        "minimaler_cashflow": minimaler_cashflow_runs,
        "mietsteigerung": mietsteigerung,
        "kostensteigerung": kostensteigerung,
        "mietausfall": mietausfall,
        "anschlusszinsatz": anschlusszinssatz,
        "verkaufsfaktor": verkaufsfaktor,
        "gesamtkosten":gesamtkosten,
        "kaufpreis_miet_verhaeltnis": kaufpreis_miet_verhaeltnis,
        "anfangs_brutto_mietrendite": anfangs_brutto_mietrendite,
        "anfangs_netto_mietrendite": anfangs_netto_mietrendite,
        "darlehen":darlehen,
        "kreditrate_jahr":kreditrate_jahr,
        "verkaufsfaktor":verkaufsfaktor,
        "anschlusszinssatz":anschlusszinssatz,
        "mietsteigerung":mietsteigerung.flatten(),
        "kostensteigerung":kostensteigerung.flatten(),
        "mietausfall":mietausfall.flatten(),
    }


# ergebnis = renditerechner()
# print(ergebnis)