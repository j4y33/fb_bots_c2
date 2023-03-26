from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, DestinationLists, Bots, ToolsAccountActions


class ToolsAccountActionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pass
        dst_id = kwargs.pop('dst_id')
        super(ToolsAccountActionForm, self).__init__(*args, **kwargs)
        if dst_id is not None and dst_id != '':
            try:
                all_fields = ToolsAccountActions.objects.get(dst_id=dst_id)
                self.fields['wait_between'].initial = all_fields.wait_between
                self.fields['wait_between_and'].initial = all_fields.wait_between_and
                self.fields['execute_between'].widget.attrs = {'value': all_fields.execute_between}
                self.fields['execute_between_and'].widget.attrs = {'value': all_fields.execute_between_and}
                self.fields['random_sleep_time'].initial = all_fields.random_sleep_time
                self.fields['rotate_weekdays_randomly'].initial = all_fields.rotate_weekdays_randomly
                self.fields['accept_per_login'].initial = all_fields.accept_per_login
                self.fields['auto_accept_friends'].initial = all_fields.auto_accept_friends
                self.fields['auto_like_news_feed_posts'].initial = all_fields.auto_like_news_feed_posts
                self.fields['auto_like_news_feed_posts_num'].initial = all_fields.auto_like_news_feed_posts_num
                self.fields['auto_like_news_feed_posts_keywords'].initial = all_fields.auto_like_news_feed_posts_keywords
                self.fields['auto_like_news_feed_posts_keywords_num'].initial = all_fields.auto_like_news_feed_posts_keywords_num
                self.fields['keywords'].initial = ",".join(all_fields.keywords)
                self.fields['exclude_keywords'].initial = ",".join(all_fields.exclude_keywords)
                self.fields['like_between_post_per_login'].initial = all_fields.like_between_post_per_login
                self.fields['like_between_post_per_login_and'].initial = all_fields.like_between_post_per_login_and
                self.fields['read_notifications_and_messages'].initial = all_fields.read_notifications_and_messages

                self.fields['high_percent'].initial = all_fields.high_percent
                self.fields['middle_percent'].initial = all_fields.middle_percent
                self.fields['low_percent'].initial = all_fields.low_percent

                self.fields['use_session_settings'].initial = all_fields.use_session_settings
                self.fields['long_session_time_min'].initial = all_fields.long_session_time_min
                self.fields['long_session_time_max'].initial = all_fields.long_session_time_max
                self.fields['medium_session_time_min'].initial = all_fields.medium_session_time_min
                self.fields['medium_session_time_max'].initial = all_fields.medium_session_time_max
                self.fields['short_session_time_min'].initial = all_fields.short_session_time_min
                self.fields['short_session_time_max'].initial = all_fields.short_session_time_max

                self.fields['short_time_min'].initial = all_fields.short_time_min
                self.fields['short_time_max'].initial = all_fields.short_time_max
                self.fields['medium_time_min'].initial = all_fields.medium_time_min
                self.fields['medium_time_max'].initial = all_fields.medium_time_max
                self.fields['long_time_min'].initial = all_fields.long_time_min
                self.fields['long_time_max'].initial = all_fields.long_time_max
                self.fields['use_engagement_levels'].initial = all_fields.use_engagement_levels
                self.fields['strong_time_min'].initial = all_fields.strong_time_min
                self.fields['strong_time_max'].initial = all_fields.strong_time_max
                self.fields['moderate_time_min'].initial = all_fields.moderate_time_min
                self.fields['moderate_time_max'].initial = all_fields.moderate_time_max
                self.fields['weak_time_min'].initial = all_fields.weak_time_min
                self.fields['weak_time_max'].initial = all_fields.weak_time_max
                for day in all_fields.operate_on:
                    self.fields[day].initial = True
            except ToolsAccountActions.DoesNotExist:
                pass

    wait_between = forms.IntegerField(min_value=0, required=False)
    wait_between_and = forms.IntegerField(min_value=0, required=False)
    execute_between = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '00:00'}))
    execute_between_and = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '23:59'}))
    random_sleep_time = forms.BooleanField(required=False)
    rotate_weekdays_randomly = forms.BooleanField(required=False)
    MON = forms.BooleanField(required=False)
    TUE = forms.BooleanField(required=False)
    WED = forms.BooleanField(required=False)
    THU = forms.BooleanField(required=False)
    FRI = forms.BooleanField(required=False)
    SAT = forms.BooleanField(required=False)
    SUN = forms.BooleanField(required=False)
    accept_per_login = forms.IntegerField(min_value=0, required=False)
    auto_accept_friends = forms.BooleanField(required=False)
    auto_like_news_feed_posts = forms.BooleanField(required=False)
    auto_like_news_feed_posts_num = forms.IntegerField(min_value=0, required=False)
    auto_like_news_feed_posts_keywords = forms.BooleanField(required=False)
    auto_like_news_feed_posts_keywords_num = forms.IntegerField(min_value=0, required=False)
    keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude_keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    like_between_post_per_login = forms.IntegerField(min_value=0, required=False)
    like_between_post_per_login_and = forms.IntegerField(min_value=0, required=False)
    read_notifications_and_messages = forms.BooleanField(required=False)
    # Percent of actions
    high_percent = forms.IntegerField(min_value=0, required=False)
    middle_percent = forms.IntegerField(min_value=0, required=False)
    low_percent = forms.IntegerField(min_value=0, required=False)
    # Session settings
    use_session_settings = forms.BooleanField(required=False)
    long_session_time_min = forms.IntegerField(min_value=0, required=False)
    long_session_time_max = forms.IntegerField(min_value=0, required=False)
    medium_session_time_min = forms.IntegerField(min_value=0, required=False)
    medium_session_time_max = forms.IntegerField(min_value=0, required=False)
    short_session_time_min = forms.IntegerField(min_value=0, required=False)
    short_session_time_max = forms.IntegerField(min_value=0, required=False)
    # Delays settings
    short_time_min = forms.IntegerField(min_value=0, required=False)
    short_time_max = forms.IntegerField(min_value=0, required=False)
    medium_time_min = forms.IntegerField(min_value=0, required=False)
    medium_time_max = forms.IntegerField(min_value=0, required=False)
    long_time_min = forms.IntegerField(min_value=0, required=False)
    long_time_max = forms.IntegerField(min_value=0, required=False)
    # engagement levels
    use_engagement_levels = forms.BooleanField(required=False)
    strong_time_min = forms.IntegerField(min_value=0, required=False)
    strong_time_max = forms.IntegerField(min_value=0, required=False)
    moderate_time_min = forms.IntegerField(min_value=0, required=False)
    moderate_time_max = forms.IntegerField(min_value=0, required=False)
    weak_time_min = forms.IntegerField(min_value=0, required=False)
    weak_time_max = forms.IntegerField(min_value=0, required=False)