from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta, time
from django.db.models import Q
from cms.models import Live, Channel
from cms.forms import ChannelForm
from . import getlive
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# Display Live Information
def live_list(request):
    limit = datetime.now() - timedelta(hours=2)
    limit = limit.time()

    # Query Set
    lives = Live.objects.filter(
        Q(starttime__gte=limit) |
        Q(status='Live')
    ).order_by('starttime')
    return render(request, 'cms/live_list.html', {'lives': lives})

# Display Channel List
def channel_list(request):
    ch = Channel.objects.all().order_by('id')
    return render(request, 'cms/channel_list.html', {'channels': ch})

# Edit Channel
def channel_edit(request, id=None):
    # Update
    if id:
        channelInstance = get_object_or_404(Channel, pk=id)
    # Create
    else:
        channelInstance = Channel()
    # Update
    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=channelInstance)
        # Validation Form
        if form.is_valid():
            channelInstance.save()
            return redirect('cms:channel_list')
    else:
        form = ChannelForm(instance=channelInstance)

    return render(request, 'cms/channel_edit.html', dict(form=form, id=id))

# Delete Channel
def channel_del(request, id):
    liveInstance = get_object_or_404(Channel, pk=id)
    liveInstance.delete()
    return redirect('cms:channel_list')

# Manual Execute , Request Live Status
def getLiveStatus(request):
    channels = Channel.objects.all()

    for channel in channels:

        # Check Exists Record
        if Live.objects.filter(channelid=channel.channelid).exists():

            # Get Channel Record
            channelObj = Live.objects.get(channelid=channel.channelid)

            # Get Live Status
            status = getlive.updateLive(channelObj.videoid)

            if status != False:
                # Update
                obj = Live.objects.filter(channelid=channel.channelid)
                obj.update(status=status)
                logger.debug("Update Record: " + channel.channeltitle + ", " + "Status: " + status)

            else:
                # Delete
                channelObj.delete()
                logger.debug("Delete Live: " + channel.channeltitle)

        else:
            # Create
            liveInfo = getlive.getLive(channel.channelid)

            if liveInfo != False:
                logger.debug("##### Create Record: " + liveInfo['channeltitle'] + " #####")
                info, created = Live.objects.update_or_create(
                    thumbnail=liveInfo['thumbnail'],
                    channelid=liveInfo['channelid'],
                    videoid=liveInfo['videoid'],
                    videotitle=liveInfo['videotitle'],
                    channeltitle=liveInfo['channeltitle'],
                    starttime=liveInfo['starttime'],
                    status=liveInfo['status'],
                    liveurl=liveInfo['liveurl'],
                    channelurl=liveInfo['channelurl']
                )

    return redirect('cms:live_list')


# Cron Request Live Status
def batchGetLiveStatus():
    channels = Channel.objects.all()

    for channel in channels:

        # Check Exists Record
        if Live.objects.filter(channelid=channel.channelid).exists():

            # Get Channel Record
            channelObj = Live.objects.get(channelid=channel.channelid)

            # Get Live Status
            status = getlive.updateLive(channelObj.videoid)

            if status != False:
                # Update
                obj = Live.objects.filter(channelid=channel.channelid)
                obj.update(status=status)
                logger.debug("Update Record: " + channel.channeltitle + ", " + "Status: " + status)

            else:
                # Delete
                channelObj.delete()
                logger.debug("Delete Live: " + channel.channeltitle)

        else:
            # Create
            liveInfo = getlive.getLive(channel.channelid)

            if liveInfo != False:
                logger.debug("##### Create Record: " + liveInfo['channeltitle'] + " #####")
                info, created = Live.objects.update_or_create(
                    thumbnail=liveInfo['thumbnail'],
                    channelid=liveInfo['channelid'],
                    videoid=liveInfo['videoid'],
                    videotitle=liveInfo['videotitle'],
                    channeltitle=liveInfo['channeltitle'],
                    starttime=liveInfo['starttime'],
                    status=liveInfo['status'],
                    liveurl=liveInfo['liveurl'],
                    channelurl=liveInfo['channelurl']
                )

    return redirect('cms:live_list')