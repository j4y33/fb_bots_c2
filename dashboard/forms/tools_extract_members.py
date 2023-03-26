from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, DestinationLists, Bots


class ToolsExtractMembersForm(forms.Form):
    # Get <span class="slider round"></span> status from DB
    # And all current settings
    url_text_area = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))
    scroll_limit = forms.IntegerField(min_value=0, required=False)
