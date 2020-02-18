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

    logger.debug('Start getLive...')

    # channelid = "UCd9BXPj-KcMTh0HiB-Vlb8A"
    # url = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=upcoming&channelId="
    # url += channelid + "&key=" + api

    # Get JSON(Channel)
    # logger.debug('Get Channel JSON... ID:' + channelid)
    # try:
    #     response = requests.get(url, timeout=3.5)
    #     json = response.json()
    # except Timeout:
    #     logger.debug("JSON Request is TimeOut.")
    #     return False

    # # Check Response
    # if response.status_code != 200:
    #     logger.debug("Bad Response!!! ")
    #     return False


    # Get VideoID
    # if len(json['items']) == 0:
    #     logger.debug("This Channel is not upcoming")
    #     return False

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
    logger.debug('Parse VideoID...')
    # try:

    target_html = lxml.html.fromstring(response)
    target_url = target_html.cssselect('meta[property="og:url"]')[0].get('content')
    
    logger.debug("Get videourl : " + target_url)
    # except Exception:
    #     logger.debug('VideoID Parse Failed.')
    #     return False
    
    # videoid = json['items'][0]['id']['videoId']

    if target_url == liveurl or len(target_url[32:]) > 10:
        logger.debug('This live is Offline')
        return False
    
    videoid = target_url[32:]
    
    logger.debug("concat id: " + videoid)
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