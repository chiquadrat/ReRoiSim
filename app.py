import numpy as np
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
from dash.exceptions import PreventUpdate

from formeln import renditerechner

# Initialize the app
app = dash.Dash(__name__)
server = app.server
# app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H1("Wohnung als Kapital­anlage"),
                        html.H2("Simulation der Objektrendite"),
                        html.Div(
                            children=[
                                html.H2(""),
                                html.P("Anzahl Simulationsläufe"),
                                dcc.Input(
                                    id="sim_runs",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=250,
                                ),
                                html.H2(""),
                                html.Button("Start der Simulation", id='button'),
                                html.H2(""),
                                html.H2("1. Kauf"),
                                html.P("Kaufpreis in Euro"),
                                dcc.Input(
                                    id="kaufpreis",
                                    placeholder="Eingabe...",
                                    value=300_000,
                                    type="number",
                                ),
                                html.H2(""),
                                html.P("-> davon Grundstücksanteil"),
                                dcc.Input(
                                    id="kaufpreis_grundstueck",
                                    placeholder="Eingabe...",
                                    value=100_000,
                                    type="number",
                                ),
                                html.H2(""),
                                html.P("-> davon Sanierungskosten"),
                                dcc.Input(
                                    id="kaufpreis_sanierung",
                                    placeholder="Eingabe...",
                                    value=0,
                                    type="number",
                                ),
                                html.H2(""),
                                html.P("Kaufnebenkosten"),
                                dcc.Input(
                                    id="kaufnebenkosten",
                                    placeholder="Eingabe...",
                                    value=40_000,
                                    type="number",
                                ),
                                html.H2(""),
                                html.P("Renovierungskosten"),
                                dcc.Input(
                                    id="renovierungskosten",
                                    placeholder="Eingabe...",
                                    value=1_000,
                                    type="number",
                                ),
                                html.H2("2. Miete und laufende Kosten"),
                                html.P("Mieteinahmen pro Jahr"),
                                dcc.Input(
                                    id="mieteinnahmen",
                                    placeholder="Eingabe...",
                                    value=12_000,
                                    type="number",
                                ),
                                html.H2(""),
                                html.P("Geschätzte Mietsteigerung pro Jahr"),
                                dcc.Input(
                                    id="mietsteigerung",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=2,
                                ),
                                html.H2(""),
                                html.P("Unsicherheit Mietsteigerung"),
                                dcc.Input(
                                    id="unsicherheit_mietsteigerung",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=1,
                                ),
                                html.H2(""),
                                html.P("Erste Mieterhöhung ab Jahr"),
                                dcc.Input(
                                    id="erste_mieterhoehung",
                                    placeholder="Eingabe...",
                                    value=5,
                                    type="number",
                                ),
                                html.H2(""),
                                html.P("Instandhaltungskosten pro Jahr "),
                                dcc.Input(
                                    id="instandhaltungskosten",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=1_200,
                                ),
                                html.H2(""),
                                html.P("Verwaltungskosten pro Jahr"),
                                dcc.Input(
                                    id="verwaltungskosten",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=600,
                                ),
                                html.H2(""),
                                html.P("Pauschale für Mietausfall "),
                                dcc.Input(
                                    id="mietausfall",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=2,
                                ),
                                html.H2(""),
                                html.P("Unsicherheit Mietausfall "),
                                dcc.Input(
                                    id="unsicherheit_mietausfall",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=2,
                                ),
                                html.H2(""),
                                html.P("Geschätzte Kostensteigerung pro Jahr"),
                                dcc.Input(
                                    id="kostensteigerung",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=1.5,
                                ),
                                html.H2(""),
                                html.P("Unsicherheit Kostensteigerung"),
                                dcc.Input(
                                    id="unsicherheit_kostensteigerung",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=2,
                                ),
                                html.H2("3. Finanzierung"),
                                html.P("Eigenkapital"),
                                dcc.Input(
                                    id="eigenkapital",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=100_000,
                                ),
                                html.H2(""),
                                html.P("Zinsbindung"),
                                dcc.Input(
                                    id="zinsbindung",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=20,
                                ),
                                html.H2(""),
                                html.P("Disagio"),
                                dcc.Input(
                                    id="disagio",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=0,
                                ),
                                html.H2(""),
                                html.P("Zinssatz"),
                                dcc.Input(
                                    id="zinsatz",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=1.5,
                                ),
                                html.H2(""),
                                html.P("Tilgungssatz"),
                                dcc.Input(
                                    id="tilgungssatz",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=2.5,
                                ),
                                html.H2(""),
                                html.P("Geschätzter Anschlusszinssatz"),
                                dcc.Input(
                                    id="anschlusszinssatz",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=4,
                                ),
                                html.H2(""),
                                html.P("Unsicherheit Anschlusszinssatz"),
                                dcc.Input(
                                    id="unsicherheit_anschlusszinssatz",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=1.5,
                                ),
                                html.H2("4. Steuern"),
                                html.P("Familienstand"),
                                dcc.RadioItems(
                                    id="familienstand",
                                    options=[
                                        {"label": "Alleinstehend", "value": "0"},
                                        {
                                            "label": "Ehepaar (zusammen veranlagt)",
                                            "value": "1",
                                        },
                                    ],
                                    value="0",
                                    labelStyle={"display": "inline-block"},
                                ),
                                html.H2(""),
                                html.P("Zu versteuerndes Einkommen"),
                                dcc.Input(
                                    id="einkommen",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=100_000,
                                ),
                                html.H2(""),
                                html.P("Baujahr"),
                                dcc.RadioItems(
                                    id="baujahr",
                                    options=[
                                        {"label": "nach 1924", "value": "0"},
                                        {"label": "bis 1924", "value": "1"},
                                    ],
                                    value="0",
                                    labelStyle={"display": "inline-block"},
                                ),
                                html.H2(""),
                                # html.P("Sonderabschreibung für Neubauwohnung"),
                                # dcc.RadioItems(
                                #     id="sonderabschreibung",
                                #     options=[
                                #         {"label": "Ja", "value": "1"},
                                #         {"label": "Nein", "value": "0"},
                                #              ],
                                #     value="0",
                                #     labelStyle={"display": "inline-block"},
                                # ),
                                html.H2("5. Renditeberechnung"),
                                html.P("Anlagehorizont"),
                                dcc.Input(
                                    id="anlagehorizont",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=15,
                                ),
                                html.H2(""),
                                html.P("Geschätzter Verkaufsfaktor"),
                                dcc.Input(
                                    id="verkaufsfaktor",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=22,
                                ),
                                html.H2(""),
                                html.P("Unsicherheit Verkaufsfaktor"),
                                dcc.Input(
                                    id="unsicherheit_verkaufsfaktor",
                                    placeholder="Eingabe...",
                                    type="number",
                                    value=5,
                                ),
                                html.H2(""),
                                html.H2(""),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        html.H1("Berechnungen"),
                        html.H2("Startwerte"),
                        dcc.Graph(id="kennzahlen"),
                        html.H2("Verteilung der mit Unsicherheit behafteten Eingabeparameter"),
                        dcc.Graph(id="eingabe_verkaufsfaktor"),
                        dcc.Graph(id="eingabe_anschlusszinssatz"),
                        dcc.Graph(id="eingabe_mietsteigerung"),
                        dcc.Graph(id="eingabe_kostensteigerung"),
                        dcc.Graph(id="eingabe_mietausfall"),
                        html.H2("Ergebnisse der Simulation"),
                        #dcc.Graph(id="kennzahlen1"),
                        dcc.Graph(id="verkaufspreis"),
                        dcc.Graph(id="objektrendite"),
                        dcc.Graph(id="eigenkapitalrendite"),
                        dcc.Graph(id="gewinn"),         
                        dcc.Graph(id="minimaler_cashflow"),         
                    ],
                ),
            ],
        )
    ]
)


