import dash
from dash import dcc, html
import os

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
server.secret_key = os.environ.get('secret_key', 'secret')