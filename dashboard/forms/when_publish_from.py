from django import forms
from django.forms import ModelChoiceField
from dashboard.models import Campaigns, CampaignsScheduler


class CampaignsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.campaign_name


class WhenPublishForm(forms.Form):
    def __init__(self, *args, **kwargs):
        camp = kwargs.pop('camp')
        super(WhenPublishForm, self).__init__(*args, **kwargs)
        if camp is not None and camp != '':
            try:
                all_fields = CampaignsScheduler.objects.get(campaign_id=camp)
                self.fields['post_per_day'].initial = all_fields.posts_per_day
                self.fields['randomise_interval_each_day'].initial = all_fields.randomise_interval_each_day
                self.fields['randomise_number_of_posts'].initial = all_fields.randomise_number_of_posts
                self.fields['randomise_number_of_posts_maximum'].initial = all_fields.maximum_randomise_posts
                self.fields['wait'].initial = all_fields.wait
                self.fields['wait_seconds'].initial = all_fields.wait_before_publishing_with_same_account
                self.fields['rotate_weekdays_randomly'].initial = all_fields.rotate_weekdays_randomly
                self.fields['publish_time_start'].widget.attrs = {'value': all_fields.post_interval_start}
                self.fields['publish_time_end'].widget.attrs = {'value': all_fields.post_interval_finish}
                for day in all_fields.operate_on:
                    self.fields[day].initial = True
                #self.fields['randomise_number_of_posts_maximum'].initial = all_fields
                #self.fields['randomise_number_of_posts_maximum'].initial = all_fields.maximum_randomise_posts
                #self.fields['randomise_number_of_posts_maximum'].initial = all_fields.maximum_randomise_posts

            except CampaignsScheduler.DoesNotExist:
                pass
            self.fields['select'].initial = camp

    select = CampaignsChoiceField(queryset=Campaigns.objects.all(),
                                  empty_label="Select campaign",
                                  widget=forms.Select(attrs={"onChange" : 'this.form.submit();'}))
    publish_time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    publish_time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    post_per_day = forms.IntegerField(min_value=0, required=True)
    randomise_interval_each_day = forms.BooleanField(required=False)
    randomise_number_of_posts = forms.BooleanField(required=False)
    randomise_number_of_posts_maximum = forms.IntegerField(min_value=0, required=False)
    wait = forms.BooleanField(required=False)
    wait_seconds = forms.IntegerField(min_value=0, required=False)
    rotate_weekdays_randomly = forms.BooleanField(required=False)
    MON = forms.BooleanField(required=False)
    TUE = forms.BooleanField(required=False)
    WED = forms.BooleanField(required=False)
    THU = forms.BooleanField(required=False)
    FRI = forms.BooleanField(required=False)
    SAT = forms.BooleanField(required=False)
    SUN = forms.BooleanField(required=False)