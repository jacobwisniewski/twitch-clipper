from config import config
import requests
from datetime import datetime, timezone, timedelta

# Take the config variables from the config.py file
CLIENT_ID = config['CLIENT_ID']


def get_recent_top_clips_data(game_id):
    """A function that gets the last days top clips from a specific game"""
    # started_at variable will be one day before, while ended_at time will be
    # the current time
    end_time = datetime.now(timezone.utc).astimezone()
    start_time = datetime.now(timezone.utc).astimezone() - timedelta(days=1)

    url = 'https://api.twitch.tv/helix/clips'
    params = {
        'game_id': '33214',  # Game ID can be set to other games
        'first': 20,  # Number of clips returned
        'started_at': start_time.isoformat(),
        'ended_at': end_time.isoformat()

    }
    headers = {
        'Client-ID': CLIENT_ID
    }
    response = requests.get(url, params=params, headers=headers).json()
    return response

