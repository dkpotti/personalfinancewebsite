from django import forms
from .models import stockmanage


class StockForm(forms.ModelForm):
    class Meta:
        model = stockmanage
        fields = [
            "symbol",
            "sharePriceBought",
            "numberOfShares",
            "dividendAmount",
            "dividendPercentage",
            "shareBoughtDate",
        ]
