import dash
import dash_html_components as html
import dash_core_components as dcc
import os

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
server.secret_key = os.environ.get('secret_key', 'secret')