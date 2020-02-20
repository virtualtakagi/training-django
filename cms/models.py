from django.db import models


class Channel(models.Model):
    # Channel Table
    channelid = models.CharField("channelid", max_length=255, unique=True)
    channeltitle = models.CharField("title", max_length=255, unique=True)


class Live(models.Model):
    # Live Table
    thumbnail = models.CharField("thumbnail", max_length=255)
    channelid = models.CharField("channelid", max_length=255)
    videoid = models.CharField("videoid", max_length=255, unique=True)
    videotitle = models.CharField("videotitle", max_length=255)
    channeltitle = models.CharField("channeltitle", max_length=255)
    starttime = models.DateTimeField("starttime")
    status = models.CharField("status", max_length=10)
    liveurl = models.CharField("liveurl",max_length=255)
    channelurl = models.CharField("channelurl",max_length=255)
