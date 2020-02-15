from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta, time

from cms.models import Live, Channel
from cms.forms import ChannelForm
from . import getlive


def live_list(request):
    limit = datetime.now() - timedelta(hours=2)
    limit = limit.time()
    lives = Live.objects.filter(starttime__gte=limit).order_by('starttime')
    return render(request, 'cms/live_list.html', {'lives': lives})


def channel_list(request):
    ch = Channel.objects.all().order_by('id')
    return render(request, 'cms/channel_list.html', {'channels': ch})


def channel_edit(request, id=None):
    if id:   # 修正時
        channelInstance = get_object_or_404(Channel, pk=id)
    else:    # 追加時
        channelInstance = Channel()

    if request.method == 'POST':
        # POST された request データからフォームを作成
        form = ChannelForm(request.POST, instance=channelInstance)
        if form.is_valid():    # フォームのバリデーション
            channelInstance.save()
            return redirect('cms:channel_list')
    else:    # GET の時
        form = ChannelForm(instance=channelInstance)  # channel インスタンスからフォームを作成

    return render(request, 'cms/channel_edit.html', dict(form=form, id=id))


def channel_del(request, id):
    liveInstance = get_object_or_404(Channel, pk=id)
    liveInstance.delete()
    return redirect('cms:channel_list')


def getLiveStatus(request):
    channels = Channel.objects.all()

    for channel in channels:

        # 既に登録済みのライブ情報か
        if Live.objects.filter(channelid=channel.channelid).exists():

            channelObj = Live.objects.get(channelid=channel.channelid)

            # ライブステータスの確認
            status = getlive.updateLive(channelObj.videoid)

            if status != False:
                # 更新
                obj = Live.objects.filter(channelid=channel.channelid)
                obj.update(status=status)
                return redirect('cms:live_list')
            else:
                # ライブ終了なら削除
                channelObj.delete()
                return redirect('cms:live_list')
        else:
            # 新規追加
            liveInfo = getlive.getLive(channel.channelid)

            if liveInfo != False:
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
