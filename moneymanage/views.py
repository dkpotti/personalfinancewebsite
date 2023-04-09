from django.shortcuts import render, redirect
from .models import moneymanage
from .forms import CashForm
from django.contrib import messages
from forex_python.converter import CurrencyRates
from django.db.models import F, FloatField, ExpressionWrapper

# Create your views here.


def home(request):
    allCashTypes = moneymanage.objects.all()
    totalCash = 0
    for eachCashItem in allCashTypes:
        totalCash = totalCash + eachCashItem.cashAmount
    allCashTypes = moneymanage.objects.annotate(
        percentageInvolved=ExpressionWrapper(
            F("cashAmount") / totalCash * 100, output_field=FloatField()
        )
    )
    for eachCashItem in allCashTypes:
        eachCashItem.percentageInvolved = eachCashItem.cashAmount / totalCash * 100
    currencyConvert = CurrencyRates()
    currentRate = currencyConvert.get_rate("USD", "INR")
    inr_amount = currencyConvert.convert("USD", "INR", totalCash)
    return render(
        request,
        "home.html",
        {
            "allCashTypes": allCashTypes,
            "totalCash": totalCash,
            "inr_amount": inr_amount,
            "currentRate": currentRate,
        },
    )


def addmoney(request):
    if request.method == "POST":
        form = CashForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "")
            return redirect("home")
    else:
        return render(request, "add-money.html", {})