@app.callback(
    Output("kennzahlen", "figure"),
    Input("kaufpreis", "value"),
    Input("kaufpreis_grundstueck", "value"),
    Input("kaufpreis_sanierung", "value"),
    Input("kaufnebenkosten", "value"),
    Input("renovierungskosten", "value"),
    Input("mieteinnahmen", "value"),
    Input("mietsteigerung", "value"),
    Input("unsicherheit_mietsteigerung", "value"),
    Input("erste_mieterhoehung", "value"),
    Input("instandhaltungskosten", "value"),
    Input("verwaltungskosten", "value"),
    Input("mietausfall", "value"),
    Input("unsicherheit_mietausfall", "value"),
    Input("kostensteigerung", "value"),
    Input("unsicherheit_kostensteigerung", "value"),
    Input("eigenkapital", "value"),
    Input("zinsbindung", "value"),
    Input("disagio", "value"),
    Input("zinsatz", "value"),
    Input("tilgungssatz", "value"),
    Input("anschlusszinssatz", "value"),
    Input("unsicherheit_anschlusszinssatz", "value"),
    Input("familienstand", "value"),
    Input("einkommen", "value"),
    Input("baujahr", "value"),
#    Input("sonderabschreibung", "value"),
    Input("anlagehorizont", "value"),
    Input("verkaufsfaktor", "value"),
    Input("unsicherheit_verkaufsfaktor", "value"),
    Input("sim_runs", "value"),
)
def custom_figure(
    kaufpreis,
    kaufpreis_grundstueck,
    kaufpreis_sanierung,
    kaufnebenkosten,
    renovierungskosten,
    mieteinnahmen,
    mietsteigerung,
    unsicherheit_mietsteigerung,
    erste_mieterhoehung,
    instandhaltungskosten,
    verwaltungskosten,
    mietausfall,
    unsicherheit_mietausfall,
    kostensteigerung,
    unsicherheit_kostensteigerung,
    eigenkapital,
    zinsbindung,
    disagio,
    zinsatz,
    tilgungssatz,
    anschlusszinssatz,
    unsicherheit_anschlusszinssatz,
    familienstand,
    einkommen,
    baujahr,
#    sonderabschreibung,
    anlagehorizont,
    verkaufsfaktor,
    unsicherheit_verkaufsfaktor,
    sim_runs,
):
    # Call formeln.py here

    # Nur zum testen, bleibt natürlich später in dem Formel Modul
    gesamtkosten = kaufpreis + kaufnebenkosten + renovierungskosten
    jahresreinertrag = (
        mieteinnahmen
        - instandhaltungskosten
        - verwaltungskosten
        - (mieteinnahmen * (mietausfall / 100))
    )
    kaufpreis_miet_verhaeltnis = round(
        (kaufpreis + renovierungskosten) / mieteinnahmen, 1
    )
    anfangs_brutto_mietrendite = round((1 / kaufpreis_miet_verhaeltnis) * 100, 2)
    anfangs_netto_mietrendite = round((jahresreinertrag / gesamtkosten) * 100, 2)

    # Finanzierung
    darlehen = (gesamtkosten - eigenkapital) / (1 - disagio)
    kreditrate_jahr = darlehen * ((zinsatz / 100) + (tilgungssatz / 100))

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=["Startwerte", ""]),
                cells=dict(
                    values=[
                        [
                            "Gesamtkosten",
                            "Kaufpreis-Miet-Verhältnis",
                            "Brutto-Mietrendite",
                            "Netto-Mietrendite",
                            "Darlehenshöhe",
                            "Kreditrate (Jahr)",
                        ],
                        [
                            f"{gesamtkosten}€",
                            kaufpreis_miet_verhaeltnis,
                            f"{anfangs_brutto_mietrendite}%",
                            f"{anfangs_netto_mietrendite}%",
                            f"{int(darlehen)}€",
                            f"{int(kreditrate_jahr)}€",
                        ],
                    ]
                ),
            )
        ]
    )
    return fig


