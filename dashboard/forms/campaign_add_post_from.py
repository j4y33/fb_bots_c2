import calendar

from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns


class CampaignsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name

class CampaignAddPost(forms.Form):
    post_text = forms.CharField(label='Add single post to queue:',
                                widget=forms.Textarea(attrs={'class': "form-control"}))
    published_by = forms.IntegerField(min_value=0)

    #if your options are coming from any model.it can be done by using a ModelChoiceField:
    select = CampaignsChoiceField(queryset=Campaigns.objects.all(), empty_label="Select campaign")
