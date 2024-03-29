import dash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    requests_pathname_prefix='/'
)


app.title = 'Strava Power Lab'
app.config.suppress_callback_exceptions = True
