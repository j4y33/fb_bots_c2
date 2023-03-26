from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, DestinationLists, Bots


class CampaignsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name


class AccountChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.login


class WherePublishRSSForm(forms.Form):
    select = CampaignsChoiceField(queryset=Campaigns.objects.all(),
                                  empty_label="Select campaign",
                                  widget=forms.Select(attrs={"onChange":'this.form.submit();'}))
    scrap_share_name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude_keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    url_text_area = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))

    account_for_extract = AccountChoiceField(queryset=Bots.objects.filter(pk__in=Bots.objects.order_by('-creation_date')[:10].values_list('login')), empty_label="Select account")

    ignore_items_without_images = forms.BooleanField(required=False)
    posts_to_post_list = forms.BooleanField(required=False)
    extract_items = forms.IntegerField(min_value=0)
    scroll_up = forms.IntegerField(min_value=0)
    extract_hours = forms.IntegerField(min_value=0)