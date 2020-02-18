from django.forms import ModelForm
from cms.models import Channel

class ChannelForm(ModelForm):
# Add Channel

    class Meta:
        model = Channel
        fields = ('channelid', 'channeltitle',)