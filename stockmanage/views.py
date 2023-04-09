from django.shortcuts import render, redirect
from .models import stockmanage
import yfinance as yf
from django.db.models import F, FloatField, ExpressionWrapper, CharField, DateField
from .forms import StockForm
from django.contrib import messages
import requests
from bs4 import BeautifulSoup


# Create your views here.


def index(request):
    api_key = "KPDTZTGNJJHY3LS5"
    allstocks = stockmanage.objects.all()
    allCashTypes = stockmanage.objects.annotate(
        stockName=ExpressionWrapper(00, output_field=CharField())
    )
    allCashTypes = stockmanage.objects.annotate(
        sectorName=ExpressionWrapper("", output_field=CharField())
    )
    allCashTypes = stockmanage.objects.annotate(
        regularMarketPrice=ExpressionWrapper(00, output_field=FloatField())
    )
    allCashTypes = stockmanage.objects.annotate(
        industryName=ExpressionWrapper(00, output_field=FloatField())
    )
    allCashTypes = stockmanage.objects.annotate(
        peRatio=ExpressionWrapper(00, output_field=FloatField())
    )
    allCashTypes = stockmanage.objects.annotate(
        dividendDate=ExpressionWrapper(00, output_field=DateField())
    )
    for eachStockObject in allstocks:
        eachStockObject.stockName = yf.Ticker(eachStockObject.symbol).info["longName"]
    for eachStockObject in allstocks:
        eachStockObject.regularMarketPrice = yf.Ticker(eachStockObject.symbol).info[
            "regularMarketPrice"
        ]

    for eachStockObject in allstocks:
        response = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={eachStockObject.symbol}&apikey={api_key}"
        )
        stock_data = response.json()
        print(stock_data)
        eachStockObject.sectorName = (
            stock_data["Sector"] if stock_data["Sector"] is not None else "NA"
        )
        eachStockObject.industryName = stock_data["Industry"]
        eachStockObject.peRatio = stock_data["PERatio"]
        eachStockObject.dividendDate = stock_data["DividendDate"]

    symbolDetails = {
        "allstocks": allstocks,
    }
    return render(request, "index.html", symbolDetails)


def addstock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "")
            return redirect("index")
    else:
        return render(request, "add-stock.html", {})
