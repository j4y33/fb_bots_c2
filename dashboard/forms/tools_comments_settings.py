from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, DestinationLists, Bots, CommentsSettings


class ToolsCommentsSettingsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dst_id = kwargs.pop('dst_id')
        super(ToolsCommentsSettingsForm, self).__init__(*args, **kwargs)
        if dst_id is not None and dst_id != '':
            try:
                all_fields = CommentsSettings.objects.get(dst_id=dst_id)
                self.fields['on_off'].initial = all_fields.on_off
                self.fields['wait_between_start'].initial = all_fields.wait_between_start
                self.fields['wait_between_end'].initial = all_fields.wait_between_end
                self.fields['execute_between_start'].widget.attrs = {'value': all_fields.execute_between_start}
                self.fields['execute_between_end'].widget.attrs = {'value': all_fields.execute_between_end}
                self.fields['random_sleep_time'].initial = all_fields.random_sleep_time
                self.fields['rotate_weekends_randomly'].initial = all_fields.rotate_weekends_randomly
                self.fields['comments_maximum_start'].initial = all_fields.comments_maximum_start
                self.fields['comments_maximum_end'].initial = all_fields.comments_maximum_end
                self.fields['comments_increasing_start'].initial = all_fields.comments_increasing_start
                self.fields['comments_increasing_end'].initial = all_fields.comments_increasing_end
                self.fields['maximum_single_source_per_day'].initial = all_fields.maximum_single_source_per_day
                self.fields['comments_single_source_maximum_start'].initial = all_fields.comments_single_source_maximum_start
                self.fields['comments_single_source_maximum_end'].initial = all_fields.comments_single_source_maximum_end
                self.fields['comments_post_maximum_age'].initial = all_fields.comments_post_maximum_age
                self.fields['comments_maximum_days'].initial = all_fields.comments_maximum_days
                self.fields['keywords'].initial = ",".join(all_fields.keywords)
                self.fields['exclude'].initial = ",".join(all_fields.exclude)
                self.fields['comment'].initial = all_fields.comment
                for day in all_fields.operate_on:
                    self.fields[day].initial = True

            except CommentsSettings.DoesNotExist as e:
                print(e)

    on_off = forms.BooleanField(required=False)
    wait_between_start = forms.IntegerField(min_value=0, required=False)
    wait_between_end = forms.IntegerField(min_value=0, required=False)
    execute_between_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '00:00'}))
    execute_between_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '23:59'}))
    random_sleep_time = forms.BooleanField(required=False)
    rotate_weekends_randomly = forms.BooleanField(required=False)
    MON = forms.BooleanField(required=False)
    TUE = forms.BooleanField(required=False)
    WED = forms.BooleanField(required=False)
    THU = forms.BooleanField(required=False)
    FRI = forms.BooleanField(required=False)
    SAT = forms.BooleanField(required=False)
    SUN = forms.BooleanField(required=False)

    comments_maximum_start = forms.IntegerField(min_value=0, required=False)
    comments_maximum_end = forms.IntegerField(min_value=0, required=False)
    comments_increasing_start = forms.IntegerField(min_value=0, required=False)
    comments_increasing_end = forms.IntegerField(min_value=0, required=False)

    maximum_single_source_per_day = forms.BooleanField(required=False)
    comments_single_source_maximum_start = forms.IntegerField(min_value=0, required=False)
    comments_single_source_maximum_end = forms.IntegerField(min_value=0, required=False)

    comments_post_maximum_age = forms.BooleanField(required=False)
    comments_maximum_days = forms.IntegerField(min_value=0, required=False)

    keywords = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))