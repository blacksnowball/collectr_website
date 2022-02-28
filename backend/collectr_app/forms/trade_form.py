from django import forms
import uuid
from datetime import datetime


class TradeCreateForm(forms.Form):
    description = forms.CharField(label='Description', widget=forms.Textarea, max_length=3500)
    condition = forms.CharField(label='Condition', widget=forms.Textarea, max_length=500)


class TradeSearchForm(forms.Form):
    title = forms.CharField()
