from django import forms

from dashboard.models import ToolsFindGroups, ToolsFindPages


class ToolsFindPagesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dst_id = kwargs.pop('dst_id')
        super(ToolsFindPagesForm, self).__init__(*args, **kwargs)
        if dst_id is not None and dst_id != '':
            try:
                all_fields = ToolsFindPages.objects.get(dst_id=dst_id)
                self.fields['keywords'].initial = ",".join(all_fields.keywords)
                self.fields['exclude_keywords'].initial = ",".join(all_fields.exclude_keywords)
                self.fields['pages_extra_urls'].initial = ",".join(all_fields.pages_extra_urls)
                self.fields['min_likes'].initial = all_fields.min_likes
                self.fields['min_likes_count'].initial = all_fields.min_likes_count
                self.fields['en_gr_pages'].initial = all_fields.en_gr_pages
            except ToolsFindPages.DoesNotExist:
                pass
    keywords = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude_keywords = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    pages_extra_urls = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))
    min_likes = forms.BooleanField(required=False)
    en_gr_pages = forms.BooleanField(required=False)
    min_likes_count = forms.IntegerField(min_value=0, required=False)