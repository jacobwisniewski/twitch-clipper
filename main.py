from config import config
import requests
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlretrieve
from time import sleep
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Take the config variables from the config.py file
CLIENT_ID = config['CLIENT_ID']
GAME_ID = config['GAME_ID']
DOWNLOAD_DIR = config['DOWNLOAD_DIR']


def get_recent_top_clips_data(game_id):
    """A function that gets the last days top clips from a specific game"""
    # started_at variable will be one day before, while ended_at time will be
    # the current time
    end_time = datetime.now(timezone.utc).astimezone()
    start_time = datetime.now(timezone.utc).astimezone() - timedelta(days=1)

    url = 'https://api.twitch.tv/helix/clips'
    params = {
        'game_id': '33214',  # Game ID can be set to other games
        'first': 10,  # Number of clips returned
        'started_at': start_time.isoformat(),
        'ended_at': end_time.isoformat()

    }
    headers = {
        'Client-ID': CLIENT_ID
    }
    response = requests.get(url, params=params, headers=headers).json()
    return response


def get_clip_download_url(clip):
    """Scraps the clip download url"""
    driver = webdriver.Chrome('/files/chromedriver/chromedriver.exe')
    driver.get(clip['url'])
    sleep(2)

    soup = BeautifulSoup(driver.page_source, "html5lib")
    url = soup.find('video')['src']
    driver.quit()

    return url


def download_clip_batch(clip_data):
    """Downloads all clips given in a clip data json"""
    # Create a new folder to store clips in
    new_path = f'/files/twitch/{datetime.today().strftime("%Y-%m-%d")}'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    # Download each clip into folder
    for clip in clip_data['data']:
        # If clip has been downloaded do not re-download
        current_date = datetime.today().strftime("%Y-%m-%d")
        download_path = f'{DOWNLOAD_DIR}{current_date}/{clip["id"]}.mp4'
        if not os.path.exists(download_path):
            download_url = get_clip_download_url(clip)
            print(f'Downloading {clip["id"]}...')
            urlretrieve(download_url, download_path)


def combine_clip_batch():
    """Combines all downloaded clips into one"""
    # Create a VideoFileClip object for each file in the date folder
    clip_dir = f'/files/twitch/{datetime.today().strftime("%Y-%m-%d")}'
    video_clips = []
    i = 0
    for clip in os.listdir(clip_dir):
        if i == 5:
            break
        video_clips.append(VideoFileClip(f'{clip_dir}/{clip}').resize((1280,720)))
        i += 1
    combined_clip = concatenate_videoclips(video_clips, method='compose')
    combined_clip.write_videofile(f'{clip_dir}.mp4')


def main():
    """The main function that structures the pre-scraping, downloading and
    merging"""
    clip_data = get_recent_top_clips_data(GAME_ID)
    download_clip_batch(clip_data)
    combine_clip_batch()


if __name__ == '__main__':
    main()
