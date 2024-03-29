import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
import app_mieten_vs_kaufen, app_immo_kapitalanlage

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1('Simuliers!'),
    dcc.Link('Immobilienrendite', href='/app_immo_kapitalanlage'),
    html.Br(),
    dcc.Link('Mieten vs. Kaufen', href='/app_mieten_vs_kaufen'),
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/app_immo_kapitalanlage':
        return app_immo_kapitalanlage.layout
    if pathname == '/app_mieten_vs_kaufen':
        return app_mieten_vs_kaufen.layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)