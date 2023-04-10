from django import forms
from .models import indexetfmanage


class FundForm(forms.ModelForm):
    class Meta:
        model = indexetfmanage
        fields = [
            "indexName",
            "fundType",
        ]
