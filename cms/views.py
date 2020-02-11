from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from cms.models import live


def live_list(request):
    """Liveの一覧"""
    #return HttpResponse('ライブの一覧')
    return render(request,'cms/live_list.html', {'lives': live.objects.all()})


def live_edit(request, channelid=None):
    """Liveの編集"""
    return HttpResponse('ライブの編集')


def live_del(request, channelid):
    """ライブの削除"""
    return HttpResponse("ライブの削除")