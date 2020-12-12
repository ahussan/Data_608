import dash
import resources

app = dash.Dash(__name__, external_stylesheets=resources.external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True
