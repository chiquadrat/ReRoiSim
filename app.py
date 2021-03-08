import numpy as np
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_auth
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
from dash.exceptions import PreventUpdate

from formeln import renditerechner

VALID_USERNAME_PASSWORD_PAIRS = {"Trump": "Tower"}

# Initialize the app
app = dash.Dash(__name__)
server = app.server
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
# app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [
        # row zero
        html.Div(
            children=[
                # first column of row zero
                html.Div(
                    children=[html.H4("1. Kauf"),],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                    },
                ),
            ],
            className="row",
        ),
        # first row
        html.Div(
            children=[
                # first column of first row
                html.Div(
                    children=[
                        html.Label("Kaufpreis"),
                        dcc.Input(
                            id="kaufpreis",
                            placeholder="Eingabe...",
                            value=300_000,
                            min=1,
                            type="number",
                            required=True,
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
                # second column of first row
                html.Div(
                    children=[
                        html.Label("-> davon Grundstücksanteil"),
                        dcc.Input(
                            id="kaufpreis_grundstueck",
                            placeholder="Eingabe...",
                            value=100_000,
                            type="number",
                            min=0,
                            required=True,
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
                # third column of first row
                html.Div(
                    children=[
                        html.Label("-> davon Sanierungskosten"),
                        dcc.Input(
                            id="kaufpreis_sanierung",
                            placeholder="Eingabe...",
                            value=0,
                            type="number",
                            required=True,
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
            ],
            className="row",
        ),
        # second row
        html.Div(
            children=[
                # first column of second row
                html.Div(
                    children=[
                        html.Label("Kaufnebenkosten"),
                        dcc.Input(
                            id="kaufnebenkosten",
                            placeholder="Eingabe...",
                            value=40_000,
                            type="number",
                            min=0,
                            required=True,
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
                # second column of second row
                html.Div(
                    children=[
                        html.Label("Renovierungskosten"),
                        dcc.Input(
                            id="renovierungskosten",
                            placeholder="Eingabe...",
                            value=1_000,
                            type="number",
                            min=0,
                            required=True,
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
            ],
            className="row",
        ),
        # third row
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("2. Miete und laufende Kosten"),],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                    },
                ),
            ],
            className="row",
        ),
        # forth row
        html.Div(
            children=[
                # first column 
                html.Div(
                    children=[
                        html.Label("Mieteinahmen pro Jahr"),
                                dcc.Input(
                                    id="mieteinnahmen",
                                    placeholder="Eingabe...",
                                    value=12_000,
                                    type="number",
                                    min=0,
                                    required=True,
                                ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
                # second column
                html.Div(
                    children=[
                        html.Label("Mietsteigerung pro Jahr"),
                                dcc.Input(
                                    id="mietsteigerung",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=2,
                                    required=True,
                                ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
                # third column
                html.Div(
                    children=[
                        html.Label("Unsicherheit Mietsteigerung"),
                                dcc.Input(
                                    id="unsicherheit_mietsteigerung",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=1,
                                    min=0.1,
                                    required=True,
                                ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
            ],
            className="row",
        ),
            # fith row
        html.Div(
            children=[
                # first column 
                html.Div(
                    children=[
                        html.Label("Erste Mieterhöhung ab Jahr"),
                                dcc.Input(
                                    id="erste_mieterhoehung",
                                    placeholder="Eingabe...",
                                    value=5,
                                    type="number",
                                    min=1,
                                    required=True,
                                ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
                # second column
                html.Div(
                    children=[
                        html.Label("Instandhaltungskosten pro Jahr "),
                                dcc.Input(
                                    id="instandhaltungskosten",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=1_200,
                                    min=0,
                                    required=True,
                                ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
                # third column
                html.Div(
                    children=[
                        html.Label("Verwaltungskosten pro Jahr"),
                                dcc.Input(
                                    id="verwaltungskosten",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=600,
                                    min=0,
                                    required=True,
                                ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
            ],
            className="row",
        ),
    ]
)


# @app.callback(
#     Output("kennzahlen", "figure"),
#     Input("kaufpreis", "value"),
#     Input("kaufpreis_grundstueck", "value"),
#     Input("kaufpreis_sanierung", "value"),
#     Input("kaufnebenkosten", "value"),
#     Input("renovierungskosten", "value"),
#     Input("mieteinnahmen", "value"),
#     Input("mietsteigerung", "value"),
#     Input("unsicherheit_mietsteigerung", "value"),
#     Input("erste_mieterhoehung", "value"),
#     Input("instandhaltungskosten", "value"),
#     Input("verwaltungskosten", "value"),
#     Input("mietausfall", "value"),
#     Input("unsicherheit_mietausfall", "value"),
#     Input("kostensteigerung", "value"),
#     Input("unsicherheit_kostensteigerung", "value"),
#     Input("eigenkapital", "value"),
#     Input("zinsbindung", "value"),
#     Input("disagio", "value"),
#     Input("zinsatz", "value"),
#     Input("tilgungssatz", "value"),
#     Input("anschlusszinssatz", "value"),
#     Input("unsicherheit_anschlusszinssatz", "value"),
#     Input("familienstand", "value"),
#     Input("einkommen", "value"),
#     Input("baujahr", "value"),
#     #    Input("sonderabschreibung", "value"),
#     Input("anlagehorizont", "value"),
#     Input("verkaufsfaktor", "value"),
#     Input("unsicherheit_verkaufsfaktor", "value"),
#     Input("sim_runs", "value"),
# )
# def custom_figure(
#     kaufpreis,
#     kaufpreis_grundstueck,
#     kaufpreis_sanierung,
#     kaufnebenkosten,
#     renovierungskosten,
#     mieteinnahmen,
#     mietsteigerung,
#     unsicherheit_mietsteigerung,
#     erste_mieterhoehung,
#     instandhaltungskosten,
#     verwaltungskosten,
#     mietausfall,
#     unsicherheit_mietausfall,
#     kostensteigerung,
#     unsicherheit_kostensteigerung,
#     eigenkapital,
#     zinsbindung,
#     disagio,
#     zinsatz,
#     tilgungssatz,
#     anschlusszinssatz,
#     unsicherheit_anschlusszinssatz,
#     familienstand,
#     einkommen,
#     baujahr,
#     #    sonderabschreibung,
#     anlagehorizont,
#     verkaufsfaktor,
#     unsicherheit_verkaufsfaktor,
#     sim_runs,
# ):
#     # Call formeln.py here

#     # Nur zum testen, bleibt natürlich später in dem Formel Modul
#     gesamtkosten = kaufpreis + kaufnebenkosten + renovierungskosten
#     jahresreinertrag = (
#         mieteinnahmen
#         - instandhaltungskosten
#         - verwaltungskosten
#         - (mieteinnahmen * (mietausfall / 100))
#     )
#     kaufpreis_miet_verhaeltnis = round(
#         (kaufpreis + renovierungskosten) / mieteinnahmen, 1
#     )
#     anfangs_brutto_mietrendite = round((1 / kaufpreis_miet_verhaeltnis) * 100, 2)
#     anfangs_netto_mietrendite = round((jahresreinertrag / gesamtkosten) * 100, 2)

#     # Finanzierung
#     darlehen = (gesamtkosten - eigenkapital) / (1 - disagio)
#     kreditrate_jahr = darlehen * ((zinsatz / 100) + (tilgungssatz / 100))

#     fig = go.Figure(
#         data=[
#             go.Table(
#                 header=dict(values=["Startwerte", ""]),
#                 cells=dict(
#                     values=[
#                         [
#                             "Gesamtkosten",
#                             "Kaufpreis-Miet-Verhältnis",
#                             "Brutto-Mietrendite",
#                             "Netto-Mietrendite",
#                             "Darlehenshöhe",
#                             "Kreditrate (Jahr)",
#                         ],
#                         [
#                             f"{gesamtkosten}€",
#                             kaufpreis_miet_verhaeltnis,
#                             f"{anfangs_brutto_mietrendite}%",
#                             f"{anfangs_netto_mietrendite}%",
#                             f"{int(darlehen)}€",
#                             f"{int(kreditrate_jahr)}€",
#                         ],
#                     ]
#                 ),
#             )
#         ]
#     )
#     return fig


# @app.callback(
#     #   Output("kennzahlen1", "figure"),
#     Output("eingabe_verkaufsfaktor", "figure"),
#     Output("eingabe_anschlusszinssatz", "figure"),
#     Output("eingabe_mietsteigerung", "figure"),
#     Output("eingabe_kostensteigerung", "figure"),
#     Output("eingabe_mietausfall", "figure"),
#     Output("verkaufspreis", "figure"),
#     Output("objektrendite", "figure"),
#     Output("eigenkapitalrendite", "figure"),
#     Output("gewinn", "figure"),
#     Output("minimaler_cashflow", "figure"),
#     [Input("button", "n_clicks")],
#     state=[
#         State("kaufpreis", "value"),
#         State("kaufpreis_grundstueck", "value"),
#         State("kaufpreis_sanierung", "value"),
#         State("kaufnebenkosten", "value"),
#         State("renovierungskosten", "value"),
#         State("mieteinnahmen", "value"),
#         State("mietsteigerung", "value"),
#         State("unsicherheit_mietsteigerung", "value"),
#         State("erste_mieterhoehung", "value"),
#         State("instandhaltungskosten", "value"),
#         State("verwaltungskosten", "value"),
#         State("mietausfall", "value"),
#         State("unsicherheit_mietausfall", "value"),
#         State("kostensteigerung", "value"),
#         State("unsicherheit_kostensteigerung", "value"),
#         State("eigenkapital", "value"),
#         State("zinsbindung", "value"),
#         State("disagio", "value"),
#         State("zinsatz", "value"),
#         State("tilgungssatz", "value"),
#         State("anschlusszinssatz", "value"),
#         State("unsicherheit_anschlusszinssatz", "value"),
#         State("familienstand", "value"),
#         State("einkommen", "value"),
#         State("baujahr", "value"),
#         #     State('sonderabschreibung', 'value'),
#         State("anlagehorizont", "value"),
#         State("verkaufsfaktor", "value"),
#         State("unsicherheit_verkaufsfaktor", "value"),
#         State("sim_runs", "value"),
#     ],
# )
# def custom_figure(
#     button,
#     kaufpreis,
#     kaufpreis_grundstueck,
#     kaufpreis_sanierung,
#     kaufnebenkosten,
#     renovierungskosten,
#     mieteinnahmen,
#     mietsteigerung,
#     unsicherheit_mietsteigerung,
#     erste_mieterhoehung,
#     instandhaltungskosten,
#     verwaltungskosten,
#     mietausfall,
#     unsicherheit_mietausfall,
#     kostensteigerung,
#     unsicherheit_kostensteigerung,
#     eigenkapital,
#     zinsbindung,
#     disagio,
#     zinsatz,
#     tilgungssatz,
#     anschlusszinssatz,
#     unsicherheit_anschlusszinssatz,
#     familienstand,
#     einkommen,
#     baujahr,
#     #    sonderabschreibung,
#     anlagehorizont,
#     verkaufsfaktor,
#     unsicherheit_verkaufsfaktor,
#     sim_runs,
# ):
#     # Call formeln.py here

#     # Preprocessing arguments
#     if baujahr == 0:
#         baujahr = 1950
#     else:
#         baujahr = 1900

#     if familienstand == 0:
#         alleinstehend = True
#     else:
#         alleinstehend = False

#     ergebnis = renditerechner(
#         kaufpreis=kaufpreis,
#         kaufpreis_grundstueck=kaufpreis_grundstueck,
#         kaufpreis_sanierung=kaufpreis_sanierung,
#         kaufnebenkosten=kaufnebenkosten,
#         renovierungskosten=renovierungskosten,
#         mieteinnahmen=mieteinnahmen,
#         mietsteigerung=(mietsteigerung / 100),
#         unsicherheit_mietsteigerung=(unsicherheit_mietsteigerung / 100),
#         erste_mieterhoehung=erste_mieterhoehung,
#         instandhaltungskosten=instandhaltungskosten,
#         verwaltungskosten=verwaltungskosten,
#         mietausfall=(mietausfall / 100),
#         unsicherheit_mietausfall=(unsicherheit_mietausfall / 100),
#         kostensteigerung=(kostensteigerung / 100),
#         unsicherheit_kostensteigerung=(unsicherheit_kostensteigerung / 100),
#         eigenkapital=eigenkapital,
#         zinsbindung=zinsbindung,
#         disagio=(disagio / 100),
#         zinsatz=(zinsatz / 100),
#         tilgungssatz=(tilgungssatz / 100),
#         anschlusszinssatz=(anschlusszinssatz / 100),
#         unsicherheit_anschlusszinssatz=(unsicherheit_anschlusszinssatz / 100),
#         alleinstehend=alleinstehend,
#         einkommen=einkommen,
#         baujahr=baujahr,
#         anlagehorizont=anlagehorizont,
#         verkaufsfaktor=verkaufsfaktor,
#         unsicherheit_verkaufsfaktor=unsicherheit_verkaufsfaktor,
#         sim_runs=sim_runs,
#         steuerjahr=2021,
#     )

#     def figure_ein_aus_gabeparameter(eingabeparameter, name, zeichen, x, runden):
#         # Geschätzter Verkaufspreis
#         eingabeparameter = np.array(ergebnis[eingabeparameter])
#         eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]
#         if np.all(eingabeparameter == eingabeparameter[0]) == True:
#             fig = go.Figure(data=[go.Table()])
#         else:
#             fig = ff.create_distplot(
#                 [eingabeparameter], [name], show_hist=False
#             )
#             fig = fig.add_vline(
#                 x=np.quantile(eingabeparameter, q=0.5),
#                 line_width=3,
#                 line_dash="dash",
#                 line_color="black",
#                 annotation_text=f"Median: {round(np.quantile(eingabeparameter, q=0.5)*x,runden)} {zeichen}",
#                 annotation_position="top right",
#                 annotation_font_size=12,
#                 annotation_font_color="black",
#             )
#             fig = fig.add_vline(
#                 x=np.quantile(eingabeparameter, q=0.05),
#                 line_width=3,
#                 line_dash="dash",
#                 line_color="red",
#                 annotation_text=f"5% Quantil: {round(np.quantile(eingabeparameter, q=.05)*x,runden)} {zeichen}",
#                 annotation_position="bottom right",
#                 annotation_font_size=12,
#                 annotation_font_color="red",
#             )
#             fig = fig.add_vline(
#                 x=np.quantile(eingabeparameter, q=0.95),
#                 line_width=3,
#                 line_dash="dash",
#                 line_color="green",
#                 annotation_text=f"95% Quantil: {round(np.quantile(eingabeparameter, q=.95)*x,runden)} {zeichen}",
#                 annotation_position="bottom right",
#                 annotation_font_size=12,
#                 annotation_font_color="green",
#             )
#         return fig

#     fig_verkaufsfaktor = figure_ein_aus_gabeparameter(
#         eingabeparameter="verkaufsfaktor",
#         name="Verkaufsfaktor",
#         zeichen="",
#         x=1,
#         runden=0,
#     )

#     fig_anschlusszinssatz = figure_ein_aus_gabeparameter(
#         eingabeparameter="anschlusszinssatz",
#         name="Anschlusszinssatz",
#         zeichen="%",
#         x=100,
#         runden=2,
#     )

#     fig_mietsteigerung = figure_ein_aus_gabeparameter(
#         eingabeparameter="mietsteigerung",
#         name="Mietsteigerung pro Jahr",
#         zeichen="%",
#         x=100,
#         runden=2,
#     )

#     fig_kostensteigerung = figure_ein_aus_gabeparameter(
#         eingabeparameter="kostensteigerung",
#         name="Kostensteigerung pro Jahr",
#         zeichen="%",
#         x=100,
#         runden=2,
#     )

#     fig_mietausfall = figure_ein_aus_gabeparameter(
#         eingabeparameter="mietausfall",
#         name="Mietausfall pro Jahr",
#         zeichen="%",
#         x=100,
#         runden=2,
#     )

#     fig_verkaufspreis = figure_ein_aus_gabeparameter(
#         eingabeparameter="verkaufspreis",
#         name="Verkaufspreis",
#         zeichen="€",
#         x=1,
#         runden=0,
#     )

#     fig_objektrendite = figure_ein_aus_gabeparameter(
#         eingabeparameter="objektrendite",
#         name="Objektrendite",
#         zeichen="%",
#         x=100,
#         runden=2,
#     )

#     fig_eigenkapitalrendite = figure_ein_aus_gabeparameter(
#         eingabeparameter="eigenkapitalrendite",
#         name="Eigenkapitalrendite",
#         zeichen="%",
#         x=100,
#         runden=2,
#     )

#     fig_gewinn = figure_ein_aus_gabeparameter(
#         eingabeparameter="gewinn",
#         name="Gewinn",
#         zeichen="€",
#         x=1,
#         runden=0,
#     )

#     fig_minimaler_cashflow = figure_ein_aus_gabeparameter(
#         eingabeparameter="minimaler_cashflow",
#         name="Minimaler Cashflow",
#         zeichen="€",
#         x=1,
#         runden=0,
#     )


#     return (
#         fig_verkaufsfaktor,
#         fig_anschlusszinssatz,
#         fig_mietsteigerung,
#         fig_kostensteigerung,
#         fig_mietausfall,
#         fig_verkaufspreis,
#         fig_objektrendite,
#         fig_eigenkapitalrendite,
#         fig_gewinn,
#         fig_minimaler_cashflow,
#     )


if __name__ == "__main__":
    app.run_server(debug=True)
