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
sim_runs=1,
unsicherheit_etf_rendite=0.05,
unsicherheit_mietsteigerung=0.05,
unsicherheit_kostensteigerung=0.05,
unsicherheit_mietausfall=0.05,
unsicherheit_anschlusszinssatz=0.05,
unsicherheit_verkaufsfaktor=0.05,
etf_rendite=0.08,
)

import plotly.figure_factory as ff

ergebnis["etf_rendite"].mean()

np.array(ergebnis["etf_ek_rendite"]).mean()
np.array(ergebnis["etf_gewinn"]).mean()

np.array(ergebnis["eigenkapitalrendite"]).mean()
np.array(ergebnis["gewinn"]).mean()

eingabeparameter = np.array(ergebnis["eigenkapitalrendite"])
eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]

eingabeparameter2 = np.array(ergebnis["etf_ek_rendite"])
eingabeparameter2 = eingabeparameter2[~np.isnan(eingabeparameter2)]

fig = ff.create_distplot([eingabeparameter2, eingabeparameter], ["EKR Bude", "EKR ETF"], 
                         show_hist=False, show_rug=False)

fig = fig.add_vline(
                    x=np.quantile(eingabeparameter, q=0.5),
                    line_width=3,
                    line_dash="dash",
                    line_color="orange",
                    annotation_text=f"Median: {round(np.quantile(eingabeparameter, q=0.5)*100,0)} %",
                    annotation_position="top left",
                    annotation_font_size=12,
                    annotation_font_color="black",
                )

fig = fig.add_vline(
                    x=np.quantile(eingabeparameter2, q=0.5),
                    line_width=3,
                    line_dash="dash",
                    line_color="blue",
                    annotation_text=f"Median: {round(np.quantile(eingabeparameter2, q=0.5)*100,0)} %",
                    annotation_position="top right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                )
fig.update_yaxes(rangemode="tozero")
fig.update_layout(plot_bgcolor="white")
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
fig.update_layout(title="EKR Rendite Immobilie vs. ETF")
fig

print(f"In {round((sum(eingabeparameter > eingabeparameter2)/len(eingabeparameter2))*100, 2)} % der Fälle hätten Sie mit einer ETF Investition eine höhere Rendite erziehlt.")

eingabeparameter3 = np.array(ergebnis["gewinn"])
eingabeparameter3 = eingabeparameter3[~np.isnan(eingabeparameter3)]

eingabeparameter4 = np.array(ergebnis["etf_gewinn"])
eingabeparameter4 = eingabeparameter4[~np.isnan(eingabeparameter4)]

fig = ff.create_distplot([eingabeparameter3, eingabeparameter4], ["Gewinn Bude", "Gewinn ETF"], 
                         show_hist=False, show_rug=False)

fig = fig.add_vline(
                    x=np.quantile(eingabeparameter3, q=0.5),
                    line_width=3,
                    line_dash="dash",
                    line_color="blue",
                    annotation_text=f"Median: {int(np.quantile(eingabeparameter3, q=0.5))} €",
                    annotation_position="top left",
                    annotation_font_size=12,
                    annotation_font_color="black",
                )

fig = fig.add_vline(
                    x=np.quantile(eingabeparameter4, q=0.5),
                    line_width=3,
                    line_dash="dash",
                    line_color="orange",
                    annotation_text=f"Median: {int(np.quantile(eingabeparameter4, q=0.5))} €",
                    annotation_position="top right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                )
fig.update_yaxes(rangemode="tozero")
fig.update_layout(plot_bgcolor="white")
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
fig.update_layout(title="Gewinn Immobilie vs. Gewinn ETF")
fig

