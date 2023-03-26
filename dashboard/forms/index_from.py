import calendar

from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns


class CampaignsChoiceFieldIndex(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name


class IndexForm(forms.Form):
    select = CampaignsChoiceFieldIndex(queryset=Campaigns.objects.all(), empty_label="Select campaign")
