from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, DestinationLists, Bots


class ToolsUseMembersForm(forms.Form):
    # Get <span class="slider round"></span> status from DB
    # And all current settings
    wait_between = forms.IntegerField(min_value=0, required=False)
    wait_between_and = forms.IntegerField(min_value=0, required=False)

    execute_between = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '00:00'}))
    execute_between_and = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '23:59'}))

    random_sleep_time = forms.BooleanField(required=False)
    rotate_weekdays_randomly = forms.BooleanField(required=False)
    ignore_existing_friends = forms.BooleanField(required=False)
    maximum_requests_per_login = forms.BooleanField(required=False)
    maximum_requests_per_login_num = forms.IntegerField(min_value=0, required=False)

    MON = forms.BooleanField(required=False)
    TUE = forms.BooleanField(required=False)
    WED = forms.BooleanField(required=False)
    THU = forms.BooleanField(required=False)
    FRI = forms.BooleanField(required=False)
    SAT = forms.BooleanField(required=False)
    SUN = forms.BooleanField(required=False)

    message_text_area = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))
    message_ignore_existing_friends = forms.BooleanField(required=False)
    message_ignore_users_invite = forms.BooleanField(required=False)