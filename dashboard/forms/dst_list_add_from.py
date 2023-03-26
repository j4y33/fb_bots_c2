from django import forms


class DestinationAddForm(forms.Form):
    dst_name = forms.CharField(label='List name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
