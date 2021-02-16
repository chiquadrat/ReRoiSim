import numpy as np
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State

# Load data
df = pd.read_csv("data/example_data.txt", index_col=0, parse_dates=True)
df.index = pd.to_datetime(df["Date"])

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


# def get_options(list_stocks):
#     dict_list = []
#     for i in list_stocks:
#         dict_list.append({"label": i, "value": i})

#     return dict_list


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
                            #className="div-for-dropdown",
                            children=[
                                # dcc.Dropdown(
                                #     id="stockselector",
                                #     options=get_options(df["stock"].unique()),
                                #     multi=True,
                                #     value=[df["stock"].sort_values()[0]],
                                #     style={"backgroundColor": "#1E1E1E"},
                                #     className="stockselector",
                                # ),
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
                                    id="kaufpreis_grundstueck ",
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
                                html.P("Geschätzte Kostensteigerung pro Jahr"),
                                dcc.Input(
                                    id="kostensteigerung",
                                    placeholder="Eingabe...", 
                                    type="number",
                                    value=1,
                                ),
                                html.H2("3. Finanzierung"),
                                html.P("Eigenkapital"),
                                dcc.Input(
                                    id="eigenkapital",
                                    placeholder="Eingabe...", 
                                    type="number",
                                    value=100_000
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
                                    value=2.5
                                ),
                                html.H2(""),
                                html.P("Geschätzter Anschlusszinssatz"),
                                dcc.Input(
                                    id="anschlusszinssatz",
                                    placeholder="Eingabe...", 
                                    type="number",
                                    value=2.5,
                                ),  
                                html.H2("4. Steuern"),
                                html.P("Familienstand"),
                                dcc.RadioItems(
                                    options=[
                                        {'label': 'Alleinstehend', 'value': '0'},
                                        {'label': 'Ehepaar (zusammen veranlagt)', 'value': '1'},
                                    ],
                                    value='0',
                                    labelStyle={'display': 'inline-block'}
                                ),  
                                html.H2(""),
                                html.P("Zu versteuerndes Einkommen"),
                                dcc.Input(
                                    id="einkommen",
                                    placeholder="Eingabe...", 
                                    type="number",
                                    value=100_000
                                ),  
                                html.H2(""),
                                html.P("Baujahr"),
                                dcc.RadioItems(
                                    options=[
                                        {'label': 'nach 1924', 'value': '0'},
                                        {'label': 'bis 1924', 'value': '1'},
                                    ],
                                    value='0',
                                    labelStyle={'display': 'inline-block'}
                                ),  
                                html.H2(""),
                                html.P("Sonderabschreibung für Neubauwohnung"),
                                dcc.Checklist(
                                    options=[
                                        {'label': 'Ja', 'value': '1'},],
                                ), 
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
                                html.Br(),
                                html.Br(),
                                html.Button(id='submit-button-state', n_clicks=0, children='Submit'),  
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        html.H1("Ergebnisse der Simulation"),
                        html.H2("Kennzahlen"),
                        dcc.Graph(id="kennzahlen"),
                        #html.Div(id='my-output'),
                        # dcc.Graph(
                        #     id="timeseries",
                        #     config={"displayModeBar": False},
                        #     animate=True,
                        # ),
                        html.H2("Grafiken"),
                        dcc.Graph(id="mietentwicklung")
                    ],
                ),
            ],
        )
    ]
)



# Callback for timeseries price
# @app.callback(Output("timeseries", "figure"), Input("stockselector", "value"))
# def update_graph(selected_dropdown_value):
#     trace1 = []
#     df_sub = df
#     for stock in selected_dropdown_value:
#         trace1.append(
#             go.Scatter(
#                 x=df_sub[df_sub["stock"] == stock].index,
#                 y=df_sub[df_sub["stock"] == stock]["value"],
#                 mode="lines",
#                 opacity=0.7,
#                 name=stock,
#                 textposition="bottom center",
#             )
#         )
#     traces = [trace1]
#     data = [val for sublist in traces for val in sublist]
#     figure = {
#         "data": data,
#         "layout": go.Layout(
#             colorway=["#5E0DAC", "#FF4F00", "#375CB1", "#FF7400", "#FFF400", "#FF0056"],
#             template="plotly_dark",
#             paper_bgcolor="rgba(0, 0, 0, 0)",
#             plot_bgcolor="rgba(0, 0, 0, 0)",
#             margin={"b": 15},
#             hovermode="x",
#             autosize=True,
#             title={
#                 "text": "Geschätzter Verkaufspreis",
#                 "font": {"color": "white"},
#                 "x": 0.5,
#             },
#             xaxis={"range": [df_sub.index.min(), df_sub.index.max()]},
#         ),
#     }

