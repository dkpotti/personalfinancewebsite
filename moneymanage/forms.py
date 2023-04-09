from django import forms
from .models import moneymanage


class CashForm(forms.ModelForm):
    class Meta:
        cash_type_options = (
            ("Certificate Deposit", "Certificate Deposit"),
            ("T Bills", "T Bills"),
            ("I Bonds", "I Bonds"),
        )
        model = moneymanage
        fields = [
            "cashName",
            "cashType",
            "cashAmount",
            "cashRate",
            "cashStartDate",
            "cashMaturityDate",
        ]
