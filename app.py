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
                        html.Label("Mieteinahmen"),
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
                        html.Label("Mietsteigerung"),
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
                        html.Label("Instandhaltungskosten Jahr "),
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
                        html.Label("Verwaltungskosten Jahr"),
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
                        html.Label("Pauschale für Mietausfall"),
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
                        html.Label("Unsicherheit Mietausfall"),
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
                        html.Label("Geschätzte Kostensteigerung"),
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
                        html.Label("Unsicherheit Kostensteigerung"),
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
                        html.Label("Eigenkapital"),
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
                        html.Label("Zinsbindung"),
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
                        html.Label("Disagio"),
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
                        html.Label("Zinssatz"),
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
                        html.Label("Tilgungssatz"),
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
                        html.Label("Anschlusszinssatz"),
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
                        html.Label("Unsicherheit Anschlusszinssatz"),
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
                        html.Label("Zu versteuerndes Einkommen"),
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
                        html.Label("Anlagehorizont"),
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
                        html.Label("Geschätzter Verkaufsfaktor"),
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
                        html.Label("Unsicherheit Verkaufsfaktor"),
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
        # row sixteen
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[html.H4("6. Simulation"),],
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
                                      dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1")
        ),],
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
                    children=[html.H4("7. Import/Export der Eingabeparameter"),],
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
                        "margin-left": "3vw",
                        "margin-top": "0vw",
                    },
                ),
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
        # row 20
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[
                        html.H4("Berechnete Kennzahlen"),
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
        # 21
        html.Div(
            children=[
                # first column of third row
                html.Div(
                    children=[
                        html.H4(
                            "Verteilung der mit Unsicherheit behafteten Eingabeparameter"
                        ),
                        dcc.Graph(id="eingabe_verkaufsfaktor"),
                        dcc.Graph(id="eingabe_anschlusszinssatz"),
                        dcc.Graph(id="eingabe_mietsteigerung"),
                        dcc.Graph(id="eingabe_kostensteigerung"),
                        dcc.Graph(id="eingabe_mietausfall"),
                        html.H4("Ergebnisse der Simulation"),
                        dcc.Markdown(id='ergebnisse'),
                        dcc.Graph(id="verkaufspreis"),
                        dcc.Graph(id="objektrendite"),
                        dcc.Graph(id="eigenkapitalrendite"),
                        dcc.Graph(id="gewinn"),
                        dcc.Graph(id="minimaler_cashflow"),
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
    darlehen = (gesamtkosten - eigenkapital) / (1 - disagio)
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
    Output('ergebnisse', 'children'),
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
):
    # Call formeln.py here

    # Preprocessing arguments
    if baujahr == 0:
        baujahr = 1950
    else:
        baujahr = 1900

    if familienstand == 0:
        alleinstehend = True
    else:
        alleinstehend = False

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
    )

    def figure_ein_aus_gabeparameter(eingabeparameter, name, zeichen, x, runden):
        # Geschätzter Verkaufspreis
        eingabeparameter = np.array(ergebnis[eingabeparameter])
        eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]
        if np.all(eingabeparameter == eingabeparameter[0]) == True:
            fig = go.Figure(data=[go.Table()])
        else:
            fig = ff.create_distplot([eingabeparameter], [name], show_hist=False)
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
            fig = fig.add_vline(
                x=np.quantile(eingabeparameter, q=0.05),
                line_width=3,
                line_dash="dash",
                line_color="red",
                annotation_text=f"5% Quantil: {round(np.quantile(eingabeparameter, q=.05)*x,runden)} {zeichen}",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="red",
            )
            fig = fig.add_vline(
                x=np.quantile(eingabeparameter, q=0.95),
                line_width=3,
                line_dash="dash",
                line_color="green",
                annotation_text=f"95% Quantil: {round(np.quantile(eingabeparameter, q=.95)*x,runden)} {zeichen}",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="green",
            )
            fig.update_layout(plot_bgcolor="white")
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
            fig.update_layout(showlegend=False)
            fig.update_layout(title=name)
        return fig

    fig_verkaufsfaktor = figure_ein_aus_gabeparameter(
        eingabeparameter="verkaufsfaktor",
        name="Verkaufsfaktor",
        zeichen="",
        x=1,
        runden=0,
    )

    fig_anschlusszinssatz = figure_ein_aus_gabeparameter(
        eingabeparameter="anschlusszinssatz",
        name="Anschlusszinssatz",
        zeichen="%",
        x=100,
        runden=2,
    )

    fig_mietsteigerung = figure_ein_aus_gabeparameter(
        eingabeparameter="mietsteigerung",
        name="Mietsteigerung pro Jahr",
        zeichen="%",
        x=100,
        runden=2,
    )

    fig_kostensteigerung = figure_ein_aus_gabeparameter(
        eingabeparameter="kostensteigerung",
        name="Kostensteigerung pro Jahr",
        zeichen="%",
        x=100,
        runden=2,
    )

    fig_mietausfall = figure_ein_aus_gabeparameter(
        eingabeparameter="mietausfall",
        name="Mietausfall pro Jahr",
        zeichen="%",
        x=100,
        runden=2,
    )

    fig_verkaufspreis = figure_ein_aus_gabeparameter(
        eingabeparameter="verkaufspreis",
        name="Verkaufspreis",
        zeichen="€",
        x=1,
        runden=0,
    )

    fig_objektrendite = figure_ein_aus_gabeparameter(
        eingabeparameter="objektrendite",
        name="Objektrendite",
        zeichen="%",
        x=100,
        runden=2,
    )

    fig_eigenkapitalrendite = figure_ein_aus_gabeparameter(
        eingabeparameter="eigenkapitalrendite",
        name="Eigenkapitalrendite",
        zeichen="%",
        x=100,
        runden=2,
    )

    fig_gewinn = figure_ein_aus_gabeparameter(
        eingabeparameter="gewinn", name="Gewinn", zeichen="€", x=1, runden=0,
    )

    fig_minimaler_cashflow = figure_ein_aus_gabeparameter(
        eingabeparameter="minimaler_cashflow",
        name="Minimaler Cashflow",
        zeichen="€",
        x=1,
        runden=0,
    )
    
    antwort = "Fertig :)"
    
    verk_text = np.array(ergebnis["verkaufspreis"])
    verk_text = verk_text[~np.isnan(verk_text)]
    ekr_text = np.array(ergebnis["eigenkapitalrendite"])
    ekr_text = ekr_text[~np.isnan(ekr_text)]
    
    ergebnisse = f"""Nach **{anlagehorizont} Jahren** werden Sie einen durchschnittlichen
    Verkaufspreis von **{round(verk_text.mean())} €** erzielen. Ihre durchschnittliche
    Eigenkapitalrendite liegt bei **{round(ekr_text.mean()*100, 2)} %** usw...."""
    
 #   bla=300_000

    return (
#        bla,
        ergebnisse,
        antwort,
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
    )

import base64
import io
import xlrd
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
#    try:
    if 'csv' in filename:
# Assume that the user uploaded a CSV file
        df = pd.read_csv(
        io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
# Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded)) 
    else:
        df = "Keine csv oder xls Datei"
 #   except Exception as e:
#        return print("Upload nich erfolgreich")
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
        #print(list_of_contents[-1])
        print(list_of_names[-1])
        print(list_of_dates[-1])
        df = parse_contents(list_of_contents[-1], list_of_names[-1], list_of_dates[-1])        
        print(list(df.columns))
        print(df)
        if isinstance(df, pd.DataFrame): 
            if list(df.columns)==default_column:
                return "**Upload erfolgreich**", *default_input # Change value of input fields if upload is succesfull
            if list(df.columns)!=default_column:
                return "**Falsches Format**", *default_input
        else:
            text_message = df
            return text_message, *default_input
    else:
        return text_message, *default_input



if __name__ == "__main__":
    app.run_server(debug=True)
