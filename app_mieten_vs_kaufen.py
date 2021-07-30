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
                            id="anlagehorizont",
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
                            id="eigenkapital",
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
                            id="kaufnebenkosten",
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
                            id="instandhaltungskosten",
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
                            id="zinsbindung",
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
                            id="nettokaltmiete",
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
                            id="unsicherheit_steigerung_nettokaltmiete",
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
                        html.Label("Kapitalertragssteuer (%)"),
                        dcc.Input(
                            id="kapitalertragssteuer",
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
                            id="verzinsung_ek",
                            placeholder="Eingabe...",
                            type="number",
                            value=2.2,
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
                            # dcc.Store inside the app that stores the intermediate value
                        dcc.Store(id='intermediate-value-investiert'),
                        dcc.Store(id='intermediate-value-nicht-investiert'),
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
                        id="grafik_selector_investiert"),  
                        dcc.Graph(id="mieten_vs_kaufen_investiert"),  
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
                        id="grafik_selector_nicht_investiert"),  
                        dcc.Graph(id="mieten_vs_kaufen_nicht_investiert"),                                                
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
    Output('intermediate-value-investiert', 'data'),
    Output('intermediate-value-nicht-investiert', 'data'),
    [Input("button", "n_clicks")],
    state=[
        State("anlagehorizont", "value"),
        State("eigenkapital", "value"),
        
        State("kaufpreis", "value"),
        State("renovierungskosten", "value"),
        State("kaufnebenkosten", "value"),
        State("instandhaltungskosten", "value"),
        State("kostensteigerung", "value"),
        State("unsicherheit_kostensteigerung", "value"),
        State("wertsteigerung", "value"),
        State("unsicherheit_wertsteigerung", "value"),
        
        State("zinsbindung", "value"),
        State("zinssatz", "value"),
        State("tilgungssatz", "value"),
        State("anschlusszinssatz", "value"),
        State("unsicherheit_anschlusszinssatz", "value"),
        
        State("nettokaltmiete", "value"),
        State("steigerung_nettokaltmiete", "value"),
        State("unsicherheit_steigerung_nettokaltmiete", "value"),
        
        State("familienstand", "value"),
        State("kapitalertragssteuer", "value"),
      
        
        State("verzinsung_ek", "value"),
        State("unsicherheit_verzinsung_ek", "value"),
        State("etf_vergleich", "value"),
    ],
)
def custom_figure(
    button,
    
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
        

    ergebnis = mieten_kaufen(
        anlagehorizont=anlagehorizont,
        eigenkapital=eigenkapital,

        kaufpreis=kaufpreis,
        renovierungskosten=renovierungskosten,
        kaufnebenkosten=kaufnebenkosten,
        instandhaltungskosten=instandhaltungskosten,
        kostensteigerung=kostensteigerung/100,
        unsicherheit_kostensteigerung=unsicherheit_kostensteigerung,
        wertsteigerung=wertsteigerung/100,
        unsicherheit_wertsteigerung=unsicherheit_wertsteigerung,
        
        zinsbindung=zinsbindung,
        zinsatz=zinssatz/100,
        tilgungssatz=tilgungssatz/100,
        anschlusszinssatz=anschlusszinssatz/100,
        unsicherheit_anschlusszinssatz=unsicherheit_anschlusszinssatz,

        nettokaltmiete=nettokaltmiete,
        steigerung_nettokaltmiete=steigerung_nettokaltmiete/100,
        unsicherheit_steigerung_nettokaltmiete=unsicherheit_steigerung_nettokaltmiete,

        alleinstehend=alleinstehend,
        kapitalertragssteuer=kapitalertragssteuer/100,
        
        etf_rendite = etf_rendite,
        unsicherheit_etf_rendite=unsicherheit_etf_rendite,
        fest_verzinst=verzinsung_ek/100,
        unsicherheit_fest_verzinst=unsicherheit_verzinsung_ek,
    )

    #print(ergebnis["etf_vermoegen_immo_versteuert_pj"])
    
    # Aufbereitung der Ergebnisse
    ergebnisse_aufbereitet_investiert = {
        "jahr_pj":ergebnis["jahr_pj"],
        "Immobilie + ETF":np.array(ergebnis["vermoegen_immo_pj"])+np.array(ergebnis["etf_vermoegen_immo_pj"]),
        "Immobilie + ETF (versteuert)":np.array(ergebnis["vermoegen_immo_pj"])+np.array(ergebnis["etf_vermoegen_immo_versteuert_pj"]),
        "Immobilie + Festgeld":np.array(ergebnis["vermoegen_immo_pj"])+np.array(ergebnis["festgeld_vermoegen_immo_pj"]),
        "Immobilie + Festgeld (versteuert)":np.array(ergebnis["vermoegen_immo_pj"])+np.array(ergebnis["festgeld_vermoegen_immo_versteuert_pj"]),
        "ETF": ergebnis["etf_vermoegen_pj"],
        "ETF (versteuert)": ergebnis["etf_vermoegen_versteuert_pj"],
        "Festgeld": ergebnis["festgeld_vermoegen_pj"],
        "Festgeld (versteuert)": ergebnis["festgeld_vermoegen_versteuert_pj"],
    }
    
    ergebnisse_aufbereitet_nicht_investiert = {
        "jahr_pj":ergebnis["jahr_pj"],
        "Immobilie":ergebnis["vermoegen_immo_pj"],
        "ETF":ergebnis["etf_vermoegen_initial_pj"],
        "ETF (versteuert)":ergebnis["etf_vermoegen_initial_versteuert_pj"],
        "Festgeld":ergebnis["etf_vermoegen_initial_pj"],
        "Festgeld (versteuert)":ergebnis["etf_vermoegen_initial_versteuert_pj"],
    }
    
    #print(ergebnisse_aufbereitet_investiert)
    #print(ergebnisse_aufbereitet_nicht_investiert)
    return (
        ergebnisse_aufbereitet_investiert,
        ergebnisse_aufbereitet_nicht_investiert
    )
    
@app.callback(
              Output('mieten_vs_kaufen_investiert', 'figure'),
              Output('mieten_vs_kaufen_nicht_investiert', 'figure'),
              Input('intermediate-value-investiert', 'data'),
              Input('intermediate-value-nicht-investiert', 'data'),
              Input('grafik_selector_investiert', "value"),
              Input('grafik_selector_nicht_investiert', "value"),
               )
def update_graph(ergebnisse_investiert, ergebnisse_nicht_investiert, grafik_selector_investiert,
                 grafik_selector_nicht_investiert):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    # print(ergebnisse_investiert)
    # print(grafik_selector_investiert)
    # print(ergebnisse_nicht_investiert)
    # print(grafik_selector_nicht_investiert)
   # bla = auswahl
    #print(dff)
  
    
    fig_vermoegen_investiert = go.Figure()
    for wahl in grafik_selector_investiert:
        fig_vermoegen_investiert.add_trace(go.Scatter(x=ergebnisse_investiert["jahr_pj"], y=ergebnisse_investiert[wahl],
                    mode='lines+markers',
                    name=wahl))

    fig_vermoegen_investiert.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
    
    fig_vermoegen_nicht_investiert = go.Figure()
    for wahl in grafik_selector_nicht_investiert:
        fig_vermoegen_nicht_investiert.add_trace(go.Scatter(x=ergebnisse_nicht_investiert["jahr_pj"], y=ergebnisse_nicht_investiert[wahl],
                    mode='lines+markers',
                    name=wahl))

    fig_vermoegen_nicht_investiert.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))    
    
    
    return (fig_vermoegen_investiert, fig_vermoegen_nicht_investiert)
    
