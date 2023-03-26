from django import forms


class ToolsCreateGroupForm(forms.Form):

    group_name = forms.CharField(label='Group name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
