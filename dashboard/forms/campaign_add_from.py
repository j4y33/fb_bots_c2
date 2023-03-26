import calendar

from django import forms
from django.forms import ModelChoiceField

from dashboard.models import DestinationLists


class DstChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.dst_name


class CampaignAddForm(forms.Form):

    name = forms.CharField(label='Campaign name', max_length=100,
                           widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': "form-control"}))

    select = DstChoiceField(queryset=DestinationLists.objects.all(), empty_label="Select destination list")
    stop_account = forms.BooleanField(required=False)
    stop_publish = forms.BooleanField(required=False)
    stop_campaign = forms.BooleanField(required=False)
    # if your options are coming from any model.it can be done by using a ModelChoiceField:

    # select = forms.ModelChoiceField(queryset=ModelName.objects.all())
