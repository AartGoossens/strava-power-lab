from stravalib import Client
from stravalib.exc import AccessUnauthorized

from . import settings


def create_client(strava_auth=None):
    if strava_auth is None:
        return Client()
    else:
        return Client(strava_auth['access_token'])


def exchange_code_for_token(code):
    client = create_client()
    return client.exchange_code_for_token(
        client_id=settings.STRAVA_CLIENT_ID,
        client_secret=settings.STRAVA_CLIENT_SECRET,
        code=code
    )


def refresh_access_token(refresh_token):
    client = Client()
    return client.refresh_access_token(
        client_id=settings.STRAVA_CLIENT_ID,
        client_secret=settings.STRAVA_CLIENT_SECRET,
        refresh_token=refresh_token
    )


def get_activities(strava_auth):
    client = create_client(strava_auth)
    try:
        return list(client.get_activities(limit=10))
    except AccessUnauthorized:
        strava_auth = refresh_access_token(strava_auth['refresh_token'])
        return get_activities(strava_auth)


def get_activity(strava_auth, ride):
    client = create_client(strava_auth)
    try:
        return client.get_activity(ride)
    except AccessUnauthorized:
        strava_auth = refresh_access_token(strava_auth['refresh_token'])
        return get_activity(strava_auth, ride)
