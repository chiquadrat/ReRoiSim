import numpy as np

ergebnis = renditerechner(
baujahr=1925,
kaufpreis=100_000,
kaufpreis_grundstueck=30_000,
kaufpreis_sanierung=7_000,
kaufnebenkosten=5_000,
renovierungskosten=1_000,
mieteinnahmen=4_000,
instandhaltungskosten=800,
verwaltungskosten=500,
mietausfall=0.02,
mietsteigerung=0.02,
erste_mieterhoehung=5,
kostensteigerung=0.015,
# Finanzierung
eigenkapital=16_500,
zinsbindung=20,
disagio=0.01,
zinsatz=0.0128,
tilgungssatz=0.03,
anschlusszinssatz=0.05,
# Steuern
alleinstehend=False,  #
einkommen=50_000,  # zu versteuerndes Jahreseinkommen
steuerjahr=2021,  # nur 2015 und 2021 implementiert
# Renditeberechnung
anlagehorizont=20,
verkaufsfaktor=25,
# Simulation
sim_runs=100,
unsicherheit_etf_rendite=0.1,
unsicherheit_mietsteigerung=0.1,
unsicherheit_kostensteigerung=0.1,
unsicherheit_mietausfall=0.1,
unsicherheit_anschlusszinssatz=0.1,
unsicherheit_verkaufsfaktor=0.1,
etf_rendite=0.08,
)

ergebnis["etf_rendite"].mean()

np.array(ergebnis["etf_ek_rendite"]).mean()
np.array(ergebnis["etf_gewinn"]).mean()

np.array(ergebnis["eigenkapitalrendite"]).mean()
np.array(ergebnis["gewinn"]).mean()