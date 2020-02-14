import json
import requests
import datetime
import dateutil.parser
import time
import pytz
from cms.key import api

# Access for YouTube Data API


def getLive(channelid):

    # channelid = "UCd9BXPj-KcMTh0HiB-Vlb8A"
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=upcoming&channelId="
    url += channelid + "&key=" + api

    # Get JSON(Channel)
    response = requests.get(url)
    json = response.json()

    # Get VideoID
    videoid = json['items'][0]['id']['videoId']

    videourl = "https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id="
    videourl += videoid + "&key=" + api

    # Get JSON(Video)
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
            'boolean' : True
            }

    # convert iso8601 -> JST
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    jst_timestamp = dateutil.parser.parse(
        live['starttime']).astimezone(JST)

    # check date
    now = datetime.date.today()
    startdate = jst_timestamp.date()
    if now != startdate:
        live['boolean'] = False

    # convert datetime to time
    live['starttime'] = jst_timestamp.strftime("%H:%M")

    # for i,v in live.items():
    #     print (i,v)

    return live
