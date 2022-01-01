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

import base64
import io
import xlrd

from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import openpyxl

#from formeln import renditerechner
from text import text_generator, text_static
from simulation_mieten_vs_kaufen import mieten_kaufen

from app import app

#VALID_USERNAME_PASSWORD_PAIRS = {
#                                "Immobilien":"Simulator",
#                                "Christoph": "Groener",
#                                 "Jack":"Singer"}

# Initialize the app
# app = dash.Dash(__name__)
# server = app.server
#auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
# app.config.suppress_callback_exceptions = True

#
# Statische Texte
#

text_statisch = text_static()


#app.layout = html.Div(
layout = html.Div(
    [
           # row
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
                    children=[html.H4("1. Allgemein"),],
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
                html.Div(
            children=[
                # first column of first row
                html.Div(
                    children=[
                        html.Label("Vergleichszeitraum"),
                        dcc.Input(
                            id="anlagehorizont_mk",
                            placeholder="Eingabe...",
                            value=15,
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
                        html.Label("Eigenkapital"),
                        dcc.Input(
                            id="eigenkapital_mk",
                            placeholder="Eingabe...",
                            value=10_000,
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
        # row zero
        html.Div(
            children=[
                # first column of row zero
                html.Div(
                    children=[html.H4("2. Kennzahlen Immobilie"),],
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
                            id="kaufpreis_mk",
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
                            id="renovierungskosten_mk",
                            placeholder="Eingabe...",
                            value=10_000,
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
                            id="kaufnebenkosten_mk",
                            placeholder="Eingabe...",
                            value=30000,
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
                            id="instandhaltungskosten_mk",
                            placeholder="Eingabe...",
                            value=2_000,
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
                        html.Label("Steigerung Instandhaltungsk. (%)",
                                   #title="Kosten die im Jahr des Kaufs anfallen und steuerlich Absetzbar sind (Sanierungskosten dürfen 15% der Gebäudekosten nicht überschreiten)."
                                   ),
                        dcc.Input(
                            id="kostensteigerung_mk",
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
                            id="unsicherheit_kostensteigerung_mk",
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
                            id="wertsteigerung_mk",
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
                            id="unsicherheit_wertsteigerung_mk",
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
                    children=[html.H4("3. Finanzierung Immobilie"),],
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
                # second column
                html.Div(
                    children=[
                        html.Label("Zinsbindung (Jahre)"),
                        dcc.Input(
                            id="zinsbindung_mk",
                            placeholder="Eingabe...",
                            type="number",
                            value=15,
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
                            id="zinssatz_mk",
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
                # second column
                html.Div(
                    children=[
                        html.Label("Tilgungssatz (%)"),
                        dcc.Input(
                            id="tilgungssatz_mk",
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

            ],
            className="row",
        ),
        # row ten
        html.Div(
            children=[



                # third column
                html.Div(
                    children=[
                        html.Label("Anschlusszinssatz (%)",
                                   title="Erwartungswert"),
                        dcc.Input(
                            id="anschlusszinssatz_mk",
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
                            id="unsicherheit_anschlusszinssatz_mk",
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
        # third row
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("4. Wohnen zur Miete"),],
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
                            id="nettokaltmiete_mk",
                            placeholder="Eingabe...",
                            value=6_500,
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
                            id="steigerung_nettokaltmiete_mk",
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
                            id="unsicherheit_steigerung_nettokaltmiete_mk",
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
                    children=[html.H4("5. Steuern"),],
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
                            id="familienstand_mk",
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
                        html.Label("Kapitalertragssteuer (%)"),
                        dcc.Input(
                            id="kapitalertragssteuer_mk",
                            placeholder="Eingabe...",
                            type="number",
                            value=26.375,
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
                    children=[html.H4("6. Rendite Alternativanlagen"),],
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
                # second column
                html.Div(
                    children=[
                        html.Label("Zinssatz fest verzinste Anlage (%)"),
                                 #  title="Kaufpreis-Miet-Verhältnis (Erwartungswert)"),
                        dcc.Input(
                            id="verzinsung_ek_mk",
                            placeholder="Eingabe...",
                            type="number",
                            value=2.2,
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
                        html.Label("Unsicherheit Zinsatz (%)",
                                   title="Standardabweichung"),
                        dcc.Input(
                            id="unsicherheit_verzinsung_ek_mk",
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
        # row fourteen
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.Label("ETF Vergleich"),
                        dcc.RadioItems(
                            id="etf_vergleich_mk",
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
                    children=[html.H4("7. Import/Export der Eingabeparameter"),
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
                html.Button("Eingabe exportieren", id='download-results-button_mk'),
                Download(id='download_mk'),                
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
        id='upload-data_mk',
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
           dcc.Markdown(id='upload-status_mk')
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
                    children=[html.H4("8. Simulation"),
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
                            id="sim_runs_mk",
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
                    children=[html.Button("Start der Simulation", id="button_mk"),
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
            children=html.Div(id="loading-output-1_mk")
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
                            # dcc.Store inside the app that stores the intermediate value
                        dcc.Store(id='intermediate-value-investiert_mk'),
                        dcc.Store(id='intermediate-value-nicht-investiert_mk'),
                        html.H4(
                            "Verteilung der mit Unsicherheit behafteten Eingabeparameter"
                        ),
                        dcc.Markdown(text_statisch["eingabeparameter"]),
                        dcc.Markdown(text_statisch["ergebnisse"]),
                        html.H4("Ergebnisse der Simulation"),
                        html.H6("Vermögensentwicklung: Cashflows werden investiert "),
                        #dcc.Markdown(id='gewinn_text'),
                        dcc.Dropdown(
                        options=[
                            #{'label': 'Immobilie', 'value': 'immo'},
                            {'label': 'Immobilie + ETF', 'value': 'Immobilie + ETF'},
                            {'label': 'Immobilie + ETF (versteuert)', 'value': 'Immobilie + ETF (versteuert)'},
                            {'label': 'Immobilie + Festgeld', 'value': 'Immobilie + Festgeld'},
                            {'label': 'Immobilie + Festgeld (versteuert)', 'value': 'Immobilie + Festgeld (versteuert)'},
                            {'label': 'ETF', 'value': 'ETF'},
                            {'label': 'ETF (versteuert)', 'value': 'ETF (versteuert)'},
                            {'label': 'Festgeld', 'value': 'Festgeld'},
                            {'label': 'Festgeld (versteuert)', 'value': 'Festgeld (versteuert)'},
                        ],
                        value=['Immobilie + ETF (versteuert)', 'ETF (versteuert)'],
                        multi=True,
                        id="grafik_selector_investiert_mk"),  
                        dcc.Graph(id="mieten_vs_kaufen_investiert_mk"),  
                        html.H6("Vermögensentwicklung: Cashflows werden nicht investiert "),
                        dcc.Dropdown(
                        options=[
                            {'label': 'Immobilie', 'value': 'Immobilie'},
                            {'label': 'ETF', 'value': 'ETF'},
                            {'label': 'ETF (versteuert)', 'value': 'ETF (versteuert)'},
                            {'label': 'Festgeld', 'value': 'Festgeld'},
                            {'label': 'Festgeld (versteuert)', 'value': 'Festgeld (versteuert)'},
                        ],
                        value=['Immobilie', 'ETF (versteuert)'],
                        multi=True,
                        id="grafik_selector_nicht_investiert_mk"),  
                        dcc.Graph(id="mieten_vs_kaufen_nicht_investiert_mk"),                                                
                        html.H4("9. Disclaimer"),
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
  #  Output('mieten_vs_kaufen', 'figure'),
    Output('intermediate-value-investiert_mk', 'data'),
    Output('intermediate-value-nicht-investiert_mk', 'data'),
    [Input("button_mk", "n_clicks")],
    state=[
        
        State("sim_runs_mk", "value"),
        State("anlagehorizont_mk", "value"),
        State("eigenkapital_mk", "value"),
        
        State("kaufpreis_mk", "value"),
        State("renovierungskosten_mk", "value"),
        State("kaufnebenkosten_mk", "value"),
        State("instandhaltungskosten_mk", "value"),
        State("kostensteigerung_mk", "value"),
        State("unsicherheit_kostensteigerung_mk", "value"),
        State("wertsteigerung_mk", "value"),
        State("unsicherheit_wertsteigerung_mk", "value"),
        
        State("zinsbindung_mk", "value"),
        State("zinssatz_mk", "value"),
        State("tilgungssatz_mk", "value"),
        State("anschlusszinssatz_mk", "value"),
        State("unsicherheit_anschlusszinssatz_mk", "value"),
        
        State("nettokaltmiete_mk", "value"),
        State("steigerung_nettokaltmiete_mk", "value"),
        State("unsicherheit_steigerung_nettokaltmiete_mk", "value"),
        
        State("familienstand_mk", "value"),
        State("kapitalertragssteuer_mk", "value"),
      
        
        State("verzinsung_ek_mk", "value"),
        State("unsicherheit_verzinsung_ek_mk", "value"),
        State("etf_vergleich_mk", "value"),
    ],
)
def custom_figure(
    button,
    
    sim_runs,
   anlagehorizont,
   eigenkapital,
    
   kaufpreis,
   renovierungskosten,
   kaufnebenkosten,
   instandhaltungskosten,
   kostensteigerung,
   unsicherheit_kostensteigerung,
   wertsteigerung,
   unsicherheit_wertsteigerung,
   
   
   zinsbindung,
   zinssatz,
   tilgungssatz,
   anschlusszinssatz,
   unsicherheit_anschlusszinssatz,
   
   nettokaltmiete,
   steigerung_nettokaltmiete,
   unsicherheit_steigerung_nettokaltmiete,
   
   familienstand,
   kapitalertragssteuer,
   
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
        
   # print(anlagehorizont)

    ergebnis = mieten_kaufen(
        sim_runs=sim_runs, 
        
        anlagehorizont=anlagehorizont,
        eigenkapital=eigenkapital,

        kaufpreis=kaufpreis,
        renovierungskosten=renovierungskosten,
        kaufnebenkosten=kaufnebenkosten,
        instandhaltungskosten=instandhaltungskosten,
        kostensteigerung=kostensteigerung/100,
        unsicherheit_kostensteigerung=unsicherheit_kostensteigerung/100,
        wertsteigerung=wertsteigerung/100,
        unsicherheit_wertsteigerung=unsicherheit_wertsteigerung/100,
        
        zinsbindung=zinsbindung,
        zinsatz=zinssatz/100,
        tilgungssatz=tilgungssatz/100,
        anschlusszinssatz=anschlusszinssatz/100,
        unsicherheit_anschlusszinssatz=unsicherheit_anschlusszinssatz/100,

        nettokaltmiete=nettokaltmiete,
        steigerung_nettokaltmiete=steigerung_nettokaltmiete/100,
        unsicherheit_steigerung_nettokaltmiete=unsicherheit_steigerung_nettokaltmiete/100,

        alleinstehend=alleinstehend,
        kapitalertragssteuer=kapitalertragssteuer/100,
        
        etf_rendite = etf_rendite,
        unsicherheit_etf_rendite=unsicherheit_etf_rendite,
        fest_verzinst=verzinsung_ek/100,
        unsicherheit_fest_verzinst=unsicherheit_verzinsung_ek/100,
    )

    #print("Hello world")
    #print(ergebnis["etf_vermoegen_initial_versteuert_pj"])
    
    # Aufbereitung der Ergebnisse
    ergebnisse_aufbereitet_investiert = {
        "jahr_pj":ergebnis["jahr_pj"],
        
        "Immobilie + ETF":np.median(np.array(ergebnis["vermoegen_immo_pj"]), axis=0)+np.median(np.array(ergebnis["etf_vermoegen_immo_pj"]), axis=0),
        "Immobilie + ETF + lower bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.1, axis=0) + np.quantile(np.array(ergebnis["etf_vermoegen_immo_pj"]), q=0.10, axis=0),
        "Immobilie + ETF + upper bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.90, axis=0) + np.quantile(np.array(ergebnis["etf_vermoegen_immo_pj"]), q=0.90, axis=0),
        
        "Immobilie + ETF (versteuert)":np.median(np.array(ergebnis["vermoegen_immo_pj"]), axis=0) + np.median(np.array(ergebnis["etf_vermoegen_immo_versteuert_pj"]),axis=0),
        "Immobilie + ETF (versteuert) + lower bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.1, axis=0) + np.quantile(np.array(ergebnis["etf_vermoegen_immo_versteuert_pj"]), q=0.1, axis=0),
        "Immobilie + ETF (versteuert) + upper bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.90, axis=0) + np.quantile(np.array(ergebnis["etf_vermoegen_immo_versteuert_pj"]), q=0.90, axis=0),
        
        "Immobilie + Festgeld":np.median(np.array(ergebnis["vermoegen_immo_pj"]), axis=0) + np.median(np.array(ergebnis["festgeld_vermoegen_immo_pj"]), axis=0),
        "Immobilie + Festgeld + lower bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.1, axis=0) + np.quantile(np.array(ergebnis["festgeld_vermoegen_immo_pj"]), q=0.1, axis=0),
        "Immobilie + Festgeld + upper bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.9, axis=0) + np.quantile(np.array(ergebnis["festgeld_vermoegen_immo_pj"]), q=0.90, axis=0),
        
        "Immobilie + Festgeld (versteuert)":np.median(np.array(ergebnis["vermoegen_immo_pj"]), axis=0) + np.median(np.array(ergebnis["festgeld_vermoegen_immo_versteuert_pj"]), axis=0),
        "Immobilie + Festgeld (versteuert) + lower bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.1, axis=0) + np.quantile(np.array(ergebnis["festgeld_vermoegen_immo_versteuert_pj"]), q=0.1, axis=0),
        "Immobilie + Festgeld (versteuert) + upper bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.9, axis=0) + np.quantile(np.array(ergebnis["festgeld_vermoegen_immo_versteuert_pj"]), q=0.90, axis=0),        
        
        "ETF": np.median(np.array(ergebnis["etf_vermoegen_pj"]), axis=0),
        "ETF + lower bound": np.quantile(np.array(ergebnis["etf_vermoegen_pj"]), q=0.1, axis=0),
        "ETF + upper bound": np.quantile(np.array(ergebnis["etf_vermoegen_pj"]), q=0.9, axis=0),
        
        "ETF (versteuert)": np.median(ergebnis["etf_vermoegen_versteuert_pj"], axis=0),
        "ETF (versteuert) + lower bound": np.quantile(np.array(ergebnis["etf_vermoegen_versteuert_pj"]), q=0.1, axis=0),
        "ETF (versteuert) + upper bound": np.quantile(np.array(ergebnis["etf_vermoegen_versteuert_pj"]), q=0.90, axis=0),
        
        "Festgeld": np.median(ergebnis["festgeld_vermoegen_pj"], axis=0),
        "Festgeld + lower bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_pj"]), q=0.1, axis=0),
        "Festgeld + upper bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_pj"]), q=0.9, axis=0),
        
        "Festgeld (versteuert)": np.median(ergebnis["festgeld_vermoegen_versteuert_pj"], axis=0),
        "Festgeld (versteuert) + lower bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_versteuert_pj"]), q=0.1, axis=0),
        "Festgeld (versteuert) + upper bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_versteuert_pj"]), q=0.9, axis=0),
        
    }
    
    
    ergebnisse_aufbereitet_nicht_investiert = {
        "jahr_pj":ergebnis["jahr_pj"],
        #"Immobilie":ergebnis["vermoegen_immo_pj"],
        
        "Immobilie":np.median(np.array(ergebnis["vermoegen_immo_pj"]), axis=0),
        "Immobilie + lower bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.1, axis=0), 
        "Immobilie + upper bound":np.quantile(np.array(ergebnis["vermoegen_immo_pj"]), q=0.90, axis=0), 

        
        #"ETF":ergebnis["etf_vermoegen_initial_pj"],
        "ETF": np.median(np.array(ergebnis["etf_vermoegen_initial_pj"]), axis=0),
        "ETF + lower bound": np.quantile(np.array(ergebnis["etf_vermoegen_initial_pj"]), q=0.1, axis=0),
        "ETF + upper bound": np.quantile(np.array(ergebnis["etf_vermoegen_initial_pj"]), q=0.9, axis=0),

        
        #"ETF (versteuert)":ergebnis["etf_vermoegen_initial_versteuert_pj"],
        "ETF (versteuert)": np.median(np.array(ergebnis["etf_vermoegen_initial_versteuert_pj"]), axis=0),
        "ETF (versteuert) + lower bound": np.quantile(np.array(ergebnis["etf_vermoegen_initial_versteuert_pj"]), q=0.1, axis=0),
        "ETF (versteuert) + upper bound": np.quantile(np.array(ergebnis["etf_vermoegen_initial_versteuert_pj"]), q=0.9, axis=0),

        #"Festgeld":ergebnis["festgeld_vermoegen_initial_pj"],
        "Festgeld": np.median(np.array(ergebnis["festgeld_vermoegen_initial_pj"]), axis=0),
        "Festgeld + lower bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_initial_pj"]), q=0.1, axis=0),
        "Festgeld + upper bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_initial_pj"]), q=0.9, axis=0),
        
        #"Festgeld (versteuert)":ergebnis["festgeld_vermoegen_initial_versteuert_pj"],
        "Festgeld (versteuert)": np.median(np.array(ergebnis["festgeld_vermoegen_initial_versteuert_pj"]), axis=0),
        "Festgeld (versteuert) + lower bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_initial_versteuert_pj"]), q=0.1, axis=0),
        "Festgeld (versteuert) + upper bound": np.quantile(np.array(ergebnis["festgeld_vermoegen_initial_versteuert_pj"]), q=0.9, axis=0),
    }
    
    return (
        ergebnisse_aufbereitet_investiert,
        ergebnisse_aufbereitet_nicht_investiert
    )
    
@app.callback(
              Output('mieten_vs_kaufen_investiert_mk', 'figure'),
              Output('mieten_vs_kaufen_nicht_investiert_mk', 'figure'),
              Input('intermediate-value-investiert_mk', 'data'),
              Input('intermediate-value-nicht-investiert_mk', 'data'),
              Input('grafik_selector_investiert_mk', "value"),
              Input('grafik_selector_nicht_investiert_mk', "value"),
               )
def update_graph(ergebnisse_investiert, ergebnisse_nicht_investiert, grafik_selector_investiert,
                 grafik_selector_nicht_investiert):
    
    farben = ['#636EFA',
                '#EF553B',
                '#00CC96',
                '#AB63FA',
                '#FFA15A',
                '#19D3F3',
                '#FF6692',
                '#B6E880',
                '#FF97FF',
                '#FECB52']
    
    farben_rgb = ["rgba(99, 110, 250, 0.3)",
                  "rgba(239, 85, 59, 0.3)",
                  "rgba(0, 204, 150, 0.3)",
                  "rgba(171, 99, 250, 0.3)",
                  "rgba(255, 161, 90, 0.3)",
                  "rgba(25, 211, 243, 0.3)",
                  "rgba(255, 102, 146, 0.3)",
                  "rgba(182, 232, 128, 0.3)",
                  "rgba(255, 151, 255, 0.3)",
                  "rgba(254, 203, 82, 0.3)"
                  ]
    
    fig_vermoegen_investiert = go.Figure()
    for i, wahl in enumerate(grafik_selector_investiert):
        #print(wahl)
        #print(i)
        #print(wahl + " lower bound")
        # print(len(ergebnisse_investiert[wahl]))
        # print(len(ergebnisse_investiert["jahr_pj"]))
        fig_vermoegen_investiert.add_trace(go.Scatter(x=ergebnisse_investiert["jahr_pj"], y=ergebnisse_investiert[wahl],
                    mode='lines+markers',
                    line_color = farben[i],
                    name=wahl))
        
        
        fig_vermoegen_investiert.add_scatter(
        name='Upper Bound',
        x=ergebnisse_investiert["jahr_pj"],
        y=np.array(ergebnisse_investiert[wahl + " + lower bound"]),
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False
        ),
        fig_vermoegen_investiert.add_scatter(
        name='Lower Bound',
        x=ergebnisse_investiert["jahr_pj"],
        y=np.array(ergebnisse_investiert[wahl + " + upper bound"]),
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor=farben_rgb[i],
        fill='tonexty',
        opacity=0.5,
        showlegend=False
    )        

    fig_vermoegen_investiert.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01,
))
    fig_vermoegen_investiert.update_layout(plot_bgcolor="white")
    fig_vermoegen_investiert.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig_vermoegen_investiert.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    
    fig_vermoegen_nicht_investiert = go.Figure()
    for i, wahl in enumerate(grafik_selector_nicht_investiert):
        #print(ergebnisse_nicht_investiert["jahr_pj"])
        #print(ergebnisse_nicht_investiert[wahl2])
        fig_vermoegen_nicht_investiert.add_trace(go.Scatter(x=ergebnisse_nicht_investiert["jahr_pj"], y=ergebnisse_nicht_investiert[wahl],
                    mode='lines+markers',
                    line_color = farben[i],
                    name=wahl))
        
        

        fig_vermoegen_nicht_investiert.add_scatter(
        name='Upper Bound',
        x=ergebnisse_nicht_investiert["jahr_pj"],
        y=np.array(ergebnisse_nicht_investiert[wahl + " + lower bound"]),
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False
        ),
        fig_vermoegen_nicht_investiert.add_scatter(
        name='Lower Bound',
        x=ergebnisse_nicht_investiert["jahr_pj"],
        y=np.array(ergebnisse_nicht_investiert[wahl + " + upper bound"]),
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor=farben_rgb[i],
        fill='tonexty',
        opacity=0.5,
        showlegend=False
    )        


    fig_vermoegen_nicht_investiert.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
    ))    
    
    fig_vermoegen_nicht_investiert.update_layout(plot_bgcolor="white")
    fig_vermoegen_nicht_investiert.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig_vermoegen_nicht_investiert.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    
    return (fig_vermoegen_investiert, fig_vermoegen_nicht_investiert)
    
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
@app.callback(Output('upload-status_mk', 'children'),
              
              
        Output("anlagehorizont_mk", "value"),
        Output("eigenkapital_mk", "value"),
        
        Output("kaufpreis_mk", "value"),
        Output("renovierungskosten_mk", "value"),
        Output("kaufnebenkosten_mk", "value"),
        Output("instandhaltungskosten_mk", "value"),
        Output("kostensteigerung_mk", "value"),
        Output("unsicherheit_kostensteigerung_mk", "value"),
        Output("wertsteigerung_mk", "value"),
        Output("unsicherheit_wertsteigerung_mk", "value"),
        
        Output("zinsbindung_mk", "value"),
        Output("zinssatz_mk", "value"),
        Output("tilgungssatz_mk", "value"),
        Output("anschlusszinssatz_mk", "value"),
        Output("unsicherheit_anschlusszinssatz_mk", "value"),
        
        Output("nettokaltmiete_mk", "value"),
        Output("steigerung_nettokaltmiete_mk", "value"),
        Output("unsicherheit_steigerung_nettokaltmiete_mk", "value"),
        
        Output("familienstand_mk", "value"),
        Output("kapitalertragssteuer_mk", "value"),
      
        
        Output("verzinsung_ek_mk", "value"),
        Output("unsicherheit_verzinsung_ek_mk", "value"),
        Output("etf_vergleich_mk", "value"),
              [Input('upload-data_mk', 'contents')],
              [State('upload-data_mk', 'filename'),
               State('upload-data_mk', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    default_input = [
        15, 100_00, 300_000, 1_000, 30_000, 2_000, 1.5, 1.5, 1.5, 1.5, 15, 1.5, 2.5, 4,
        1.5, 6500, 2, 1, "0", 26.375, 2.2, 1, "0"
    ]   
    default_column = [
   "anlagehorizont",
   "eigenkapital",
    
   "kaufpreis",
   "renovierungskosten",
   "kaufnebenkosten",
   "instandhaltungskosten",
   "kostensteigerung",
   "unsicherheit_kostensteigerung",
   "wertsteigerung",
   "unsicherheit_wertsteigerung",
   
   
   "zinsbindung",
   "zinssatz",
   "tilgungssatz",
   "anschlusszinssatz",
   "unsicherheit_anschlusszinssatz",
   
   "nettokaltmiete",
   "steigerung_nettokaltmiete",
   "unsicherheit_steigerung_nettokaltmiete",
   
   "familienstand",
   "kapitalertragssteuer",
   
   "verzinsung_ek",
   "unsicherheit_verzinsung_ek",
   "etf_vergleich",
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

@app.callback(Output('download_mk', 'data'),
             [Input('download-results-button_mk', 'n_clicks')],
             state=[
                State("anlagehorizont_mk", "value"),
                State("eigenkapital_mk", "value"),
                
                State("kaufpreis_mk", "value"),
                State("renovierungskosten_mk", "value"),
                State("kaufnebenkosten_mk", "value"),
                State("instandhaltungskosten_mk", "value"),
                State("kostensteigerung_mk", "value"),
                State("unsicherheit_kostensteigerung_mk", "value"),
                State("wertsteigerung_mk", "value"),
                State("unsicherheit_wertsteigerung_mk", "value"),
                
                State("zinsbindung_mk", "value"),
                State("zinssatz_mk", "value"),
                State("tilgungssatz_mk", "value"),
                State("anschlusszinssatz_mk", "value"),
                State("unsicherheit_anschlusszinssatz_mk", "value"),
                
                State("nettokaltmiete_mk", "value"),
                State("steigerung_nettokaltmiete_mk", "value"),
                State("unsicherheit_steigerung_nettokaltmiete_mk", "value"),
                
                State("familienstand_mk", "value"),
                State("kapitalertragssteuer_mk", "value"),
            
                
                State("verzinsung_ek_mk", "value"),
                State("unsicherheit_verzinsung_ek_mk", "value"),
                State("etf_vergleich_mk", "value"),
            ],
            )
def download_data(n_clicks, 
            anlagehorizont,
            eigenkapital,
                
            kaufpreis,
            renovierungskosten,
            kaufnebenkosten,
            instandhaltungskosten,
            kostensteigerung,
            unsicherheit_kostensteigerung,
            wertsteigerung,
            unsicherheit_wertsteigerung,
            
            
            zinsbindung,
            zinssatz,
            tilgungssatz,
            anschlusszinssatz,
            unsicherheit_anschlusszinssatz,
            
            nettokaltmiete,
            steigerung_nettokaltmiete,
            unsicherheit_steigerung_nettokaltmiete,
            
            familienstand,
            kapitalertragssteuer,
            
            verzinsung_ek,
            unsicherheit_verzinsung_ek,
            etf_vergleich,
):
    #print(n_clicks)
    if n_clicks != None:
        df = pd.DataFrame({"anlagehorizont":[anlagehorizont],
   "eigenkapital":[eigenkapital],
   "kaufpreis":[kaufpreis],
   "renovierungskosten":[renovierungskosten],
   "kaufnebenkosten":[kaufnebenkosten],
   "instandhaltungskosten":[instandhaltungskosten],
   "kostensteigerung":[kostensteigerung],
   "unsicherheit_kostensteigerung":[unsicherheit_kostensteigerung],
   "wertsteigerung":[wertsteigerung],
   "unsicherheit_wertsteigerung":[unsicherheit_wertsteigerung],
   
   "zinsbindung":[zinsbindung],
   "zinssatz":[zinssatz],
   "tilgungssatz":[tilgungssatz],
   "anschlusszinssatz":[anschlusszinssatz],
   "unsicherheit_anschlusszinssatz":[unsicherheit_anschlusszinssatz],
   
   "nettokaltmiete":[nettokaltmiete],
   "steigerung_nettokaltmiete":[steigerung_nettokaltmiete],
   "unsicherheit_steigerung_nettokaltmiete":[unsicherheit_steigerung_nettokaltmiete],
   
   "familienstand":[familienstand],
   "kapitalertragssteuer":[kapitalertragssteuer],
   
   "verzinsung_ek":[verzinsung_ek],
   "unsicherheit_verzinsung_ek":[unsicherheit_verzinsung_ek],
   "etf_vergleich":[etf_vergleich]
                           },
                          index=["Daten"]
        )
        #print(df)
        return send_data_frame(df.to_csv, filename='data.csv')


# if __name__ == "__main__":
#     app.run_server(debug=True)