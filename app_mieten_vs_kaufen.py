import numpy as np
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable
import dash_table
import dash_auth
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
from dash.exceptions import PreventUpdate
from scipy.stats import iqr

# Import
import base64
import io
import xlrd

# Export
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import openpyxl

from formeln import renditerechner
from text import text_generator, text_static
from simulation_mieten_vs_kaufen import mieten_kaufen

#VALID_USERNAME_PASSWORD_PAIRS = {
#                                "Immobilien":"Simulator",
#                                "Christoph": "Groener",
#                                 "Jack":"Singer"}

# Initialize the app
app = dash.Dash(__name__)
server = app.server
#auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
# app.config.suppress_callback_exceptions = True

#
# Statische Texte
#

text_statisch = text_static()

app.layout = html.Div(
    [
                # row zero
        html.Div(
            children=[
                # first column of row zero
                html.Div(
                    children=[html.H3("Mieten vs. Kaufen - Simulator"),
                              dcc.Markdown(text_statisch["einleitung"]),],
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
        # row zero
        html.Div(
            children=[
                # first column of row zero
                html.Div(
                    children=[html.H4("1. Kennzahlen Immobilie"),],
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
                        html.Label("Kaufpreis (Euro)"),
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
                # third column of first row
                html.Div(
                    children=[
                        html.Label("Kaufnebenkosten (Euro)",
                                  # title="nach § 7h oder § 7i EStG: Nur für die Sanierung von Baudenkmälern und Gebäuden in Sanierungsgebieten"
                                  ),
                        dcc.Input(
                            id="kaufnebenkosten",
                            placeholder="Eingabe...",
                            value=10000,
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
                        html.Label("Instandhaltungskosten",
                                   #title="Umfassen Makler und Notarkosten sowie die Grunderwerbssteuer."
                                   ),
                        dcc.Input(
                            id="instandhaltungskosten",
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
                        html.Label("Kostensteigerung Instandhaltungskosten (%)",
                                   #title="Kosten die im Jahr des Kaufs anfallen und steuerlich Absetzbar sind (Sanierungskosten dürfen 15% der Gebäudekosten nicht überschreiten)."
                                   ),
                        dcc.Input(
                            id="kostensteigerung",
                            placeholder="Eingabe...",
                            value=1.5,
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
                html.Div(
                    children=[
                        html.Label("Unsicherheit Kostensteigerung",
                                   #title="Kosten die im Jahr des Kaufs anfallen und steuerlich Absetzbar sind (Sanierungskosten dürfen 15% der Gebäudekosten nicht überschreiten)."
                                   ),
                        dcc.Input(
                            id="unsicherheit_kostensteigerung",
                            placeholder="Eingabe...",
                            value=1.5,
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
        # next row
        html.Div(
            children=[
                # first column of second row
                html.Div(
                    children=[
                        html.Label("Wertsteigerung Immobilie (%)",
                                   #title="Umfassen Makler und Notarkosten sowie die Grunderwerbssteuer."
                                   ),
                        dcc.Input(
                            id="wertsteigerung",
                            placeholder="Eingabe...",
                            value=1.5,
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
                        html.Label("Unsicherheit Wertsteigerung (%)",
                                   #title="Kosten die im Jahr des Kaufs anfallen und steuerlich Absetzbar sind (Sanierungskosten dürfen 15% der Gebäudekosten nicht überschreiten)."
                                   ),
                        dcc.Input(
                            id="unsicherheit_wertsteigerung",
                            placeholder="Eingabe...",
                            value=1.5,
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
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("2. Finanzierung Immobilie"),],
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
        # row nine
        html.Div(
            children=[
                # first column
                html.Div(
                    children=[
                        html.Label("Eigenkapital (Euro)"),
                        dcc.Input(
                            id="eigenkapital",
                            placeholder="Eingabe...",
                            type="number",
                            value=100_000,
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
                        html.Label("Zinsbindung (Jahre)"),
                        dcc.Input(
                            id="zinsbindung",
                            placeholder="Eingabe...",
                            type="number",
                            value=20,
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
                
                                html.Div(
                    children=[
                        html.Label("Zinssatz (%)"),
                        dcc.Input(
                            id="zinssatz",
                            placeholder="Eingabe...",
                            type="number",
                            value=1.5,
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
        # row ten
        html.Div(
            children=[


                # second column
                html.Div(
                    children=[
                        html.Label("Tilgungssatz (%)"),
                        dcc.Input(
                            id="tilgungssatz",
                            placeholder="Eingabe...",
                            type="number",
                            value=2.5,
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
                        html.Label("Anschlusszinssatz (%)",
                                   title="Erwartungswert"),
                        dcc.Input(
                            id="anschlusszinssatz",
                            placeholder="Eingabe...",
                            type="number",
                            value=4,
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
                
                html.Div(
                    children=[
                        html.Label("Unsicherheit Anschlusszinssatz (%)",
                                   title="Standardabweichung"),
                        dcc.Input(
                            id="unsicherheit_anschlusszinssatz",
                            placeholder="Eingabe...",
                            type="number",
                            value=1.5,
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
        # row eleven
        # html.Div(
        #     children=[
        #         # first column

        #     ],
        #     className="row",
        # ),     
        # third row
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("3. Wohnen zur Miete"),],
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
                        html.Label("Nettokaltmiete (Euro)",
                                   #title="Nettokaltmiete"
                                   ),
                        dcc.Input(
                            id="nettokaltmiete",
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
                        html.Label("Mietsteigerung (%)",
                                  title="Erwartungswert"
                                   ),
                        dcc.Input(
                            id="steigerung_nettokaltmiete",
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
                        html.Label("Unsicherheit Mietsteigerung (%)",
                                   title="Standardabweichung"
                                  ),
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

        # row twelve
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("4. Steuern"),],
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
        # row thirteen
        html.Div(
            children=[
                # first column
                html.Div(
                    children=[
                        html.Label("Familienstand"),
                        dcc.RadioItems(
                            id="familienstand",
                            options=[
                                {"label": "alleinstehend", "value": "0"},
                                {
                                    "label": "Ehepaar (zusammen veranlagt)",
                                    "value": "1",
                                },
                            ],
                            value="0",
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
                        html.Label("zu versteuerndes Einkommen (Euro)"),
                        dcc.Input(
                            id="einkommen",
                            placeholder="Eingabe...",
                            type="number",
                            value=100_000,
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
        # row fourteen
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("5. Renditeberechnung"),],
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
        # row fiveteen
        html.Div(
            children=[
                # first column
                html.Div(
                    children=[
                        html.Label("Anlagehorizont (Jahre)"),
                        dcc.Input(
                            id="anlagehorizont",
                            placeholder="Eingabe...",
                            type="number",
                            value=15,
                            min=10,
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
                        html.Label("Zinssatz fest verzinste Anlage (%)"),
                                 #  title="Kaufpreis-Miet-Verhältnis (Erwartungswert)"),
                        dcc.Input(
                            id="verzinsung_ek",
                            placeholder="Eingabe...",
                            type="number",
                            value=22,
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
                # third column
                html.Div(
                    children=[
                        html.Label("Unsicherheit Zinsatz (%)",
                                   title="Standardabweichung"),
                        dcc.Input(
                            id="unsicherheit_verzinsung_ek",
                            placeholder="Eingabe...",
                            type="number",
                            value=4,
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
        # row fourteen
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.Label("ETF Vergleich"),
                        dcc.RadioItems(
                            id="etf_vergleich",
                            options=[
                                {"label": "MSCI World (einschließlich Dividenden)", "value": "0"},
                                {"label": "Dax (einschließlich Dividenden)","value": "1",},
                            ],
                            value="0",
                        ),],
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
        # row sixteen
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("6. Import/Export der Eingabeparameter"),
                              dcc.Markdown(text_statisch["export_import"]),],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                        "margin-right": "10vw",
                    },
                ),
            ],
            className="row",
        ),

        # row sixteen
        html.Div(
            children=[
                    # third column
                    html.Div(
            children=[
                # first column of third row
                html.Button("Eingabe exportieren", id='download-results-button'),
                Download(id='download'),                
            ],                    
            style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                    ),
                # first column of third row
                html.Div(
                    children=[
                            dcc.Upload(
        id='upload-data',
        children=html.Div([
            'DATEN IMPORTIEREN',
            #html.A('Select Files')
        ]),
        style={
            'width': "210px",
            'height': '38px',
            'lineHeight': '35px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '4px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "2.3vw",
                        "margin-top": "0vw",
                    },
                ),
                # second column
                                html.Div(
                    children=[
           dcc.Markdown(id='upload-status')
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
        
        # row sixteen
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("7. Simulation"),
                              dcc.Markdown(text_statisch["simulation"]),],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                        "margin-right": "10vw",
                    },
                ),
            ],
            className="row",
        ),
        # row seventeen
        html.Div(
            children=[
                # first column
                html.Div(
                    children=[
                        html.Label("Anzahl der Simulationsläufe"),
                        dcc.Input(
                            id="sim_runs",
                            placeholder="Eingabe...",
                            type="number",
                            value=250,
                            min=2,
                            max=10_000,
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
        # row eighteen
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.Button("Start der Simulation", id="button"),
],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
                ),
            html.Div(
                children=[
                                                          dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1")
        ),
                    
                ],
                                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "1vw",
                    },
            )
            ],
            className="row",
        ),
        
        # 21
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[
                        html.H4(
                            "Verteilung der mit Unsicherheit behafteten Eingabeparameter"
                        ),
                        dcc.Markdown(text_statisch["eingabeparameter"]),
                        html.H4("Ergebnisse der Simulation"),
                        dcc.Markdown(text_statisch["ergebnisse"]),
                        dcc.Graph(id="mieten_vs_kaufen"),                        
                        html.H4("8. Disclaimer"),
                        dcc.Markdown(text_statisch["haftungsausschluss"]),
                    ],
                    style={
                        # "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                        "margin-right": "10vw",
                    },
                ),
            ],
            className="row",
        ),
    ],
    className="container",
)



#
# Callbacks
#

@app.callback(
    Output('mieten_vs_kaufen', 'children'),
    [Input("button", "n_clicks")],
    state=[
        State("kaufpreis", "value"),
        State("renovierungskosten", "value"),
        State("kaufnebenkosten", "value"),
        State("instandhaltungskosten", "value"),
        State("kostensteigerung", "value"),
        State("unsicherheit_kostensteigerung", "value"),
        State("wertsteigerung", "value"),
        State("unsicherheit_wertsteigerung", "value"),
        State("eigenkapital", "value"),
        State("zinsbindung", "value"),
        State("zinssatz", "value"),
        State("tilgungssatz", "value"),
        State("anschlusszinssatz", "value"),
        State("unsicherheit_anschlusszinssatz", "value"),
        State("nettokaltmiete", "value"),
        State("steigerung_nettokaltmiete", "value"),
        State("unsicherheit_mietsteigerung", "value"),
        State("familienstand", "value"),
        State("einkommen", "value"),
        State("anlagehorizont", "value"),
        State("verzinsung_ek", "value"),
        State("unsicherheit_verzinsung_ek", "value"),
        State("etf_vergleich", "value"),

    ],
)
def custom_figure(
    button,
    kaufpreis,
   renovierungskosten,
   kaufnebenkosten,
   instandhaltungskosten,
   kostensteigerung,
   unsicherheit_kostensteigerung,
   wertsteigerung,
   unsicherheit_wertsteigerung,
   eigenkapital,
   zinsbindung,
   zinssatz,
   tilgungssatz,
   anschlusszinssatz,
   unsicherheit_anschlusszinssatz,
   nettokaltmiete,
   steigerung_nettokaltmiete,
   unsicherheit_mietsteigerung,
   familienstand,
   einkommen,
   anlagehorizont,
   verzinsung_ek,
   unsicherheit_verzinsung_ek,
   etf_vergleich,
):
    
    if int(familienstand) == 0:
        alleinstehend = True
    else:
        alleinstehend = False
        
    if int(etf_vergleich)==0:    # MSCI World
        etf_rendite = 0.1046
        unsicherheit_etf_rendite = 0.1711
        name2 = "MSCI World"
    elif int(etf_vergleich)==1:  # Dax
        etf_rendite = 0.1095
        unsicherheit_etf_rendite = 0.2276
        name2 = "Dax"

    ergebnis = mieten_kaufen(
        anlagehorizont=anlagehorizont,
        alleinstehend=alleinstehend,
        einkommen=einkommen,
        steuerjahr=2021,
        kaufpreis=kaufpreis,
        renovierungskosten=renovierungskosten,
        kaufnebenkosten=kaufnebenkosten,
        instandhaltungskosten=instandhaltungskosten,
        kostensteigerung=kostensteigerung,
        unsicherheit_kostensteigerung=unsicherheit_kostensteigerung,
        wertsteigerung=wertsteigerung,
        unsicherheit_wertsteigerung=unsicherheit_wertsteigerung,
        eigenkapital=eigenkapital,
        zinsbindung=zinsbindung,
        zinssatz=zinssatz,
        tilgungssatz=tilgungssatz,
        anschlusszinssatz=anschlusszinssatz,
        unsicherheit_anschlusszinssatz=unsicherheit_anschlusszinssatz,
        nettokaltmiete=nettokaltmiete,
        steigerung_nettokaltmiete=steigerung_nettokaltmiete,
        unsicherheit_mietsteigerung=unsicherheit_mietsteigerung,
        etf_rendite = etf_rendite,
        unsicherheit_etf_rendite=unsicherheit_etf_rendite,
        verzinsung_ek=verzinsung_ek,
        unsicherheit_verzinsung_ek=unsicherheit_verzinsung_ek,
        
    )

    def figure_ein_aus_gabeparameter(eingabeparameter, name, zeichen, x, runden, area):
        if name == "Minimaler Cashflow":
            eingabeparameter = np.array(ergebnis[eingabeparameter])
            eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]
            upper_bound = np.quantile(eingabeparameter, q=0.75) + 4.5 * iqr(eingabeparameter)
            lower_bound = np.quantile(eingabeparameter, q=0.75) - 4.5 * iqr(eingabeparameter)
            eingabeparameter = eingabeparameter[(eingabeparameter > lower_bound) & (eingabeparameter < upper_bound)]
        else:        
            eingabeparameter = np.array(ergebnis[eingabeparameter])
            eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]
        
        if np.all(eingabeparameter == eingabeparameter[0]) == True:
            fig = go.Figure(data=[go.Table()])
        else:
            fig = ff.create_distplot([eingabeparameter], 
                                     [name], 
                                     show_hist=False, show_rug=False)
            
            if (name=="Verkaufspreis") and (eingabeparameter.min() < kaufpreis):
                #print(len(eingabeparameter[eingabeparameter<kaufpreis])/len(eingabeparameter))
                fig = fig.add_vline(
                x=kaufpreis,
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{round(len(eingabeparameter[eingabeparameter<kaufpreis])/len(eingabeparameter)*100,2)} % Quantil",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",
                annotation_bgcolor="white",)
            elif (name=="Gewinn") and (eingabeparameter.min() < 0):
                #print(len(eingabeparameter[eingabeparameter<kaufpreis])/len(eingabeparameter))
                fig = fig.add_vline(
                x=0,
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{round(len(eingabeparameter[eingabeparameter<0])/len(eingabeparameter)*100,2)} % Quantil",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",
                annotation_bgcolor="white",)
            elif (name=="Objektrendite" or name=="Eigenkapitalrendite") and (eingabeparameter.min()<0):
                fig = fig.add_vline(
                x=0,
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{round(len(eingabeparameter[eingabeparameter<0])/len(eingabeparameter)*100,2)} % Quantil",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",
                annotation_bgcolor="white",)                
            else:
                if runden==0:
                    annotation_tmp = f"5% Quantil: {int(np.quantile(eingabeparameter, q=.05)*x)} {zeichen}" 
                else:
                    annotation_tmp = f"5% Quantil: {round(np.quantile(eingabeparameter, q=.05)*x,runden)} {zeichen}"
                fig = fig.add_vline(
                    x=np.quantile(eingabeparameter, q=0.05),
                    line_width=3,
                    line_dash="dash",
                    line_color="black",
                    annotation_text=annotation_tmp,
                    annotation_position="bottom right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                    annotation_bgcolor="white",
                )
            if runden==0:
                annotation_tmp = f"95% Quantil: {int(np.quantile(eingabeparameter, q=.95)*x)} {zeichen}" 
            else:
                annotation_tmp = f"95% Quantil: {round(np.quantile(eingabeparameter, q=.95)*x,runden)} {zeichen}"            
            fig = fig.add_vline(
                    x=np.quantile(eingabeparameter, q=0.95),
                    line_width=3,
                    line_dash="dash",
                    line_color="black",
                    annotation_text=annotation_tmp,
                    annotation_position="bottom right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                    annotation_bgcolor="white",
                )

            if runden==0:
                annotation_tmp = f"Median: {int(np.quantile(eingabeparameter, q=0.5)*x)} {zeichen}" 
            else:
                annotation_tmp = f"Median: {round(np.quantile(eingabeparameter, q=0.5)*x,runden)} {zeichen}"                            
            fig = fig.add_vline(
                    x=np.quantile(eingabeparameter, q=0.5),
                    line_width=3,
                    line_dash="dash",
                    line_color="black",
                    annotation_text=annotation_tmp,
                    annotation_position="top right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                    annotation_bgcolor="white",
                )
            
            # fig = fig.add_vline(
            #         x=eingabeparameter.mean(),
            #         line_width=3,
            #         line_dash="dash",
            #         line_color="red",
            #         annotation_text="",
            #         annotation_position="top right",
            #         annotation_font_size=12,
            #         annotation_font_color="black",
            #     )

            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(plot_bgcolor="white")
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
            fig.update_layout(showlegend=False)
            fig.update_layout(title=name)
            
            
            if area == "middle":
                xl = np.quantile(eingabeparameter, q=0.05)
                xr = np.quantile(eingabeparameter, q=0.95)
                x1   = [xc   for xc in fig.data[0].x if xc <xl]
                y1   = fig.data[0].y[:len(x1)]

                x2   = [xc   for xc in fig.data[0].x if xc > xr]
                y2   = fig.data[0].y[-len(x2):]

                x3 = [xc   for xc in fig.data[0].x if (xc > xl) and (xc < xr)]
                y3 = fig.data[0].y[len(x1):-len(x2)]

                fig.add_scatter(x=x3, y=y3,fill='tozeroy', 
                                mode='none' , fillcolor='lightblue',
                                name=name)
            
                #fig.add_scatter(x=x1, y=y1,fill='tozeroy', mode='none' , fillcolor="red")
                #fig.add_scatter(x=x2, y=y2,fill='tozeroy', mode='none' , fillcolor='green')
            if name=="Verkaufspreis":
                x1   = [xc   for xc in fig.data[0].x if xc <kaufpreis]
                y1   = fig.data[0].y[:len(x1)]            
                fig.add_scatter(x=x1, y=y1,fill='tozeroy', mode='none' , 
                                fillcolor="red", name=name)

            if ((name=="Objektrendite") or 
                (name=="Eigenkapitalrendite") or
                (name=="Gewinn")):
                x1   = [xc   for xc in fig.data[0].x if xc <0]
                y1   = fig.data[0].y[:len(x1)]            
                fig.add_scatter(x=x1, y=y1,fill='tozeroy', mode='none' , 
                                fillcolor="red", name=name)
                
            if name=="Minimaler Cashflow":
                xl = np.quantile(eingabeparameter, q=0.05)
                x1   = [xc   for xc in fig.data[0].x if xc <xl]
                y1   = fig.data[0].y[:len(x1)]
                fig.add_scatter(x=x1, y=y1,fill='tozeroy', mode='none' , 
                                fillcolor='red', name=name)
                
        return fig

    fig_verkaufsfaktor = figure_ein_aus_gabeparameter(
        eingabeparameter="verkaufsfaktor",
        name="Verkaufsfaktor",
        zeichen="",
        x=1,
        runden=1,
        area="middle"
    )

    fig_anschlusszinssatz = figure_ein_aus_gabeparameter(
        eingabeparameter="anschlusszinssatz",
        name="Anschlusszinssatz",
        zeichen="%",
        x=100,
        runden=2,
        area="middle"
    )

    fig_mietsteigerung = figure_ein_aus_gabeparameter(
        eingabeparameter="mietsteigerung",
        name="Mietsteigerung pro Jahr",
        zeichen="%",
        x=100,
        runden=2,
        area="middle"
    )

    fig_kostensteigerung = figure_ein_aus_gabeparameter(
        eingabeparameter="kostensteigerung",
        name="Kostensteigerung pro Jahr",
        zeichen="%",
        x=100,
        runden=2,
        area="middle"
    )

    fig_mietausfall = figure_ein_aus_gabeparameter(
        eingabeparameter="mietausfall",
        name="Mietausfall pro Jahr",
        zeichen="%",
        x=100,
        runden=2,
        area="middle"
    )

    fig_verkaufspreis = figure_ein_aus_gabeparameter(
        eingabeparameter="verkaufspreis",
        name="Verkaufspreis",
        zeichen="€",
        x=1,
        runden=0,
        area="nothing"
    )

    fig_objektrendite = figure_ein_aus_gabeparameter(
        eingabeparameter="objektrendite",
        name="Objektrendite",
        zeichen="%",
        x=100,
        runden=2,
        area="nothing"
    )
    
    fig_eigenkapitalrendite = figure_ein_aus_gabeparameter(
        eingabeparameter="eigenkapitalrendite",
        name="Eigenkapitalrendite",
        zeichen="%",
        x=100,
        runden=2,
        area="nothing"
    )

    fig_gewinn = figure_ein_aus_gabeparameter(
        eingabeparameter="gewinn", name="Gewinn", zeichen="€", x=1, runden=0,
        area="nothing"
    )

    fig_minimaler_cashflow = figure_ein_aus_gabeparameter(
        eingabeparameter="minimaler_cashflow",
        name="Minimaler Cashflow",
        zeichen="€",
        x=1,
        runden=0,
        area="nothing"
    )

    def figure_etf_vergleich(
        eingabeparameter1, 
        eingabeparameter2, 
        name1,
        name2,
        zeichen, x, runden, ueberschrift):
        
        eingabeparameter1 = np.array(ergebnis[eingabeparameter1])
        eingabeparameter1 = eingabeparameter1[~np.isnan(eingabeparameter1)]
        
        eingabeparameter2 = np.array(ergebnis[eingabeparameter2])
        eingabeparameter2 = eingabeparameter2[~np.isnan(eingabeparameter2)]
        
        fig = ff.create_distplot([eingabeparameter1, eingabeparameter2], [name1, name2], 
                         show_hist=False, show_rug=False)

        if runden==0:
            annotation_tmp = f"Median: {int(np.quantile(eingabeparameter1, q=0.5)*x)} {zeichen}"
        else:
            annotation_tmp = f"Median: {round(np.quantile(eingabeparameter1, q=0.5)*x,runden)} {zeichen}"            
        fig = fig.add_vline(
                            x=np.quantile(eingabeparameter1, q=0.5),
                            line_width=3,
                            line_dash="dash",
                            line_color="cornflowerblue",
                            annotation_text=annotation_tmp,
                            annotation_position="top left",
                            annotation_font_size=12,
                            annotation_font_color="black",
                            annotation_bgcolor="white",
                        )

        if runden==0:
            annotation_tmp = f"Median: {int(np.quantile(eingabeparameter2, q=0.5)*x)} {zeichen}"
        else:
            annotation_tmp = f"Median: {round(np.quantile(eingabeparameter2, q=0.5)*x,runden)} {zeichen}"
        fig = fig.add_vline(
                            x=np.quantile(eingabeparameter2, q=0.5),
                            line_width=3,
                            line_dash="dash",
                            line_color="orange",
                            annotation_text=annotation_tmp,
                            annotation_position="bottom right",
                            annotation_font_size=12,
                            annotation_font_color="black",
                            annotation_bgcolor="white",
                        )
                
        
        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(plot_bgcolor="white")
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
        fig.update_layout(title=ueberschrift)
        
        return fig
        
    fig_etf_rendite = figure_etf_vergleich(
        eingabeparameter1="eigenkapitalrendite",
        eingabeparameter2="etf_ek_rendite",
        name1="Immobilie",
        name2=name2,
        zeichen="%",
        x=100,
        runden=2,
        ueberschrift="Eigenkapitalrendite"
    )
    
    fig_etf_gewinn = figure_etf_vergleich(
        eingabeparameter1="gewinn",
        eingabeparameter2="etf_gewinn",
        name1="Immobilie",
        name2=name2,
        zeichen="€",
        x=1,
        runden=0,
        ueberschrift="Gewinn"
    )
        
    loading_antwort = ""
    
   
    
    # Generate text output
    text_dynamisch = text_generator(
        ergebnis,
        zinsbindung,
        anlagehorizont,
        erste_mieterhoehung,
        kaufpreis,
        )

    return (
#        text["einleitung"],
        text_dynamisch["etf_rendite"],
        text_dynamisch["etf_gewinn"],
        text_dynamisch["anschlusszinssatz"],
        text_dynamisch["verkaufsfaktor"],
        text_dynamisch["mietsteigerung"],
        text_dynamisch["kostensteigerung"],
        text_dynamisch["mietausfall"],
        #text_dynamisch["ergebnisse"],
        text_dynamisch["verkaufspreis"],
        text_dynamisch["objektrendite"],
        text_dynamisch["eigenkapitalrendite"],
        text_dynamisch["gewinn"],
        text_dynamisch["minimaler_cashflow"],
        loading_antwort,
        fig_verkaufsfaktor,
        fig_anschlusszinssatz,
        fig_mietsteigerung,
        fig_kostensteigerung,
        fig_mietausfall,
        fig_verkaufspreis,
        fig_objektrendite,
        fig_eigenkapitalrendite,
        fig_gewinn,
        fig_minimaler_cashflow,
        fig_etf_rendite,
        fig_etf_gewinn,
    )
    
#
# CSV/Excel Import
#

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
# Assume that the user uploaded a CSV file
        df = pd.read_csv(
        io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
# Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded)) 
    else:
        df = "**Keine csv oder xlsx Datei**"
    return df

# Upload component: The same file can NOT be uploaded twice in a row. It will not
# get recognized. This is something we need to live with right now. In the future we 
# could checkout:
# https://community.plotly.com/t/reuploading-same-file/42178
# https://community.plotly.com/t/can-i-upload-the-same-file-twice-in-a-row/40526/3
@app.callback(Output('upload-status', 'children'),
                Output("kaufpreis", "value"),
                Output("kaufpreis_grundstueck", "value"),
                Output("kaufpreis_sanierung", "value"),
                Output("kaufnebenkosten", "value"),
                Output("renovierungskosten", "value"),
                Output("mieteinnahmen", "value"),
                Output("mietsteigerung", "value"),
                Output("unsicherheit_mietsteigerung", "value"),
                Output("erste_mieterhoehung", "value"),
                Output("instandhaltungskosten", "value"),
                Output("verwaltungskosten", "value"),
                Output("mietausfall", "value"),
                Output("unsicherheit_mietausfall", "value"),
                Output("kostensteigerung", "value"),
                Output("unsicherheit_kostensteigerung", "value"),
                Output("eigenkapital", "value"),
                Output("zinsbindung", "value"),
                Output("disagio", "value"),
                Output("zinsatz", "value"),
                Output("tilgungssatz", "value"),
                Output("anschlusszinssatz", "value"),
                Output("unsicherheit_anschlusszinssatz", "value"),
                Output("familienstand", "value"),
                Output("einkommen", "value"),
                Output("baujahr", "value"),
                #    Input("sonderabschreibung", "value"),
                Output("anlagehorizont", "value"),
                Output("verkaufsfaktor", "value"),
                Output("unsicherheit_verkaufsfaktor", "value"),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    default_input = [
        300_000, 100_000, 0, 40_000, 1_000, 12_000, 2, 1, 5, 1_200, 600, 2, 2, 1.5,
        2, 100_000, 20, 0, 1.5, 2.5, 4, 1.5, "0", 100_000, "0", 15, 22, 4
    ]   
    default_column = [
        'Kaufpreis', 'davon Grundstücksanteil', 'davon Sanierungskosten', 
        'Kaufnebenkosten', 'Renovierungskosten', 'Mieteinahmen', 'Mietsteigerung', 
        'Unsicherheit Mietsteigerung', 'Erste Mieterhöhung ab Jahr', 'Instandhaltungskosten Jahr', 
        'Verwaltungskosten Jahr', 'Pauschale für Mietausfall', 'Unsicherheit Mietausfall', 
        'Geschätzte Kostensteigerung', 'Unsicherheit Kostensteigerung', 'Eigenkapital', 
        'Zinsbindung', 'Disagio', 'Zinssatz', 'Tilgungssatz', 'Anschlusszinssatz', 
        'Unsicherheit Anschlusszinssatz', 'Familienstand', 'Zu versteuerndes Einkommen', 
        'Baujahr', 'Anlagehorizont', 'Geschätzter Verkaufsfaktor', 'Unsicherheit Verkaufsfaktor'
    ] 
    text_message = ""
    if list_of_contents is not None:
        df = parse_contents(list_of_contents[-1], list_of_names[-1], list_of_dates[-1])        
        if isinstance(df, pd.DataFrame): 
            if "Unnamed: 0" in list(df.columns):                
                df.drop(["Unnamed: 0"], axis=1, inplace=True)
            imported_input = (
                str(df[i][0]) 
                if i in ["Familienstand", "Baujahr"] 
                else df[i][0] 
                for i in list(df.columns)
            )
            #print(list(df.columns))
            if list(df.columns)==default_column:
                return "**Upload erfolgreich**", *imported_input 
            if list(df.columns)!=default_column:
                return "**Falsches Format**", *default_input
        else:
            text_message = df
            return text_message, *default_input
    else:
        return text_message, *default_input

#
# CSV Export
#

@app.callback(Output('download', 'data'),
             [Input('download-results-button', 'n_clicks')],
             state=[
            State("kaufpreis", "value"),
            State("kaufpreis_grundstueck", "value"),
            State("kaufpreis_sanierung", "value"),
            State("kaufnebenkosten", "value"),
            State("renovierungskosten", "value"),
            State("mieteinnahmen", "value"),
            State("mietsteigerung", "value"),
            State("unsicherheit_mietsteigerung", "value"),
            State("erste_mieterhoehung", "value"),
            State("instandhaltungskosten", "value"),
            State("verwaltungskosten", "value"),
            State("mietausfall", "value"),
            State("unsicherheit_mietausfall", "value"),
            State("kostensteigerung", "value"),
            State("unsicherheit_kostensteigerung", "value"),
            State("eigenkapital", "value"),
            State("zinsbindung", "value"),
            State("disagio", "value"),
            State("zinsatz", "value"),
            State("tilgungssatz", "value"),
            State("anschlusszinssatz", "value"),
            State("unsicherheit_anschlusszinssatz", "value"),
            State("familienstand", "value"),
            State("einkommen", "value"),
            State("baujahr", "value"),
            #    Input("sonderabschreibung", "value"),
            State("anlagehorizont", "value"),
            State("verkaufsfaktor", "value"),
            State("unsicherheit_verkaufsfaktor", "value"),
            ],
            )
def download_data(n_clicks, 
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
):
    #print(n_clicks)
    if n_clicks != None:
        df = pd.DataFrame({"Kaufpreis": [kaufpreis], 
                           "davon Grundstücksanteil": [kaufpreis_grundstueck],
                            "davon Sanierungskosten":[kaufpreis_sanierung],
                "Kaufnebenkosten":[kaufnebenkosten],
                "Renovierungskosten":[renovierungskosten],
                "Mieteinahmen":[mieteinnahmen],
                "Mietsteigerung":[mietsteigerung],
                'Unsicherheit Mietsteigerung':[unsicherheit_mietsteigerung],
                'Erste Mieterhöhung ab Jahr':[erste_mieterhoehung],
                'Instandhaltungskosten Jahr':[instandhaltungskosten],
                'Verwaltungskosten Jahr':[verwaltungskosten],
                'Pauschale für Mietausfall':[mietausfall],
                'Unsicherheit Mietausfall':[unsicherheit_mietausfall],
                'Geschätzte Kostensteigerung':[kostensteigerung],
                'Unsicherheit Kostensteigerung':[unsicherheit_kostensteigerung],
                'Eigenkapital':[eigenkapital],
                'Zinsbindung':[zinsbindung],
                'Disagio':[disagio],
                'Zinssatz':[zinsatz],
                'Tilgungssatz':[tilgungssatz],
                'Anschlusszinssatz':[anschlusszinssatz],
                'Unsicherheit Anschlusszinssatz':[unsicherheit_anschlusszinssatz],
                'Familienstand':[familienstand],
                'Zu versteuerndes Einkommen':[einkommen],
                'Baujahr':[baujahr],
                #    sonderabschreibung,
                'Anlagehorizont':[anlagehorizont],
                'Geschätzter Verkaufsfaktor':[verkaufsfaktor],
                'Unsicherheit Verkaufsfaktor':[unsicherheit_verkaufsfaktor],
                           },
                          index=["Daten"]
        )
        #print(df)
        return send_data_frame(df.to_csv, filename='data.csv')


if __name__ == "__main__":
    app.run_server(debug=True)
