from cms.key import api
import json
import requests
import datetime
import dateutil.parser
import time
import pytz
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# Access for YouTube Data API


def getLive(channelid):

    logger.debug('Start getLive...')

    # channelid = "UCd9BXPj-KcMTh0HiB-Vlb8A"
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=upcoming&channelId="
    url += channelid + "&key=" + api

    # Get JSON(Channel)
    logger.debug('Get Channel JSON... ID:' + channelid)
    response = requests.get(url)
    json = response.json()

    # Get VideoID
    videoid = json['items'][0]['id']['videoId']

    videourl = "https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id="
    videourl += videoid + "&key=" + api

    # Get JSON(Video)
    logger.debug('Get Video JSON... ID:' + videoid)
    response = requests.get(videourl)
    json = response.json()

    channelurl = "https://www.youtube.com/channel/" + channelid
    liveurl = channelurl + "/live"

    # Create live
    live = {'thumbnail': json['items'][0]['snippet']['thumbnails']['default']['url'],
            'channelid': json['items'][0]['snippet']['channelId'],
            'videoid': videoid,
            'videotitle': json['items'][0]['snippet']['title'],
            'channeltitle': json['items'][0]['snippet']['channelTitle'],
            'starttime': json['items'][0]['liveStreamingDetails']['scheduledStartTime'],
            'status': "upcoming",
            'liveurl': liveurl,
            'channelurl': channelurl,
            }

    # convert iso8601 -> JST
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    jst_timestamp = dateutil.parser.parse(
        live['starttime']).astimezone(JST)

    # check date
    today = datetime.date.today()
    startdate = jst_timestamp.date()
    if today != startdate:
        return False

    # convert datetime to time
    live['starttime'] = jst_timestamp.strftime("%H:%M")

    logger.debug('Return Live Object.')

    return live


def updateLive(videoid):

    logger.debug('Start updateLive...')
    #channelid = "UCUc8GZfFxtmk7ZwSO7ccQ0g"
    videourl = "https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id="
    videourl += videoid + "&key=" + api

    # Get JSON(Video)
    logger.debug('Get Video JSON... ID:' + videoid)
    response = requests.get(videourl)
    json = response.json()

    # Check Date
    live = json['items'][0]['liveStreamingDetails']['scheduledStartTime']
    live = datetime.datetime.fromisoformat(live[:-1])

    # Compare Date
    today = datetime.date.today()
    startdate = live.date()
    if today != startdate:
        logger.debug("this live information is delete target.")
        return False

    # Check Live Status
    if json['items'][0]['snippet']['liveBroadcastContent'] != "none":
        logger.info('Return Live Status.')
        return json['items'][0]['snippet']['liveBroadcastContent']


    return False
