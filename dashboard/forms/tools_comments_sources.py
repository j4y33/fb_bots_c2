from django import forms
from django.forms import ModelChoiceField

from dashboard.models import Campaigns, DestinationLists, Bots, CommentsSources


class ToolsCommentsSourcesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dst_id = kwargs.pop('dst_id')
        super(ToolsCommentsSourcesForm, self).__init__(*args, **kwargs)
        if dst_id is not None and dst_id != '':
            try:
                all_fields = CommentsSources.objects.get(dst_id=dst_id)
                self.fields['comment_like_in_pages'].initial = all_fields.comment_like_in_pages
                self.fields['comment_like_in_walls'].initial = all_fields.comment_like_in_walls
                self.fields['comment_like_in_searches'].initial = all_fields.comment_like_in_searches
                self.fields['keywords'].initial = ",".join(all_fields.keywords)
                self.fields['exclude_keywords'].initial = ",".join(all_fields.exclude_keywords)
                self.fields['comment_like_in_groups'].initial = all_fields.comment_like_in_groups
                self.fields['comment_like_in_permalinks'].initial = all_fields.comment_like_in_permalinks
                self.fields['url_text_area'].initial = all_fields.url_text_area
            except CommentsSources.DoesNotExist as e:
                print(e)
    comment_like_in_pages = forms.BooleanField(required=False)
    comment_like_in_walls = forms.BooleanField(required=False)
    comment_like_in_searches = forms.BooleanField(required=False)
    keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    exclude_keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    comment_like_in_groups = forms.BooleanField(required=False)
    comment_like_in_permalinks = forms.BooleanField(required=False)
    url_text_area = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': 5, 'class': "form-control"}))