from django.forms import ModelForm
from cms.models import Channel

class ChannelForm(ModelForm):
    """チャンネルの追加フォーム"""

    class Meta:
        model = Channel
        fields = ('channelid', 'channeltitle',)