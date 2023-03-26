from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, DestinationLists, Bots, CampaignsMonitorFolders


class CampaignsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name


class WherePublishMonitorFoldersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        camp = kwargs.pop('camp')
        super(WherePublishMonitorFoldersForm, self).__init__(*args, **kwargs)
        if camp is not None and camp != '':
            self.fields['select'].initial = camp
            try:
                all_fields = CampaignsMonitorFolders.objects.get(campaign_id=camp)
                self.fields['url_text_area'].initial = ",".join(all_fields.folders)
            except CampaignsMonitorFolders.DoesNotExist:
                pass

    select = CampaignsChoiceField(queryset=Campaigns.objects.all(),
                                  empty_label="Select campaign",
                                  widget=forms.Select(attrs={"onChange":'this.form.submit();'}))
    url_text_area = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))
    add_post_as_pending = forms.BooleanField(required=False)
    add_post_as_publishing = forms.BooleanField(required=False)