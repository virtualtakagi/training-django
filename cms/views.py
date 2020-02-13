from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from datetime import timedelta
# Create your views here.

from cms.models import live
from cms.models import Channel
from cms.forms import ChannelForm

def live_list(request):
    """Liveの一覧"""
    #return HttpResponse('ライブの一覧')
    now = datetime.now() - timedelta(hours=1)
    lives = live.objects.filter(starttime__gte=now).order_by('starttime')
    return render(request,'cms/live_list.html', {'lives': lives})


def channel_list(request):
    """Channelの一覧"""
    #return HttpResponse('ライブの一覧')
    ch = Channel.objects.all().order_by('id')
    return render(request,'cms/channel_list.html', {'channels': ch})


def channel_edit(request, channel_id=None):
    """Liveの編集"""
    #return HttpResponse('ライブの編集')
    if channel_id:   # live_id が指定されている (修正時)
        channelInstance = get_object_or_404(Channel, pk=channel_id)
    else:         # live_id が指定されていない (追加時)
        channelInstance = Channel()

    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=channelInstance)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            channelInstance = form.save(commit=False)
            channelInstance.save()
            return redirect('cms:channel_list')
    else:    # GET の時
        form = ChannelForm(instance=channelInstance)  # channel インスタンスからフォームを作成

    return render(request, 'cms/channel_edit.html', dict(form=form, channel_id=channel_id))


def channel_del(request, channel_id):
    """ライブの削除"""
    #return HttpResponse("ライブの削除")
    liveInstance = get_object_or_404(Channel, pk=channel_id)
    liveInstance.delete()
    return redirect('cms:channel_list')