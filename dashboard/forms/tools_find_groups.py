from django import forms

from dashboard.models import ToolsFindGroups


class ToolsFindGroupsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dst_id = kwargs.pop('dst_id')
        super(ToolsFindGroupsForm, self).__init__(*args, **kwargs)
        if dst_id is not None and dst_id != '':
            try:
                all_fields = ToolsFindGroups.objects.get(dst_id=dst_id)
                self.fields['keywords'].initial = ",".join(all_fields.keywords)
                self.fields['exclude_keywords'].initial = ",".join(all_fields.exclude_keywords)
                self.fields['groups_extra_urls'].initial = ",".join(all_fields.groups_extra_urls)
                self.fields['min_users'].initial = all_fields.min_users
                self.fields['en_gr_groups'].initial = all_fields.en_gr_groups
                self.fields['opened_groups'].initial = all_fields.opened_groups
                self.fields['admin_post'].initial = all_fields.admin_post
                self.fields['min_users_count'].initial = all_fields.min_users_count
            except ToolsFindGroups.DoesNotExist:
                pass
    keywords = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude_keywords = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    groups_extra_urls = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))
    min_users = forms.BooleanField(required=False)
    en_gr_groups = forms.BooleanField(required=False)
    opened_groups = forms.BooleanField(required=False)
    admin_post = forms.BooleanField(required=False)
    min_users_count = forms.IntegerField(min_value=0, required=False)