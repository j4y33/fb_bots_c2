from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, CampaignsMonitorFolders, CampaignsCommentLike


class CampaignsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name


class WherePublishCommentLikeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        camp = kwargs.pop('camp')
        super(WherePublishCommentLikeForm, self).__init__(*args, **kwargs)
        if camp is not None and camp != '':
            self.fields['select'].initial = camp
            try:
                all_fields = CampaignsCommentLike.objects.get(campaign_id=camp)
                self.fields['keywords'].initial = ",".join(all_fields.keywords)
                self.fields['exclude'].initial = ",".join(all_fields.exclude)
                self.fields['like_all_posts_in_history'].initial = all_fields.like_all_posts_in_history
            except CampaignsCommentLike.DoesNotExist:
                pass

    select = CampaignsChoiceField(queryset=Campaigns.objects.all(),
                                  empty_label="Select campaign",
                                  widget=forms.Select(attrs={"onChange":'this.form.submit();'}))
    keywords = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    like_all_posts_in_history = forms.BooleanField(required=False)