@app.callback(
 #   Output("kennzahlen1", "figure"),
    Output("eingabe_verkaufsfaktor", "figure"),
    Output("eingabe_anschlusszinssatz", "figure"),
    Output("eingabe_mietsteigerung", "figure"),
    Output("eingabe_kostensteigerung", "figure"),
    Output("eingabe_mietausfall", "figure"),
    Output("verkaufspreis", "figure"),
    Output("objektrendite", "figure"),
    Output("eigenkapitalrendite", "figure"),
    Output("gewinn", "figure"),
    Output("minimaler_cashflow", "figure"),
    [Input('button', 'n_clicks')],
    state=[
     State('kaufpreis', 'value'),
     State('kaufpreis_grundstueck', 'value'),
     State('kaufpreis_sanierung', 'value'),
     State('kaufnebenkosten', 'value'),
     State('renovierungskosten', 'value'),
     State('mieteinnahmen', 'value'),
     State('mietsteigerung', 'value'),
     State('unsicherheit_mietsteigerung', 'value'),
     State('erste_mieterhoehung', 'value'),
     State('instandhaltungskosten', 'value'),
     State('verwaltungskosten', 'value'),
     State('mietausfall', 'value'),
     State('unsicherheit_mietausfall', 'value'),
     State('kostensteigerung', 'value'),
     State('unsicherheit_kostensteigerung', 'value'),
     State('eigenkapital', 'value'),
     State('zinsbindung', 'value'),
     State('disagio', 'value'),
     State('zinsatz', 'value'),
     State('tilgungssatz', 'value'),
     State('anschlusszinssatz', 'value'),
     State('unsicherheit_anschlusszinssatz', 'value'),
     State('familienstand', 'value'),
     State('einkommen', 'value'),
     State('baujahr', 'value'),
#     State('sonderabschreibung', 'value'),
     State('anlagehorizont', 'value'),
     State('verkaufsfaktor', 'value'),
     State('unsicherheit_verkaufsfaktor', 'value'),
     State('sim_runs', 'value')
     ])

