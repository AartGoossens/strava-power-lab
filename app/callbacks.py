from urllib.parse import urlparse, parse_qs

import dash
import dash_html_components as html
from stravalib import Client
from stravalib.exc import AuthError

from . import settings, strava
from .layouts import app_layout, strava_login_layout
from .server import app


@app.callback(
    output=[
        dash.dependencies.Output('body', 'children'),
        dash.dependencies.Output('strava-auth', 'data')
    ],
    inputs=[
        dash.dependencies.Input('url', 'search'),
    ],
    state=[
        dash.dependencies.State('strava-auth', 'data')
    ]
)
def display_page(query_string, strava_auth):
    if strava_auth is None:
        strava_auth = {}

    body = strava_login_layout

    if strava_auth.get('authenticated', False):
        body = app_layout
    elif query_string is not None:
        query = parse_qs(str(query_string[1:]))
        if 'code' in query:
            strava_auth.update(strava.exchange_code_for_token(query['code']))
            strava_auth['authenticated'] = True
            body = app_layout

    return body, strava_auth


@app.callback(
    output=[
        dash.dependencies.Output('ride-dropdown', 'options'),
    ],
    inputs=[
        dash.dependencies.Input('strava-auth', 'data')
    ]
)
def ride_dropdown(strava_auth):
    activities = strava.get_activities(strava_auth)

    return [[{'label': a.name, 'value': a.id} for a in activities]]


@app.callback(
    output=[
        dash.dependencies.Output('segment-datatable', 'data'),
    ],
    inputs=[
        dash.dependencies.Input('ride-dropdown', 'value')
    ],
    state=[
        dash.dependencies.State('strava-auth', 'data')
    ]
)
def ride_dropdown(ride, strava_auth):
    activity = strava.get_activity(strava_auth, ride)

    segments = []
    for segment in activity.segment_efforts:
        segments.append({
            'segment_name': segment.segment.name,
            'segment_id': segment.segment.id,
            'distance': round(float(segment.distance)/1000, 2),
            'average_grade': float(segment.segment.average_grade),
            'elevation': int(round(float(segment.segment.elevation_high - segment.segment.elevation_low), 0)),
            'power': int(round(float(segment.average_watts), 0)),
        })

    return [segments]


@app.callback(
    output=[
        dash.dependencies.Output('results', 'children'),
    ],
    inputs=[
        dash.dependencies.Input('do-the-math-button', 'n_clicks')
    ],
    state=[
        dash.dependencies.State('segment-datatable', 'data'),
        dash.dependencies.State('segment-datatable', 'selected_rows')
    ]
)
def results(n_clicks, data, selected_rows):
    selected_rows = selected_rows or []
    return [[html.Div(data[i]['segment_name']) for i in selected_rows]]
