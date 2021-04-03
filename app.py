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

VALID_USERNAME_PASSWORD_PAIRS = {"Christoph": "Groener"}

# Initialize the app
app = dash.Dash(__name__)
server = app.server
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
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
                    children=[html.H3("Immobilienrendite-Simulator"),
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
                        html.Label("davon Grundstücksanteil (Euro)"),
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
                        html.Label("davon Sanierungskosten (Euro)*",
                                   title="nach § 7h oder § 7i EStG: Nur für die Sanierung von Baudenkmälern und Gebäuden in Sanierungsgebieten"),
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
                        html.Label("Kaufnebenkosten (Euro)*",
                                   title="Umfassen Makler und Notarkosten sowie die Grunderwerbssteuer."),
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
                        html.Label("Renovierungskosten (Euro)*",
                                   title="Kosten die im Jahr des Kaufs anfallen und steuerlich Absetzbar sind (Sanierungskosten dürfen 15% der Gebäudekosten nicht überschreiten)."),
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
                    children=[html.H4("2. Miete und laufende Kosten (pro Jahr)"),],
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
                        html.Label("Mieteinahmen (Euro)*",
                                   title="Nettokaltmiete"),
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
                        html.Label("Mietsteigerung (%)*",
                                   title="Erwartungswert"),
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
                        html.Label("Unsicherheit Mietsteigerung*",
                                   title="Standardabweichung"),
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
                        html.Label("Instandhaltungskosten (Euro)"),
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
                        html.Label("Verwaltungskosten (Euro)"),
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
        # row six
        html.Div(
            children=[
                # first column
                html.Div(
                    children=[
                        html.Label("Pauschale für Mietausfall (%)*",
                                   title="Erwartungswert"),
                        dcc.Input(
                            id="mietausfall",
                            placeholder="Eingabe...",
                            type="number",
                            value=2,
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
                        html.Label("Unsicherheit Mietausfall*",
                                   title="Standardabweichung"),
                        dcc.Input(
                            id="unsicherheit_mietausfall",
                            placeholder="Eingabe...",
                            type="number",
                            value=2,
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
                # third column
                html.Div(
                    children=[
                        html.Label("Geschätzte Kostensteigerung (%)*",
                                   title="Erwartungswert"),
                        dcc.Input(
                            id="kostensteigerung",
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
        # row seven
        html.Div(
            children=[
                # first column
                html.Div(
                    children=[
                        html.Label("Unsicherheit Kostensteigerung*",
                                   title="Standardabweichung"),
                        dcc.Input(
                            id="unsicherheit_kostensteigerung",
                            placeholder="Eingabe...",
                            type="number",
                            value=2,
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
        # row eight
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("3. Finanzierung"),],
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
                # third column
                html.Div(
                    children=[
                        html.Label("Disagio (%)"),
                        dcc.Input(
                            id="disagio",
                            placeholder="Eingabe...",
                            type="number",
                            value=0,
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
                # first column
                html.Div(
                    children=[
                        html.Label("Zinssatz (%)"),
                        dcc.Input(
                            id="zinsatz",
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
                # third column
                html.Div(
                    children=[
                        html.Label("Anschlusszinssatz (%)*",
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
            ],
            className="row",
        ),
        # row eleven
        html.Div(
            children=[
                # first column
                html.Div(
                    children=[
                        html.Label("Unsicherheit Anschlusszinssatz*",
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
                                {"label": "Alleinstehend", "value": "0"},
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
                        html.Label("Zu versteuerndes Einkommen (Euro)"),
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
                # third column
                html.Div(
                    children=[
                        html.Label("Baujahr"),
                        dcc.RadioItems(
                            id="baujahr",
                            options=[
                                {"label": "nach 1924", "value": "0"},
                                {"label": "bis 1924", "value": "1"},
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
                        html.Label("Geschätzter Verkaufsfaktor*",
                                   title="Kaufpreis-Miet-Verhältnis (Erwartungswert)"),
                        dcc.Input(
                            id="verkaufsfaktor",
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
                        html.Label("Unsicherheit Verkaufsfaktor*",
                                   title="Standardabweichung"),
                        dcc.Input(
                            id="unsicherheit_verkaufsfaktor",
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
                                {"label": "MSCI World", "value": "0"},
                                {"label": "Dax","value": "1",},
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
        # Berechnete Kennzahlen
        # row 20
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[
                        html.H4("Berechnete Kennzahlen"),
                        dcc.Markdown(text_statisch["berechnete_kennzahlen"]),
                        dash_table.DataTable(
                            id="table",
                            style_cell={
                                "textAlign": "left",
                                "fontSize": 14,
                                "font-family": "sans-serif",
                            },
                            style_as_list_view=True,
                            style_header={
                                "backgroundColor": "white",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                    style={
                        #  "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                        "margin-right": "15vw",
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
            'Daten importieren',
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
        
        # Next row
        # html.Div(
        #     children=[
        #         # first column of third row
        #         html.Button("Daten exportieren", id='download-results-button'),
        #         Download(id='download'),                
        #     ],                    
        #     style={
        #                 "display": "inline-block",
        #                 "vertical-align": "top",
        #                 "margin-left": "3vw",
        #                 "margin-top": "1vw",
        #             },
        #     className="row",
        # ),

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
                        dcc.Graph(id="eingabe_verkaufsfaktor"),
                        dcc.Markdown(id='verkaufsfaktor_text'),
                        dcc.Graph(id="eingabe_anschlusszinssatz"),
                        dcc.Markdown(id='anschlusszinssatz_text'),                        
                        dcc.Graph(id="eingabe_mietsteigerung"),
                        dcc.Markdown(id='mietsteigerung_text'),
                        dcc.Graph(id="eingabe_kostensteigerung"),
                        dcc.Markdown(id='kostensteigerung_text'),
                        dcc.Graph(id="eingabe_mietausfall"),
                        dcc.Markdown(id='mietausfall_text'),
                        html.H4("Ergebnisse der Simulation"),
                        dcc.Markdown(text_statisch["ergebnisse"]),
                        dcc.Graph(id="verkaufspreis"),
                        dcc.Markdown(id='verkaufspreis_text'),
                        dcc.Graph(id="objektrendite"),
                        dcc.Markdown(id='objektrendite_text'),
                        dcc.Graph(id="eigenkapitalrendite"),
                        dcc.Markdown(id='eigenkapitalrendite_text'),
                        dcc.Graph(id="gewinn"),
                        dcc.Markdown(id='gewinn_text'),
                        dcc.Graph(id="minimaler_cashflow"),
                        dcc.Markdown(id='minimaler_cashflow_text'),
                        html.H6("ETF Vergleich"),
                        dcc.Graph(id="etf_rendite"),
                        dcc.Graph(id="etf_gewinn"),
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
    Output("table", "columns"),
    Output("table", "data"),
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
def updateTable(
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
    darlehen = (gesamtkosten - eigenkapital) / (1 - (disagio/100))
    kreditrate_jahr = darlehen * ((zinsatz / 100) + (tilgungssatz / 100))

    df = pd.DataFrame(
        {
            "Kennzahlen": [
                "Gesamtkosten",
                "Kaufpreis-Miet-Verhältnis",
                "Brutto-Mietrendite",
                "Netto-Mietrendite",
                "Darlehenshöhe",
                "Kreditrate (Jahr)",
            ],
            "Berechnungen": [
                f"{gesamtkosten}€",
                kaufpreis_miet_verhaeltnis,
                f"{anfangs_brutto_mietrendite}%",
                f"{anfangs_netto_mietrendite}%",
                f"{int(darlehen)}€",
                f"{int(kreditrate_jahr)}€",
            ],
        }
    )
    data = df.to_dict("records")
    columns = [{"name": i, "id": i} for i in df.columns]

    return columns, data


@app.callback(
    #   Output("kennzahlen1", "figure"),
#    Output('kaufpreis', 'value'),
#    Output('einleitung_text', 'children'),
    Output('anschlusszinssatz_text', 'children'),
    Output('verkaufsfaktor_text', 'children'),
    Output('mietsteigerung_text', 'children'),
    Output('kostensteigerung_text', 'children'),
    Output('mietausfall_text', 'children'),
    #Output('ergebnisse_text', 'children'),
    Output('verkaufspreis_text', 'children'),
    Output('objektrendite_text', 'children'),
    Output('eigenkapitalrendite_text', 'children'),
    Output('gewinn_text', 'children'),
    Output('minimaler_cashflow_text', 'children'),
    Output("loading-output-1", "children"),
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
    Output("etf_rendite", "figure"),
    Output("etf_gewinn", "figure"),
    [Input("button", "n_clicks")],
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
        #     State('sonderabschreibung', 'value'),
        State("anlagehorizont", "value"),
        State("verkaufsfaktor", "value"),
        State("unsicherheit_verkaufsfaktor", "value"),
        State("sim_runs", "value"),
        State("etf_vergleich", "value"),
    ],
)
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
    etf_vergleich,
):
    # Call formeln.py here

    # Preprocessing arguments
    if int(baujahr) == 0:
        baujahr = 1950
    else:
        baujahr = 1900
    
    if int(familienstand) == 0:
        alleinstehend = True
    else:
        alleinstehend = False
        
    if int(etf_vergleich)==0:    # MSCI World
        etf_rendite = 0.08
        unsicherheit_etf_rendite = 0.1
    elif int(etf_vergleich)==1:  # Dax
        etf_rendite = 0.06
        unsicherheit_etf_rendite = 0.08

    ergebnis = renditerechner(
        kaufpreis=kaufpreis,
        kaufpreis_grundstueck=kaufpreis_grundstueck,
        kaufpreis_sanierung=kaufpreis_sanierung,
        kaufnebenkosten=kaufnebenkosten,
        renovierungskosten=renovierungskosten,
        mieteinnahmen=mieteinnahmen,
        mietsteigerung=(mietsteigerung / 100),
        unsicherheit_mietsteigerung=(unsicherheit_mietsteigerung / 100),
        erste_mieterhoehung=erste_mieterhoehung,
        instandhaltungskosten=instandhaltungskosten,
        verwaltungskosten=verwaltungskosten,
        mietausfall=(mietausfall / 100),
        unsicherheit_mietausfall=(unsicherheit_mietausfall / 100),
        kostensteigerung=(kostensteigerung / 100),
        unsicherheit_kostensteigerung=(unsicherheit_kostensteigerung / 100),
        eigenkapital=eigenkapital,
        zinsbindung=zinsbindung,
        disagio=(disagio / 100),
        zinsatz=(zinsatz / 100),
        tilgungssatz=(tilgungssatz / 100),
        anschlusszinssatz=(anschlusszinssatz / 100),
        unsicherheit_anschlusszinssatz=(unsicherheit_anschlusszinssatz / 100),
        alleinstehend=alleinstehend,
        einkommen=einkommen,
        baujahr=baujahr,
        anlagehorizont=anlagehorizont,
        verkaufsfaktor=verkaufsfaktor,
        unsicherheit_verkaufsfaktor=unsicherheit_verkaufsfaktor,
        sim_runs=sim_runs,
        steuerjahr=2021,
        etf_rendite=etf_rendite,
        unsicherheit_etf_rendite=unsicherheit_etf_rendite,
    )

    def figure_ein_aus_gabeparameter(eingabeparameter, name, zeichen, x, runden, area):
        
        eingabeparameter = np.array(ergebnis[eingabeparameter])
        eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]
        if np.all(eingabeparameter == eingabeparameter[0]) == True:
            fig = go.Figure(data=[go.Table()])
        else:
            fig = ff.create_distplot([eingabeparameter], [name], show_hist=False, show_rug=False)
            
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
                annotation_font_color="black",)
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
                annotation_font_color="black",)
            elif (name=="Objektrendite" or name=="Eigenkapitalrendite") and (eingabeparameter.min()<0):
                fig = fig.add_vline(
                x=0,
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{round(len(eingabeparameter[eingabeparameter<0])/len(eingabeparameter)*100,2)} % Quantil",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",)                
            else:
                fig = fig.add_vline(
                    x=np.quantile(eingabeparameter, q=0.05),
                    line_width=3,
                    line_dash="dash",
                    line_color="black",
                    annotation_text=f"5% Quantil: {round(np.quantile(eingabeparameter, q=.05)*x,runden)} {zeichen}",
                    annotation_position="bottom right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                )
                
            fig = fig.add_vline(
                    x=np.quantile(eingabeparameter, q=0.95),
                    line_width=3,
                    line_dash="dash",
                    line_color="black",
                    annotation_text=f"95% Quantil: {round(np.quantile(eingabeparameter, q=.95)*x,runden)} {zeichen}",
                    annotation_position="bottom right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                )
                #fig.update_layout(yaxis_range=[0,4])
            fig = fig.add_vline(
                    x=np.quantile(eingabeparameter, q=0.5),
                    line_width=3,
                    line_dash="dash",
                    line_color="black",
                    annotation_text=f"Median: {round(np.quantile(eingabeparameter, q=0.5)*x,runden)} {zeichen}",
                    annotation_position="top right",
                    annotation_font_size=12,
                    annotation_font_color="black",
                )

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
        runden=0,
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

        fig = fig.add_vline(
                            x=np.quantile(eingabeparameter1, q=0.5),
                            line_width=3,
                            line_dash="dash",
                            line_color="cornflowerblue",
                            annotation_text=f"Median: {round(np.quantile(eingabeparameter1, q=0.5)*x,runden)} {zeichen}",
                            annotation_position="top left",
                            annotation_font_size=12,
                            annotation_font_color="black",
                        )

        fig = fig.add_vline(
                            x=np.quantile(eingabeparameter2, q=0.5),
                            line_width=3,
                            line_dash="dash",
                            line_color="orange",
                            annotation_text=f"Median: {round(np.quantile(eingabeparameter2, q=0.5)*x,runden)} {zeichen}",
                            annotation_position="top right",
                            annotation_font_size=12,
                            annotation_font_color="black",
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
        name2="ETF",
        zeichen="%",
        x=100,
        runden=2,
        ueberschrift="Eigenkapitalrendite"
    )
    
    fig_etf_gewinn = figure_etf_vergleich(
        eingabeparameter1="gewinn",
        eingabeparameter2="etf_gewinn",
        name1="Immobilie",
        name2="ETF",
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
