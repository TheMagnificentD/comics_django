from django import forms
from django.forms import ModelForm
from main.models import Box, Comic


class CreateNewBox(ModelForm):
    class Meta:
        model = Box
        fields = ["name", "sImg"]


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
