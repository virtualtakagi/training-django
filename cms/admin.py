from django.contrib import admin
from cms.models import Channel, Live
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# admin.site.register(Channel)
# admin.site.register(live)

class ChannelResource(resources.ModelResource):
    # Modelに対するdjango-import-exportの設定
    class Meta:
        model = Channel


@admin.register(Channel)
class ChannelAdmin(ImportExportModelAdmin):
    # ImportExportModelAdminを利用する
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
