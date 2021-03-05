import numpy as np
import numpy_financial as npf

# asset value
def sim_value(start_val, n_sims=1000, n_years=25, mean=0.01, var=0.015, final_values=False):

    # initialize data structures
    start_arr = np.full(n_sims, fill_value=start_val)
    returns = np.random.normal(mean + 1, var, size=(n_sims, n_years))

    # calculate
    if final_values:
        final_returns = np.prod(returns, axis=1)
        final_values = np.multiply(final_returns, start_arr) # single value per sim
        return final_values
    else:
        yearly_returns = np.cumproduct(returns, axis=1)
        yearly_values = np.multiply(start_arr.reshape(-1, 1), yearly_returns) # values per year and sim
        return yearly_values


# rent income
def sim_rent(start_val, n_sims=1000, n_years=25, flat_years=5, mean=0.05, var=0.03, final_values=False):

    start_arr = np.full((n_sims, 1), fill_value=start_val)
    rent_incrs = np.random.normal(mean + 1, var, size=(n_sims, n_years // flat_years))
    rent_incrs[:, 0] = 1.0

    rent_rel = np.cumproduct(rent_incrs, axis=1)
    rent_abs = np.multiply(start_arr, rent_rel)

    rent_final = np.concatenate(
                                [np.repeat(rent_abs[:, i].reshape(-1, 1), flat_years, axis=1) for i in range(rent_abs.shape[1])], 
                                axis=1
                                )

    return rent_final


# "Mietausfall"
def sim_mietausfall(p=0.02, n_sims=1000, n_years=25):
    # 2% reduction per period -> constant
    # return np.full((n_sims, n_years), fill_value=0.02)

    # alternative: random sparse matrix (i.e. complete loss in this year)
    return np.random.binomial(n=1, p=1-p, size=n_sims*n_years).reshape(n_sims, n_years)


# Darlehen
def get_darlehen_values(start_val, n_sims=1000, n_years=25, zinsrate=0.015, kreditrate=24000):
    # pdb.set_trace()

    restschuld = [start_val]
    for _ in range(n_years - 1):
        restschuld.append(restschuld[-1] - (kreditrate - restschuld[-1] * zinsrate))

    restschuld = np.asarray(restschuld).clip(0)
    restschuld_full = np.repeat(restschuld[None], n_sims, axis=0)

    zinsrate_full = np.full((n_sims, n_years), fill_value=zinsrate)
    interest = np.multiply(restschuld_full, zinsrate_full)

    # TODO: adjust last year of tilgung to be the same as restschuld
    tilgung = np.full((n_sims, n_years), fill_value=kreditrate) - interest
    tilgung[kreditrate == tilgung] = 0

    return restschuld_full, interest, tilgung


## AFA Gebäude

# bemessung_abschreibung = (
#     kaufpreis
#     + kaufnebenkosten
#     - (kaufpreis_grundstueck + kaufpreis_sanierung) * (1 + kaufnebenkosten / kaufpreis)
# )

def afa_gebaude(baujahr, bemessung_abschreibung, n_sims=1000, n_years=25):
    
    abschreibungssatz = 0.02 if baujahr > 1924 else 0.025
    return np.full((n_sims, n_years), fill_value=bemessung_abschreibung*abschreibungssatz)


# AFA Sanierung
# bemessung_sonderabschreibung = kaufpreis_sanierung * gesamtkosten / kaufpreis

def afa_sanierung(bemessung_sonderabschreibung, n_sims=1000, n_years=25):

    afa_sanierung = np.concatenate(
        [
            np.full((n_sims, min(n_years, 13)), fill_value=bemessung_sonderabschreibung),
            np.zeros((n_sims, max(n_years-13, 0))),
        ],
        axis=1
    )

    afas_sanierung = np.concatenate(
        [
            np.full((n_sims, min(n_years, 9)), fill_value=0.09),
            np.full((n_sims, min(max(n_years-9, 0), 4)), fill_value=0.07),
            np.zeros((n_sims, max(n_years-13, 0))),
        ],
        axis=1
    )

    return np.multiply(afa_sanierung, afas_sanierung)


# "Werbungskosten"
# first year: 
# if Disagio > 0.05: Renovierung + disagio * darlehen / zinsbindung
# else: Renovierung + disagio * darlehen

# following years:
# else Disagio > 0.05: disagio * darlehen / zinsbindung; else: 0

def werbungskosten(darlehen, renovierung, disagio, zinsbindung, n_sims=1000, n_years=25):

    werbung = np.zeros((n_sims, n_years))
    if disagio > 0.05:
        werbung[:, 0] = renovierung + disagio * darlehen / zinsbindung
        werbung[:, 1:zinsbindung] = disagio * darlehen / zinsbindung
    else:
        werbung[:, 0] = renovierung + disagio * darlehen

    return werbung


# income tax
from steuerberechnung import steuerberechnung

# TODO: vectorize einkommensteuer
def eink_steuer_vect(eink_array, alleinstehend=True, jahr=2021):
    return np.apply_along_axis(lambda x: np.asarray([steuerberechnung(s, alleinstehend, 2021) for s in x]),
                                axis=0,
                                arr=eink_array)


# def steuern_calc(steuer_ergebnis, eink=60000, alleinstehend=True, n_sims=1000, n_years=25):
    # steuer_vorher = np.full((n_sims, n_years), fill_value=steuerberechnung(eink, alleinstehend, 2021))
    # eink_vorher = np.full((n_sims, n_years), fill_value=eink)

    # eink_nachher = eink_vorher + steuer_ergebnis

    # steuer_nachher = eink_steuer_vect(eink_nachher)

    # steuerwirkung = steuer_vorher - steuer_nachher

    # return steuerwirkung, eink_vorher, steuer_vorher, eink_nachher, steuer_nachher

# steuerwirkung, eink_vorher, steuer_vorher, eink_nachher, steuer_nachher = steuern_calc(steuer_ergebnis)


def renditerechner_vect(
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
    """Dokumentation Eingabe/Ausgabeparameter siehe formeln.py"""

    ## -- Abgeleitete Parameter -- ##

    n_sims = sim_runs
    n_years = anlagehorizont

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
    bemessung_sonderabschreibung = kaufpreis_sanierung * gesamtkosten / kaufpreis


    ## Simulation

    # Miete
    # rent = sim_rent(mieteinnahmen, n_sims, n_years, flat_years=erste_mieterhoehung, 
    #                 mean=mietsteigerung, var=unsicherheit_mietsteigerung)
    rent_increase = sim_rent(1, n_sims, n_years, mean=mietsteigerung, var=unsicherheit_mietsteigerung)
    rent = np.multiply(np.full((n_sims, n_years), fill_value=mieteinnahmen), rent_increase)

    # Kosten
    # costs = sim_value(verwaltungskosten + instandhaltungskosten, 
    #                   n_sims, n_years,
    #                   mean=kostensteigerung, 
    #                   var=unsicherheit_kostensteigerung)
    cost_increase = sim_value(1, n_sims, n_years, mean=kostensteigerung, var=unsicherheit_kostensteigerung)
    costs = np.multiply(np.full((n_sims, n_years), fill_value=verwaltungskosten+instandhaltungskosten), cost_increase)

    mietausfall = sim_mietausfall(mietausfall, n_sims, n_years)

    # "Jahresreinertrag"
    ertrag = rent * mietausfall - costs

    # Darlehen
    restschuld, zins, tilgung = get_darlehen_values(kaufpreis, n_sims, n_years, zinsrate=zinsatz, kreditrate=kreditrate_jahr)

    anschlusszinssatz = sim_value(zinsatz, mean=0.1, var=unsicherheit_anschlusszinssatz, n_sims=n_sims, n_years=1).flatten()

    # Afa
    afa_s = afa_sanierung(bemessung_sonderabschreibung, n_sims, n_years)
    afa_g = afa_gebaude(baujahr, bemessung_abschreibung, n_sims, n_years)

    # Werbungskosten
    werbung = werbungskosten(kaufpreis, bemessung_sonderabschreibung, disagio, zinsbindung, n_sims, n_years)

    # Steuerl. Ergebnis
    steuer_ergebnis = (((ertrag - zins) - afa_g) - afa_s ) - werbung

    # Einkommen(steuer)
    steuer_vorher = np.full((n_sims, n_years), fill_value=steuerberechnung(einkommen, alleinstehend, steuerjahr))
    eink_vorher = np.full((n_sims, n_years), fill_value=einkommen)

    eink_nachher = eink_vorher + steuer_ergebnis
    steuer_nachher = eink_steuer_vect(eink_nachher)

    steuerwirkung = steuer_vorher - steuer_nachher

    # "Überschuss"
    kreditrate_full = zins + tilgung
    ueberschuss = ertrag - (kreditrate_full - steuerwirkung)

    # Immobilienwert
    # TODO: unsicherheit_verkaufsfaktor korrekt umrechnen
    asset = sim_value(kaufpreis, n_sims, n_years, final_values=True)

    # Ergebnisse nach Anlagehorizont
    ueberschuss[:, -1] = ueberschuss[:, -1] + asset - restschuld[:, -1]

    steuer_ergebnis_object = (((ertrag - zins) - afa_g) - afa_s )
    eink_nachher_object = eink_vorher + steuer_ergebnis_object
    steuer_nachher_object = eink_steuer_vect(eink_nachher_object)

    steuerwirkung_obj = steuer_nachher_object - steuer_vorher

    liquid = (ertrag + steuerwirkung_obj)
    liquid[:, -1] += asset

    ## finale Werte pro Sim
    verkaufspreis = asset
    verkaufsfaktor = asset / rent[:, -1]

    gewinn = np.sum(ueberschuss, axis=1)
    min_cashflow = np.min(ueberschuss, axis=1)

    ek_rendite = np.apply_along_axis(npf.irr, axis=1, arr=ueberschuss)
    obj_rendite = np.apply_along_axis(npf.irr, axis=1, arr=liquid)

    return {
        "verkaufspreis": verkaufspreis, #.tolist(), # 1d
        "eigenkapitalrendite": ek_rendite, #.tolist(), # 1d
        "objektrendite": obj_rendite, #.tolist(), # 1d
        "gewinn": gewinn, #.tolist(), # 1d
        "minimaler_cashflow": min_cashflow, #.tolist(), # 1d
        "mietsteigerung": rent_increase.flatten(), # 2d -> 1d
        "kostensteigerung": cost_increase.flatten(), # 2d -> 1d
        "mietausfall": mietausfall.flatten(), # 2d -> 1d
        "anschlusszinsatz": anschlusszinssatz, # 1d
        "verkaufsfaktor": verkaufsfaktor, # 1d
        "gesamtkosten": gesamtkosten, # scalar
        "kaufpreis_miet_verhaeltnis": kaufpreis_miet_verhaeltnis, # scalar
        "anfangs_brutto_mietrendite": anfangs_brutto_mietrendite, # scalar
        "anfangs_netto_mietrendite": anfangs_netto_mietrendite, # scalar
        "darlehen": darlehen, # scalar
        "kreditrate_jahr": kreditrate_jahr, # scalar
    }


if __name__=="__main__":

    result = renditerechner_vect()
    print(result)