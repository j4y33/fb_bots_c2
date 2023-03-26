from django import forms
from django.forms import ModelChoiceField
from dashboard.models import Campaigns, DestinationLists, Bots, ToolsJoiner


class ToolsJoinerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dst_id = kwargs.pop('dst_id')
        super(ToolsJoinerForm, self).__init__(*args, **kwargs)
        if dst_id is not None and dst_id != '':
            try:
                all_fields = ToolsJoiner.objects.get(dst_id=dst_id)
                self.fields['wait_between'].initial = all_fields.wait_between
                self.fields['wait_between_and'].initial = all_fields.wait_between_and
                self.fields['execute_between'].widget.attrs = {'value': all_fields.execute_between}
                self.fields['execute_between_and'].widget.attrs = {'value': all_fields.execute_between_and}
                self.fields['random_sleep_time'].initial = all_fields.random_sleep_time
                self.fields['join_between'].initial = all_fields.join_between
                self.fields['join_between_and'].initial = all_fields.join_between_and
                self.fields['auto_stop'].initial = all_fields.auto_stop
                self.fields['reaching_groups'].initial = all_fields.reaching_groups
                self.fields['join_between_peer_day'].initial = all_fields.join_between_peer_day
                self.fields['join_between_and_peer_day'].initial = all_fields.join_between_and_peer_day
                self.fields['auto_stop_peer_day'].initial = all_fields.auto_stop_peer_day
                self.fields['reaching_groups_peer_day'].initial = all_fields.reaching_groups_peer_day
                for day in all_fields.operate_on:
                    self.fields[day].initial = True
            except ToolsJoiner.DoesNotExist:
                pass

    wait_between = forms.IntegerField(min_value=0, required=False)
    wait_between_and = forms.IntegerField(min_value=0, required=False)
    execute_between = forms.TimeField(required=False, widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '00:00'}))
    execute_between_and = forms.TimeField(required=False, widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '23:59'}))
    random_sleep_time = forms.BooleanField(required=False)
    MON = forms.BooleanField(required=False)
    TUE = forms.BooleanField(required=False)
    WED = forms.BooleanField(required=False)
    THU = forms.BooleanField(required=False)
    FRI = forms.BooleanField(required=False)
    SAT = forms.BooleanField(required=False)
    SUN = forms.BooleanField(required=False)

    join_between = forms.IntegerField(min_value=0, required=False)
    join_between_and = forms.IntegerField(min_value=0, required=False)
    auto_stop = forms.BooleanField(required=False)
    reaching_groups = forms.IntegerField(min_value=0, required=False)

    join_between_peer_day = forms.IntegerField(min_value=0, required=False)
    join_between_and_peer_day = forms.IntegerField(min_value=0, required=False)
    auto_stop_peer_day = forms.BooleanField(required=False)
    reaching_groups_peer_day = forms.IntegerField(min_value=0, required=False)