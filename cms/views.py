from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from cms.models import live


def live_list(request):
    """Liveの一覧"""
    #return HttpResponse('ライブの一覧')
    lives = live.objects.all()
    return render(request,'cms/live_list.html', {'lives': lives})


def live_edit(request, channelid=None):
    """Liveの編集"""
    return HttpResponse('ライブの編集')


def live_del(request, channelid):
    """ライブの削除"""
    return HttpResponse("ライブの削除")