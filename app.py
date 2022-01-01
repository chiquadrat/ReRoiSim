import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)
server = app.server
#app.config.suppress_callback_exceptions = True