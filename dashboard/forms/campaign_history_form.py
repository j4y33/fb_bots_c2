from django import forms
from django.forms import ModelChoiceField
from dashboard.models import Campaigns


class CampaignsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name


class HistoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        camp = kwargs.pop('camp')
        super(HistoryForm, self).__init__(*args, **kwargs)
        if camp is not None and camp != '':
            self.fields['select'].initial = camp

    select = CampaignsChoiceField(queryset=Campaigns.objects.all(),
                                  empty_label="Select campaign",
                                  widget=forms.Select(attrs={"onChange" : 'this.form.submit();'}))