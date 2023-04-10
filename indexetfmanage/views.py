from django.shortcuts import render, redirect
from .models import indexetfmanage
from .forms import FundForm
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from django.db.models import (
    F,
    FloatField,
    ExpressionWrapper,
    CharField,
    DateField,
)

# Create your views here.


def indexetfhome(request):
    allFunds = indexetfmanage.objects.all()
    message = ""
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36"
    }
    for eachFund in allFunds:
        ticker_symbol = eachFund.indexName
        ticker_info = yf.Ticker(ticker_symbol)
        indexquoteurl = "https://finance.yahoo.com/quote/{}/".format(ticker_symbol)
        indexperformanceurl = (
            "https://finance.yahoo.com/quote/{}/performance?p={}".format(
                ticker_symbol, ticker_symbol
            )
        )
        indexprofileurl = "https://finance.yahoo.com/quote/{}/profile?p={}".format(
            ticker_symbol, ticker_symbol
        )
        response = requests.get(
            indexquoteurl,
            headers=header,
        )
        performanceresponse = requests.get(indexperformanceurl, headers=header)
        profileresponse = requests.get(indexprofileurl, headers=header)

        html_content = response.content
        performance_html_content = performanceresponse.content
        profile_html_content = profileresponse.content

        indexFundHtml = BeautifulSoup(html_content, "html.parser")

        performanceindexFundHtml = BeautifulSoup(
            performance_html_content, "html.parser"
        )
        profileindexFundHtml = BeautifulSoup(profile_html_content, "html.parser")

        eachFund.indexlongname = (
            indexFundHtml.find("h1", {"class": "D(ib) Fz(18px)"}).text
            if indexFundHtml.find("h1", {"class": "D(ib) Fz(18px)"}) is not None
            else "NA"
        )
        eachFund.indexprice = (
            indexFundHtml.find(
                "fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}
            ).text
            if indexFundHtml.find(
                "fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}
            )
            is not None
            else "NA"
        )
        eachFund.expenseratio = (
            indexFundHtml.find("td", {"data-test": "EXPENSE_RATIO-value"}).text
            if indexFundHtml.find("td", {"data-test": "EXPENSE_RATIO-value"})
            is not None
            else "NA"
        )
        eachFund.ytdreturn = (
            indexFundHtml.find("td", {"data-test": "YTD_DTR-value"}).text
            if indexFundHtml.find("td", {"data-test": "YTD_DTR-value"}) is not None
            else indexFundHtml.find("td", {"data-test": "YTD_RETURN-value"}).text
        )
        eachFund.peratio = (
            indexFundHtml.find("td", {"data-test": "PE_RATIO-value"}).text
            if indexFundHtml.find("td", {"data-test": "PE_RATIO-value"}) is not None
            else (
                ticker_info.info["trailingPE"]
                if ticker_info.info["trailingPE"] is not None
                else "NA"
            )
        )
        eachFund.fundType = (
            ticker_info.info["quoteType"]
            if yf.Ticker(ticker_symbol).info["quoteType"] is not None
            else eachFund.fundType
        )

    return render(
        request,
        "indexetfhome.html",
        {"message": message, "allFunds": allFunds},
    )


def addfund(request):
    if request.method == "POST":
        form = FundForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("indexetfhome")
    else:
        return render(request, "add-fund.html", {})