#     return figure

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input('submit-button-state', 'n_clicks'),
    State(component_id='kaufpreis', component_property='value'),
    State(component_id='kaufnebenkosten', component_property='value'),
    State(component_id='renovierungskosten', component_property='value'),
)
def update_output_div(n_clicks, kaufpreis, kaufnebenkosten, renovierungskosten):
    gesamtkosten = kaufpreis + kaufnebenkosten + renovierungskosten
    return f"Gesamtkosten: {gesamtkosten}"


@app.callback(
   Output("mietentwicklung", "figure"), 
   Input("mieteinnahmen", "value"),
   Input("mietsteigerung", "value"), 
   Input("erste_mieterhoehung", "value"), 
   Input("anlagehorizont", "value"), 
)
# Produce first custom graph
def custom_figure(mieteinnahmen, mietsteigerung, erste_mieterhoehung, anlagehorizont):
    mietsteigerung = mietsteigerung / 100
    #anlagehorizont = 15
    #erste_mieterhoehung = 5
    runs = 100
    df_sim_miete = pd.DataFrame(columns=["Run", "Miete"]) 
    
    for run in list(range(1,runs+1)):
        mietsteigerung_pj = np.random.normal(mietsteigerung, 0.01, anlagehorizont)
        mieteinnahmen_pj = [mieteinnahmen]  # pj -> pro jahr
        for jahr in range(1, anlagehorizont + 1):
            if jahr >= erste_mieterhoehung:
                mieteinnahmen_pj.append(mieteinnahmen_pj[-1] * (1 + mietsteigerung_pj[jahr-1]))
            else:
                mieteinnahmen_pj.append(mieteinnahmen_pj[-1])

        df = pd.DataFrame({
            "Jahr": np.array(list(range(1, anlagehorizont + 1))),
            "Run":np.full((len(np.array(mieteinnahmen_pj)[1:])), run), 
            "Miete":np.array(mieteinnahmen_pj)[1:]})
        
        df_sim_miete = df_sim_miete.append(df)

    fig = px.line(df_sim_miete, x="Jahr", 
                  y="Miete", title="Mietentwicklung", color="Run")

    return fig

@app.callback(
   Output("kennzahlen", "figure"), 
   Input("kaufpreis", "value"),
   Input("kaufnebenkosten", "value"),
   Input("renovierungskosten", "value"),
   Input("mieteinnahmen", "value"),
   Input("instandhaltungskosten", "value"),
   Input("verwaltungskosten", "value"),
   Input("mietausfall", "value"),
   Input("eigenkapital", "value"),
   Input("disagio", "value"),
   Input("zinsatz", "value"),
   Input("tilgungssatz", "value"),
)
# Produce first custom graph
def custom_figure(kaufpreis, kaufnebenkosten, renovierungskosten,
                  mieteinnahmen, instandhaltungskosten, verwaltungskosten,
                  mietausfall, eigenkapital,
                  disagio, zinsatz, tilgungssatz):
    # Nur zum testen, bleibt natürlich später in dem Formel Modul
    gesamtkosten = kaufpreis + kaufnebenkosten + renovierungskosten
    jahresreinertrag = (
        mieteinnahmen
        - instandhaltungskosten
        - verwaltungskosten
        - (mieteinnahmen * (mietausfall/100))
    )
    kaufpreis_miet_verhaeltnis = round((kaufpreis + renovierungskosten) / mieteinnahmen,1)
    anfangs_brutto_mietrendite = round((1 / kaufpreis_miet_verhaeltnis)*100,2)
    anfangs_netto_mietrendite = round((jahresreinertrag / gesamtkosten)*100,2)

# Finanzierung
    darlehen = (gesamtkosten - eigenkapital) / (1 - disagio)
    kreditrate_jahr = darlehen * ((zinsatz/100) + (tilgungssatz/100))
    
    fig = go.Figure(data=[go.Table(header=dict(values=['Startwerte', ""]),
                 cells=dict(values=[[
                     "Gesamtkosten", 
                     "Kaufpreis-Miet-Verhältnis",
                     "Brutto-Mietrendite",
                     "Netto-Mietrendite", 
                     "Darlehenshöhe", 
                     "Kreditrate (Jahr)"], [
                         f"{gesamtkosten}€", 
                         kaufpreis_miet_verhaeltnis, 
                         f"{anfangs_brutto_mietrendite}%", 
                         f"{anfangs_netto_mietrendite}%",
                         f"{int(darlehen)}€",
                         f"{int(kreditrate_jahr)}€"]]))
                     ])
    return fig



if __name__ == "__main__":
    app.run_server(debug=True)
