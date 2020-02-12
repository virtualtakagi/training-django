from django.db import models

# Create your models here.
class Channel(models.Model):
    # チャンネル情報
    channelid = models.CharField("channelid", max_length=255)
    channeltitle = models.CharField("title", max_length=255)

    # def __str__(self):
    #     return self.channeltitle


class live(models.Model):
    # ライブ情報
    thumbnail = models.CharField("thumbnail", max_length=255)
    channelid = models.CharField("channelid", max_length=255)
    videoid = models.CharField("videoid", max_length=255)
    videotitle = models.CharField("videotitle", max_length=255)
    channeltitle = models.CharField("channeltitle", max_length=255)
    starttime = models.DateTimeField("starttime")
    status = models.CharField("status", max_length=10)
    liveurl = models.CharField("liveurl",max_length=255)
    channelurl = models.CharField("channelurl",max_length=255)

    # def __str__(self):
    #     return self.videotitle