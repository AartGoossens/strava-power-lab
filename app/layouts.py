import dash_table
import dash_core_components as dcc
import dash_html_components as html
from stravalib import Client

from . import settings
from .server import app


app.layout = html.Div([
    dcc.Store(id='strava-auth', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    html.H1(children='Strava Power Lab'),
    html.Hr(),
    html.Div(id='body')
])


client = Client()
strava_authorization_url = client.authorization_url(
    client_id=settings.STRAVA_CLIENT_ID,
    redirect_uri=settings.APP_URL,
    state='strava-dash-app'
)

strava_login_layout= html.Div([
    html.A(
        html.Img(src='static/btn_strava_connectwith_orange.png'),
        'Connect with Strava',
        href=strava_authorization_url
    )
])


app_layout = html.Div([
    html.P('Select Ride and segments'),
    dcc.Dropdown(id='ride-dropdown'),
    html.Br(),
    dash_table.DataTable(
        id='segment-datatable',
        columns=[
            {"name": 'Segment Name', "id": 'segment_name'},
            {"name": 'Segment ID', "id": 'segment_id'},
            {"name": 'Distance (km)', "id": 'distance'},
            {"name": 'Average Grade (%)', "id": 'average_grade'},
            {"name": 'Elevation (m)', "id": 'elevation'},
            {"name": 'Power (Watt)', "id": 'power'},
        ],
        filter_action="native",
        sort_action="native",
        sort_by=[{'column_id': 'elevation', 'direction': 'desc'}],
        row_selectable="multi",
        page_action="native",
        page_current= 0,
        page_size= 20,
    ),
    html.Hr(),
    html.Button('Do the math!', id='do-the-math-button'),
    html.Hr(),
    html.Div(id='results'),
])
