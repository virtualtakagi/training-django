from django.contrib import admin
from cms.models import Channel, Live

# Register your models here.
#admin.site.register(Channel)
#admin.site.register(live)


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('channelid', 'channeltitle')
    list_display_links = ('channelid', 'channeltitle')


admin.site.register(Channel,ChannelAdmin)


class LiveAdmin(admin.ModelAdmin):
    list_display = ('id','thumbnail', 'channelid', 'videoid', 'videotitle', 'channeltitle', 'starttime', 'status', 'channelurl', 'liveurl')


admin.site.register(Live, LiveAdmin)