# #
# # CSV/Excel Import
# #

# def parse_contents(contents, filename, date):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     if 'csv' in filename:
# # Assume that the user uploaded a CSV file
#         df = pd.read_csv(
#         io.StringIO(decoded.decode('utf-8')))
#     elif 'xls' in filename:
# # Assume that the user uploaded an excel file
#         df = pd.read_excel(io.BytesIO(decoded)) 
#     else:
#         df = "**Keine csv oder xlsx Datei**"
#     return df

# # Upload component: The same file can NOT be uploaded twice in a row. It will not
# # get recognized. This is something we need to live with right now. In the future we 
# # could checkout:
# # https://community.plotly.com/t/reuploading-same-file/42178
# # https://community.plotly.com/t/can-i-upload-the-same-file-twice-in-a-row/40526/3
# @app.callback(Output('upload-status', 'children'),
#                 Output("kaufpreis", "value"),
#                 Output("kaufpreis_grundstueck", "value"),
#                 Output("kaufpreis_sanierung", "value"),
#                 Output("kaufnebenkosten", "value"),
#                 Output("renovierungskosten", "value"),
#                 Output("mieteinnahmen", "value"),
#                 Output("mietsteigerung", "value"),
#                 Output("unsicherheit_mietsteigerung", "value"),
#                 Output("erste_mieterhoehung", "value"),
#                 Output("instandhaltungskosten", "value"),
#                 Output("verwaltungskosten", "value"),
#                 Output("mietausfall", "value"),
#                 Output("unsicherheit_mietausfall", "value"),
#                 Output("kostensteigerung", "value"),
#                 Output("unsicherheit_kostensteigerung", "value"),
#                 Output("eigenkapital", "value"),
#                 Output("zinsbindung", "value"),
#                 Output("disagio", "value"),
#                 Output("zinsatz", "value"),
#                 Output("tilgungssatz", "value"),
#                 Output("anschlusszinssatz", "value"),
#                 Output("unsicherheit_anschlusszinssatz", "value"),
#                 Output("familienstand", "value"),
#                 Output("einkommen", "value"),
#                 Output("baujahr", "value"),
#                 #    Input("sonderabschreibung", "value"),
#                 Output("anlagehorizont", "value"),
#                 Output("verkaufsfaktor", "value"),
#                 Output("unsicherheit_verkaufsfaktor", "value"),
#               [Input('upload-data', 'contents')],
#               [State('upload-data', 'filename'),
#                State('upload-data', 'last_modified')])
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     default_input = [
#         300_000, 100_000, 0, 40_000, 1_000, 12_000, 2, 1, 5, 1_200, 600, 2, 2, 1.5,
#         2, 100_000, 20, 0, 1.5, 2.5, 4, 1.5, "0", 100_000, "0", 15, 22, 4
#     ]   
#     default_column = [
#         'Kaufpreis', 'davon Grundstücksanteil', 'davon Sanierungskosten', 
#         'Kaufnebenkosten', 'Renovierungskosten', 'Mieteinahmen', 'Mietsteigerung', 
#         'Unsicherheit Mietsteigerung', 'Erste Mieterhöhung ab Jahr', 'Instandhaltungskosten Jahr', 
#         'Verwaltungskosten Jahr', 'Pauschale für Mietausfall', 'Unsicherheit Mietausfall', 
#         'Geschätzte Kostensteigerung', 'Unsicherheit Kostensteigerung', 'Eigenkapital', 
#         'Zinsbindung', 'Disagio', 'Zinssatz', 'Tilgungssatz', 'Anschlusszinssatz', 
#         'Unsicherheit Anschlusszinssatz', 'Familienstand', 'Zu versteuerndes Einkommen', 
#         'Baujahr', 'Anlagehorizont', 'Geschätzter Verkaufsfaktor', 'Unsicherheit Verkaufsfaktor'
#     ] 
#     text_message = ""
#     if list_of_contents is not None:
#         df = parse_contents(list_of_contents[-1], list_of_names[-1], list_of_dates[-1])        
#         if isinstance(df, pd.DataFrame): 
#             if "Unnamed: 0" in list(df.columns):                
#                 df.drop(["Unnamed: 0"], axis=1, inplace=True)
#             imported_input = (
#                 str(df[i][0]) 
#                 if i in ["Familienstand", "Baujahr"] 
#                 else df[i][0] 
#                 for i in list(df.columns)
#             )
#             #print(list(df.columns))
#             if list(df.columns)==default_column:
#                 return "**Upload erfolgreich**", *imported_input 
#             if list(df.columns)!=default_column:
#                 return "**Falsches Format**", *default_input
#         else:
#             text_message = df
#             return text_message, *default_input
#     else:
#         return text_message, *default_input

# #
# # CSV Export
# #

# @app.callback(Output('download', 'data'),
#              [Input('download-results-button', 'n_clicks')],
#              state=[
#             State("kaufpreis", "value"),
#             State("kaufpreis_grundstueck", "value"),
#             State("kaufpreis_sanierung", "value"),
#             State("kaufnebenkosten", "value"),
#             State("renovierungskosten", "value"),
#             State("mieteinnahmen", "value"),
#             State("mietsteigerung", "value"),
#             State("unsicherheit_mietsteigerung", "value"),
#             State("erste_mieterhoehung", "value"),
#             State("instandhaltungskosten", "value"),
#             State("verwaltungskosten", "value"),
#             State("mietausfall", "value"),
#             State("unsicherheit_mietausfall", "value"),
#             State("kostensteigerung", "value"),
#             State("unsicherheit_kostensteigerung", "value"),
#             State("eigenkapital", "value"),
#             State("zinsbindung", "value"),
#             State("disagio", "value"),
#             State("zinsatz", "value"),
#             State("tilgungssatz", "value"),
#             State("anschlusszinssatz", "value"),
#             State("unsicherheit_anschlusszinssatz", "value"),
#             State("familienstand", "value"),
#             State("einkommen", "value"),
#             State("baujahr", "value"),
#             #    Input("sonderabschreibung", "value"),
#             State("anlagehorizont", "value"),
#             State("verkaufsfaktor", "value"),
#             State("unsicherheit_verkaufsfaktor", "value"),
#             ],
#             )
# def download_data(n_clicks, 
#                 kaufpreis,
#                 kaufpreis_grundstueck,
#                 kaufpreis_sanierung,
#                 kaufnebenkosten,
#                 renovierungskosten,
#                 mieteinnahmen,
#                 mietsteigerung,
#                 unsicherheit_mietsteigerung,
#                 erste_mieterhoehung,
#                 instandhaltungskosten,
#                 verwaltungskosten,
#                 mietausfall,
#                 unsicherheit_mietausfall,
#                 kostensteigerung,
#                 unsicherheit_kostensteigerung,
#                 eigenkapital,
#                 zinsbindung,
#                 disagio,
#                 zinsatz,
#                 tilgungssatz,
#                 anschlusszinssatz,
#                 unsicherheit_anschlusszinssatz,
#                 familienstand,
#                 einkommen,
#                 baujahr,
#                 #    sonderabschreibung,
#                 anlagehorizont,
#                 verkaufsfaktor,
#                 unsicherheit_verkaufsfaktor,
# ):
#     #print(n_clicks)
#     if n_clicks != None:
#         df = pd.DataFrame({"Kaufpreis": [kaufpreis], 
#                            "davon Grundstücksanteil": [kaufpreis_grundstueck],
#                             "davon Sanierungskosten":[kaufpreis_sanierung],
#                 "Kaufnebenkosten":[kaufnebenkosten],
#                 "Renovierungskosten":[renovierungskosten],
#                 "Mieteinahmen":[mieteinnahmen],
#                 "Mietsteigerung":[mietsteigerung],
#                 'Unsicherheit Mietsteigerung':[unsicherheit_mietsteigerung],
#                 'Erste Mieterhöhung ab Jahr':[erste_mieterhoehung],
#                 'Instandhaltungskosten Jahr':[instandhaltungskosten],
#                 'Verwaltungskosten Jahr':[verwaltungskosten],
#                 'Pauschale für Mietausfall':[mietausfall],
#                 'Unsicherheit Mietausfall':[unsicherheit_mietausfall],
#                 'Geschätzte Kostensteigerung':[kostensteigerung],
#                 'Unsicherheit Kostensteigerung':[unsicherheit_kostensteigerung],
#                 'Eigenkapital':[eigenkapital],
#                 'Zinsbindung':[zinsbindung],
#                 'Disagio':[disagio],
#                 'Zinssatz':[zinsatz],
#                 'Tilgungssatz':[tilgungssatz],
#                 'Anschlusszinssatz':[anschlusszinssatz],
#                 'Unsicherheit Anschlusszinssatz':[unsicherheit_anschlusszinssatz],
#                 'Familienstand':[familienstand],
#                 'Zu versteuerndes Einkommen':[einkommen],
#                 'Baujahr':[baujahr],
#                 #    sonderabschreibung,
#                 'Anlagehorizont':[anlagehorizont],
#                 'Geschätzter Verkaufsfaktor':[verkaufsfaktor],
#                 'Unsicherheit Verkaufsfaktor':[unsicherheit_verkaufsfaktor],
#                            },
#                           index=["Daten"]
#         )
#         #print(df)
#         return send_data_frame(df.to_csv, filename='data.csv')


if __name__ == "__main__":
    app.run_server(debug=True)
