import requests
import json
import re


def parse_duration(duration_str):

    hours = 0
    minutes = 0
    seconds = 0

    results = re.search(r'([0-9]+)H', duration_str)
    if results:
        hours = int(results.group(1))
    results = re.search(r'([0-9]+)M', duration_str)
    if results:
        minutes = int(results.group(1))
    results = re.search(r'([0-9]+)S', duration_str)
    if results:
        seconds = int(results.group(1))

    return (hours, minutes, seconds)


def get_video_data(video_id):
    url_fmt = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={}&maxResults=5&key=AIzaSyBCl1ISMSqqIe9ajFkfIBwdTx1horJFI8Q'
    data = requests.get(url_fmt.format(video_id)).text
    data = json.loads(data)
    if len(data['items']) == 0:
        return None

    vid = data['items'][0]
    duration = parse_duration(vid['contentDetails']['duration'])
    return {
        'title': vid['snippet']['title'],
        'duration': duration,
    }


def extract_yt_ids(msg):
    vidz = []
    pattern = r'https?://www.youtube.com/watch\?v=([_0-9a-zA-Z-]+)'
    vidz.extend(re.findall(pattern, msg))
    pattern = r'https?://youtu.be/([_0-9a-zA-Z-]+)'
    vidz.extend(re.findall(pattern, msg))
    return vidz
