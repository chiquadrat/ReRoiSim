import numpy as np
import matplotlib.pyplot as plt

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


## -- calculate -- ##

n_sims = 1000
n_years = 25

eink = 60000
alleinstehend = True
kreditrate=24000
zinsbindung=15000
zinsrate=0.015
kaufpreis=400000
disagio=0.03
sonderabschreibung=20000
abschreibung=30000
kosten_pa=2000
baujahr=1920

# Miete
rent = sim_rent(15000)

# Kosten
costs = sim_value(kosten_pa, mean=0.02, var=0.02)

mietausfall = sim_mietausfall()

# "Jahresreinertrag"
ertrag = rent * mietausfall - costs

# Darlehen
restschuld, zins, tilgung = get_darlehen_values(kaufpreis, zinsrate=zinsrate, kreditrate=kreditrate)

# Afa
afa_s = afa_sanierung(bemessung_sonderabschreibung=sonderabschreibung)
afa_g = afa_gebaude(baujahr, abschreibung)

# Werbungskosten
werbung = werbungskosten(kaufpreis, sonderabschreibung, disagio, zinsbindung)

# Steuerl. Ergebnis
steuer_ergebnis = (((ertrag - zins) - afa_g) - afa_s ) - werbung

# Einkommen(steuer)
steuer_vorher = np.full((n_sims, n_years), fill_value=steuerberechnung(eink, alleinstehend, 2021))
eink_vorher = np.full((n_sims, n_years), fill_value=eink)

eink_nachher = eink_vorher + steuer_ergebnis
steuer_nachher = eink_steuer_vect(eink_nachher)

steuerwirkung = steuer_vorher - steuer_nachher

# "Überschuss"
kreditrate_full = zins + tilgung
ueberschuss = ertrag - (kreditrate_full - steuerwirkung)

# Immobilienwert
asset = sim_value(kaufpreis, final_values=True)

# Ergebnisse nach Anlagehorizont
ueberschuss_final = ueberschuss[:, -1] + asset - restschuld[:, -1]

steuer_ergebnis_object = (((ertrag - zins) - afa_g) - afa_s )
eink_nachher_object = eink_vorher + steuer_ergebnis_object
steuer_nachher_object = eink_steuer_vect(eink_nachher_object)

steuerwirkung_obj = steuer_nachher_object - steuer_vorher

liquid = (ertrag + steuerwirkung_obj)
liquid[:, -1] += asset
