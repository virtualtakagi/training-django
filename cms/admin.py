from django.contrib import admin
from cms.models import Channel, live

# Register your models here.
#admin.site.register(Channel)
#admin.site.register(live)


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('channelid', 'channeltitle')
    list_display_links = ('channelid', 'channeltitle')


admin.site.register(Channel,ChannelAdmin)


class liveAdmin(admin.ModelAdmin):
    list_display = ('channelid', 'videoid', 'videotitle', 'channeltitle', 'starttime')


admin.site.register(live, liveAdmin)
