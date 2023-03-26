from django import forms

from dashboard.models import ToolsFindGroups, ToolsFindFriends


class ToolsFindFriendsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dst_id = kwargs.pop('dst_id')
        super(ToolsFindFriendsForm, self).__init__(*args, **kwargs)
        if dst_id is not None and dst_id != '':
            try:
                all_fields = ToolsFindFriends.objects.get(dst_id=dst_id)
                self.fields['keywords'].initial = ",".join(all_fields.keywords)
                self.fields['exclude_keywords'].initial = ",".join(all_fields.exclude_keywords)
                self.fields['friends_extra_urls'].initial = ",".join(all_fields.friends_extra_urls)
                self.fields['min_mutual'].initial = all_fields.min_mutual
                self.fields['en_gr_friends'].initial = all_fields.en_gr_friends
                self.fields['opened_friends'].initial = all_fields.opened_friends
                self.fields['min_mutual_count'].initial = all_fields.min_mutual_count
            except ToolsFindFriends.DoesNotExist:
                pass
    keywords = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude_keywords = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    friends_extra_urls = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))
    min_mutual = forms.BooleanField(required=False)
    en_gr_friends = forms.BooleanField(required=False)
    opened_friends = forms.BooleanField(required=False)
    min_mutual_count = forms.IntegerField(min_value=0, required=False)