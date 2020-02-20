from cms.key import api
import json
import requests
import datetime
import dateutil.parser
import time
import pytz
import cssselect
import lxml.html
from requests.exceptions import Timeout
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# Access to YouTube Data API
def getLive(channelid):

    logger.debug('##### Start getLive #####')

    # Create Live URL
    channelurl = "https://www.youtube.com/channel/" + channelid
    liveurl = channelurl + "/live"

    # Get HTML Source
    logger.debug('Get HTML Source.')
    try:
        response = requests.get(liveurl, timeout=3.5).text
    except Timeout:
        logger.debug("JSON Request is TimeOut.")
        return False

    # Parse VideoID
    logger.debug('Parse VideoID...Channel ID: ' + channelid)

    target_html = lxml.html.fromstring(response)
    try:
        target_url = target_html.cssselect('meta[property="og:url"]')[0].get('content')
    except Exception:
        logger.debug("Illegal Response. Can't Get Status.")
        return False

    logger.debug("Get videourl : " + target_url)

    if target_url == liveurl[:-5]:
        logger.debug("Not Setting LiveStream : " + liveurl[:-5])
        return False
    else:
        target_url = target_html.cssselect('meta[property="og:image"]')[0].get('content')
    
    # split URL
    videoid_tmp = target_url.split('/')
    videoid = videoid_tmp[4]

    # concat videourl
    videourl = "https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id="
    videourl += videoid + "&key=" + api

    # Get JSON(Video)
    logger.debug('Get Video JSON... ID:' + videoid)
    try:
        response = requests.get(videourl, timeout=3.5)
        json = response.json()
    except Timeout:
        logger.debug("JSON Request is TimeOut.")
        return False

    # Check Response
    if response.status_code != 200:
        logger.debug("Bad Response!!! ")
        return False

    # Check Live Status / Check Offline
    if json['items'][0]['snippet']['liveBroadcastContent'] == 'none':
        logger.info('This Stream is Offline.')
        return False

    # Check Live Status
    if json['items'][0]['snippet']['liveBroadcastContent'] == 'live':
        live = {'thumbnail': json['items'][0]['snippet']['thumbnails']['default']['url'],
                'channelid': json['items'][0]['snippet']['channelId'],
                'videoid': videoid,
                'videotitle': json['items'][0]['snippet']['title'],
                'channeltitle': json['items'][0]['snippet']['channelTitle'],
                'starttime': json['items'][0]['liveStreamingDetails']['actualStartTime'],
                'status': "Live",
                'liveurl': liveurl,
                'channelurl': channelurl,
        }
    else:
        # Live Status [upcoming]
        live = {'thumbnail': json['items'][0]['snippet']['thumbnails']['default']['url'],
                'channelid': json['items'][0]['snippet']['channelId'],
                'videoid': videoid,
                'videotitle': json['items'][0]['snippet']['title'],
                'channeltitle': json['items'][0]['snippet']['channelTitle'],
                'starttime': json['items'][0]['liveStreamingDetails']['scheduledStartTime'],
                'status': "Upcoming",
                'liveurl': liveurl,
                'channelurl': channelurl,
                }

    # convert date iso8601 -> JST
    #JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    jst_timestamp = dateutil.parser.parse(
        live['starttime']).astimezone(pytz.timezone('Asia/Tokyo'))

    # Compare Date
    now = datetime.datetime.now(dateutil.tz.tzlocal())
    later = now + datetime.timedelta(hours=24)
    
    if jst_timestamp >= later:
        logger.debug("----- Invalid StartTime -----")
        return False
    
    live['starttime'] = jst_timestamp
     # convert datetime to time
    #live['starttime'] = jst_timestamp.strftime("%Y-%m-%d %H:%M")

    return live


def updateLive(videoid):

    logger.debug('##### Start updateLive #####')
    #channelid = "UCUc8GZfFxtmk7ZwSO7ccQ0g"
    videourl = "https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id="
    videourl += videoid + "&key=" + api

    # Get JSON(Video)
    logger.debug('Get Video JSON... ID:' + videoid)
    try:
        response = requests.get(videourl, timeout=3.5)
        json = response.json()
    except Timeout:
        logger.debug("JSON Request is TimeOut.")
        return False
    
    # Check Response
    if response.status_code != 200:
        logger.debug("Bad Response!!! ")
        return False

    # Check Live Status
    if json['items'][0]['snippet']['liveBroadcastContent'] == "none":
        logger.debug("This Stream is Offline.")
        return False
    
    # live 
    if json['items'][0]['snippet']['liveBroadcastContent'] == "live":
        startDateTime = json['items'][0]['liveStreamingDetails']['actualStartTime']
        startDateTime = datetime.datetime.fromisoformat(startDateTime[:-1])
        status = "Live"
    else:
        # upcoming or completed
        startDateTime = json['items'][0]['liveStreamingDetails']['scheduledStartTime']
        startDateTime = datetime.datetime.fromisoformat(startDateTime[:-1])
        status = "Upcoming"

    # Compare Date
    now = datetime.datetime.now()
    ago = now - datetime.timedelta(hours=12)
    if ago >= startDateTime:
        logger.debug("----- this live information is delete target -----")
        return False

    return status