def custom_figure(
    button,
    kaufpreis,
    kaufpreis_grundstueck,
    kaufpreis_sanierung,
    kaufnebenkosten,
    renovierungskosten,
    mieteinnahmen,
    mietsteigerung,
    unsicherheit_mietsteigerung,
    erste_mieterhoehung,
    instandhaltungskosten,
    verwaltungskosten,
    mietausfall,
    unsicherheit_mietausfall,
    kostensteigerung,
    unsicherheit_kostensteigerung,
    eigenkapital,
    zinsbindung,
    disagio,
    zinsatz,
    tilgungssatz,
    anschlusszinssatz,
    unsicherheit_anschlusszinssatz,
    familienstand,
    einkommen,
    baujahr,
#    sonderabschreibung,
    anlagehorizont,
    verkaufsfaktor,
    unsicherheit_verkaufsfaktor,
    sim_runs,
):
    # Call formeln.py here
    
    # Preprocessing arguments
    if baujahr==0:
        baujahr=1950
    else:
        baujahr=1900
    
    if familienstand==0:
        alleinstehend=True
    else:
        alleinstehend=False
    
    ergebnis = renditerechner(
        kaufpreis=kaufpreis, 
        kaufpreis_grundstueck=kaufpreis_grundstueck,
        kaufpreis_sanierung=kaufpreis_sanierung,
        kaufnebenkosten=kaufnebenkosten,
        renovierungskosten=renovierungskosten,
        mieteinnahmen=mieteinnahmen,
        mietsteigerung=(mietsteigerung/100),
        unsicherheit_mietsteigerung=(unsicherheit_mietsteigerung/100),
        erste_mieterhoehung=erste_mieterhoehung,
        instandhaltungskosten=instandhaltungskosten,
        verwaltungskosten=verwaltungskosten,
        mietausfall=(mietausfall/100),
        unsicherheit_mietausfall=(unsicherheit_mietausfall/100),
        kostensteigerung=(kostensteigerung/100),
        unsicherheit_kostensteigerung=(unsicherheit_kostensteigerung/100),
        eigenkapital=eigenkapital,
        zinsbindung=zinsbindung,
        disagio=(disagio/100),
        zinsatz=(zinsatz/100),
        tilgungssatz=(tilgungssatz/100),
        anschlusszinssatz=(anschlusszinssatz/100),
        unsicherheit_anschlusszinssatz=(unsicherheit_anschlusszinssatz/100),
        alleinstehend=alleinstehend,
        einkommen=einkommen,
        baujahr=baujahr,
        anlagehorizont=anlagehorizont,
        verkaufsfaktor=verkaufsfaktor,
        unsicherheit_verkaufsfaktor=unsicherheit_verkaufsfaktor,
        sim_runs=sim_runs,
        steuerjahr=2021,
    )
    
    

    # tab1 = go.Figure(
    #     data=[
    #         go.Table(
    #             header=dict(values=["Startwerte", ""]),
    #             cells=dict(
    #                 values=[
    #                     [
    #                         "button",
    #                         "verkaufspreis",
    #                         "eigenkapitalrendite",
    #                         "kaufpreis",
    #                         "kaufpreis_grundstueck",
    #                         "kaufpreis_sanierung",
    #                         "familienstand",
    #                         "baujahr",
    #                         "sim_runs"
    #                     ],
    #                     [
    #                         button,
    #                         ergebnis["verkaufspreis"],
    #                         ergebnis["eigenkapitalrendite"],
    #                         kaufpreis,
    #                         kaufpreis_grundstueck,
    #                         kaufpreis_sanierung,
    #                         familienstand,
    #                         baujahr,
    #                         sim_runs
    #                     ],
    #                 ]
    #             ),
    #         )
    #     ]
    # )
    
    def figure_eingabeparameter(eingabeparameter, name, zeichen,x, runden):
        # Geschätzter Verkaufspreis
        eingabeparameter = np.array(ergebnis[eingabeparameter])
        eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]
        if np.all(eingabeparameter==eingabeparameter[0])==True:
                fig_eingabeparameter = go.Figure(
                    data=[
                        go.Table(
                        
                        )
                    ]
                )
        else:
            fig_eingabeparameter = ff.create_distplot([eingabeparameter], [name], show_hist=False)
            fig_eingabeparameter = fig_eingabeparameter.add_vline(
                x=np.quantile(eingabeparameter, q=0.5), line_width=3, line_dash="dash",
                line_color="black",
            annotation_text=f"Median: {round(np.quantile(eingabeparameter, q=0.5)*x,runden)} {zeichen}",
            annotation_position="top right",
            annotation_font_size=10,
            annotation_font_color="black"
                )
            fig_eingabeparameter = fig_eingabeparameter.add_vline(
                x=np.quantile(eingabeparameter, q=.05), line_width=3, line_dash="dash",
                line_color="red",
                annotation_text=f"5% Quantil: {round(np.quantile(eingabeparameter, q=.05)*x,runden)} {zeichen}",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="red"
                )
            fig_eingabeparameter = fig_eingabeparameter.add_vline(
                x=np.quantile(eingabeparameter, q=.95), line_width=3, line_dash="dash",
                line_color="green",
                annotation_text=f"95% Quantil: {round(np.quantile(eingabeparameter, q=.95)*x,runden)} {zeichen}",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="green"
                )
        return fig_eingabeparameter
    
    
    fig_verkaufsfaktor = figure_eingabeparameter(eingabeparameter="verkaufsfaktor", 
                                                   name="Verkaufsfaktor", 
                                                   zeichen="",
                                                   x=1,
                                                   runden=0)
    
    fig_anschlusszinssatz = figure_eingabeparameter(eingabeparameter="anschlusszinssatz", 
                                                name="Anschlusszinssatz", 
                                                zeichen="%",
                                                x=100,
                                                runden=2)
    
    fig_mietsteigerung = figure_eingabeparameter(eingabeparameter="mietsteigerung", 
                                            name="Mietsteigerung pro Jahr", 
                                            zeichen="%",
                                            x=100,
                                            runden=2)

    fig_kostensteigerung = figure_eingabeparameter(eingabeparameter="kostensteigerung", 
                                            name="Kostensteigerung pro Jahr", 
                                            zeichen="%",
                                            x=100,
                                            runden=2)

    fig_mietausfall = figure_eingabeparameter(eingabeparameter="mietausfall", 
                                            name="Mietausfall pro Jahr", 
                                            zeichen="%",
                                            x=100,
                                            runden=2)

    
    
    # Geschätzter Verkaufspreis
    verkaufspreis = np.array(ergebnis["verkaufspreis"])
    verkaufspreis = verkaufspreis[~np.isnan(verkaufspreis)]
    if np.all(verkaufspreis==verkaufspreis[0])==True:
            fig_verkaufspreis = go.Figure(
                data=[
                    go.Table(
                     
                    )
                ]
            )
    else:
        fig_verkaufspreis = ff.create_distplot([verkaufspreis], ["Verkaufspreis"], show_hist=False)
        fig_verkaufspreis = fig_verkaufspreis.add_vline(
            x=np.quantile(verkaufspreis, q=0.5), line_width=3, line_dash="dash",
            line_color="black",
        annotation_text=f"Median: {round(np.quantile(verkaufspreis, q=0.5))} €",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color="black"
            )
        fig_verkaufspreis = fig_verkaufspreis.add_vline(
            x=np.quantile(verkaufspreis, q=.05), line_width=3, line_dash="dash",
            line_color="red",
            annotation_text=f"5% Quantil: {round(np.quantile(verkaufspreis, q=.05))} €",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="red"
            )
        fig_verkaufspreis = fig_verkaufspreis.add_vline(
            x=np.quantile(verkaufspreis, q=.95), line_width=3, line_dash="dash",
            line_color="green",
            annotation_text=f"95% Quantil: {round(np.quantile(verkaufspreis, q=.95))} €",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="green"
            )
    
    # Geschätzte Objektrendite
    objektrendite = np.array(ergebnis["objektrendite"])
    objektrendite = objektrendite[~np.isnan(objektrendite)]
    if np.all(objektrendite==objektrendite[0])==True:
            fig_objektrendite = go.Figure(
                data=[
                    go.Table(
                     
                    )
                ]
            )
    else:
        fig_objektrendite = ff.create_distplot([objektrendite], ["Objektrendite"], show_hist=False)
        fig_objektrendite = fig_objektrendite.add_vline(
            x=np.quantile(objektrendite, q=0.5), line_width=3, line_dash="dash",
            line_color="black",
        annotation_text=f"Median: {round(np.quantile(objektrendite, q=0.5)*100, 2)} %",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color="black"
            )
        fig_objektrendite = fig_objektrendite.add_vline(
            x=np.quantile(objektrendite, q=.05), line_width=3, line_dash="dash",
            line_color="red",
            annotation_text=f"5% Quantil: {round(np.quantile(objektrendite, q=.05)*100, 2)} %",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="red"
            )
        fig_objektrendite = fig_objektrendite.add_vline(
            x=np.quantile(objektrendite, q=.95), line_width=3, line_dash="dash",
            line_color="green",
            annotation_text=f"95% Quantil: {round(np.quantile(objektrendite, q=.95)*100, 2)} %",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="green"
            )

    # Geschätzte Eigenkapitalrendite
    eigenkapitalrendite = np.array(ergebnis["eigenkapitalrendite"])
    eigenkapitalrendite = eigenkapitalrendite[~np.isnan(eigenkapitalrendite)]
    if np.all(eigenkapitalrendite==eigenkapitalrendite[0])==True:
            fig_eigenkapitalrendite = go.Figure(
                data=[
                    go.Table(
                    
                    )
                ]
            )
    else:
        fig_eigenkapitalrendite = ff.create_distplot([eigenkapitalrendite], ["Eigenkapitalrendite"], show_hist=False)
        fig_eigenkapitalrendite = fig_eigenkapitalrendite.add_vline(
            x=np.quantile(eigenkapitalrendite, q=0.5), line_width=3, line_dash="dash",
            line_color="black",
        annotation_text=f"Median: {round(np.quantile(eigenkapitalrendite, q=0.2)*100, 2)} %",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color="black"
            )
        fig_eigenkapitalrendite = fig_eigenkapitalrendite.add_vline(
            x=np.quantile(eigenkapitalrendite, q=.05), line_width=3, line_dash="dash",
            line_color="red",
            annotation_text=f"5% Quantil: {round(np.quantile(eigenkapitalrendite, q=.05)*100, 2)} %",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="red"
            )
        fig_eigenkapitalrendite = fig_eigenkapitalrendite.add_vline(
            x=np.quantile(eigenkapitalrendite, q=.95), line_width=3, line_dash="dash",
            line_color="green",
            annotation_text=f"95% Quantil: {round(np.quantile(eigenkapitalrendite, q=.95)*100, 2)} %",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="green"
            )
            
    # Geschätzte Gewinn
    gewinn = np.array(ergebnis["gewinn"])
    gewinn = gewinn[~np.isnan(gewinn)]
    #print(gewinn)
    #print(gewinn.shape)
    if np.all(gewinn==gewinn[0])==True:
            fig_gewinn = go.Figure(
                data=[
                    go.Table(
                    
                    )
                ]
            )
    else:
        fig_gewinn = ff.create_distplot([gewinn], ["Gewinn"], show_hist=False)
        fig_gewinn = fig_gewinn.add_vline(
            x=np.quantile(gewinn, q=0.5), line_width=3, line_dash="dash",
            line_color="black",
        annotation_text=f"Median: {round(np.quantile(gewinn, q=0.5))} €",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color="black"
            )
        fig_gewinn = fig_gewinn.add_vline(
            x=np.quantile(gewinn, q=.05), line_width=3, line_dash="dash",
            line_color="red",
            annotation_text=f"5% Quantil: {round(np.quantile(gewinn, q=.05))} €",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="red"
            )
        fig_gewinn = fig_gewinn.add_vline(
            x=np.quantile(gewinn, q=.95), line_width=3, line_dash="dash",
            line_color="green",
            annotation_text=f"95% Quantil: {round(np.quantile(gewinn, q=.95))} €",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="green"
            )
        
    # Geschätzter minimaler Cashflow
    minimaler_cashflow = np.array(ergebnis["minimaler_cashflow"])
    minimaler_cashflow = minimaler_cashflow[~np.isnan(minimaler_cashflow)]
    #print(minimaler_cashflow)
    #print(minimaler_cashflow.shape)
    if np.all(minimaler_cashflow==minimaler_cashflow[0])==True:
            fig_minimaler_cashflow = go.Figure(
                data=[
                    go.Table(
                    
                    )
                ]
            )
    else:
        fig_minimaler_cashflow = ff.create_distplot([minimaler_cashflow], ["Minimaler Cashflow"], show_hist=False)
        fig_minimaler_cashflow = fig_minimaler_cashflow.add_vline(
            x=np.quantile(minimaler_cashflow, q=0.5), line_width=3, line_dash="dash",
            line_color="black",
        annotation_text=f"Median: {round(np.quantile(minimaler_cashflow, q=0.5))} €",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color="black"
            )
        fig_minimaler_cashflow = fig_minimaler_cashflow.add_vline(
            x=np.quantile(minimaler_cashflow, q=.05), line_width=3, line_dash="dash",
            line_color="red",
            annotation_text=f"5% Quantil: {round(np.quantile(minimaler_cashflow, q=.05))} €",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="red"
            )
        fig_minimaler_cashflow = fig_minimaler_cashflow.add_vline(
            x=np.quantile(minimaler_cashflow, q=.95), line_width=3, line_dash="dash",
            line_color="green",
            annotation_text=f"95% Quantil: {round(np.quantile(minimaler_cashflow, q=.95))} €",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="green"
            )



    
    
    return fig_verkaufsfaktor, fig_anschlusszinssatz, fig_mietsteigerung, fig_kostensteigerung, fig_mietausfall, fig_verkaufspreis, fig_objektrendite, fig_eigenkapitalrendite, fig_gewinn, fig_minimaler_cashflow





if __name__ == "__main__":
    app.run_server(debug=True)
