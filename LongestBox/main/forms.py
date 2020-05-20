from django import forms
from django.forms import ModelForm
from main.models import Box, Comic

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class CreateNewBox(ModelForm):
    class Meta:
        model = Box
        fields = ["name", "sImg"]


class DateInput(forms.DateInput):
    input_type = "date"


class CreateNewComic(ModelForm):
    class Meta:
        model = Comic
        fields = [
            "box",
            "publisher",
            "name",
            "number",
            "variant",
            "date",
            "condition",
            "owned",
            "sImg",
        ]
        widgets = {
            "date": DateInput(),
        }
