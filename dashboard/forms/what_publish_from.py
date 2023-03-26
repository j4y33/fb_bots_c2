from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, CampaignsScrapAndSharePosts


class CampaignsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name


class AccountChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.login


class WhatPublishForm(forms.Form):
    def __init__(self, *args, **kwargs):
        camp = kwargs.pop('camp')
        super(WhatPublishForm, self).__init__(*args, **kwargs)
        if camp is not None and camp != '':
            self.fields['select'].initial = camp
            try:
                all_fields = CampaignsScrapAndSharePosts.objects.get(campaign_id=camp)
                self.fields['process_name'].initial = all_fields.process_name
                self.fields['keywords'].initial = all_fields.keywords
                self.fields['exclude_keywords'].initial = all_fields.exclude_keywords
                self.fields['url'].initial = all_fields.url
                self.fields['ignore_items_without_images'].initial = all_fields.ignore_items_without_images
                self.fields['maximum_posts'].initial = all_fields.maximum_posts
                self.fields['post_text'].initial = all_fields.post_text
            except CampaignsScrapAndSharePosts.DoesNotExist:
                pass

    select = CampaignsChoiceField(queryset=Campaigns.objects.all(),
                                  empty_label="Select campaign",
                                  widget=forms.Select(attrs={"onChange" : 'this.form.submit();'}))

    process_name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude_keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    url = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))

    ignore_items_without_images = forms.BooleanField(required=False)
    maximum_posts = forms.IntegerField(min_value=0)
    post_text = forms.CharField(required=False, label='Add text to post:',
                                widget=forms.Textarea(attrs={'class': "form-control"}))