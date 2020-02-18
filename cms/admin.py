from django.contrib import admin
from cms.models import Channel, Live
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ChannelResource(resources.ModelResource):
    # Setting Django-import-export for Model
    class Meta:
        model = Channel


@admin.register(Channel)
class ChannelAdmin(ImportExportModelAdmin):
    # Using ImportExportModelAdmin
    ordering = ['id']
    list_display = ('id','channelid', 'channeltitle')


# class ChannelAdmin(admin.ModelAdmin):
#     list_display = ('channelid', 'channeltitle')
#     list_display_links = ('channelid', 'channeltitle')


# admin.site.register(Channel, ChannelAdmin)


class LiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'channelid', 'videoid', 'videotitle',
                    'channeltitle', 'starttime', 'status', 'channelurl', 'liveurl')


admin.site.register(Live, LiveAdmin)
