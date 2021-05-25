import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import plotly.graph_objects as go
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from nsetools import Nse


nse = pd.read_csv("Datasets/NSE_COMPANIES.csv")
symbols = nse['Symbol'].sort_values().tolist()

ticker = st.sidebar.selectbox('Choose A Nse Stock', symbols) + ".NS"


info_type = st.sidebar.radio('Choose an Info Type',
                             ("Company Info", "Company Statistics", "Technical Indicators", "Market News", "Top Winners/Losers"))

if info_type == "Company Info":
    stock = yf.Ticker(ticker)
    info = stock.info
    logo = info['logo_url']
    st.markdown(f'<center><img src="{logo}" /></center>',
                unsafe_allow_html=True)
    st.header("Company Profile")
    st.markdown('** Name **: ' + info["shortName"])
    st.markdown('**Sector **: ' + info["sector"])
    st.markdown('**Industry **: ' + info["industry"])
    st.markdown('**Phone **: ' + info["phone"])
    st.markdown(
        '** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['zip'] + ', ' + info['country'])
    st.markdown('**Website **: ' + info["website"])
    st.markdown("**Country **: " + info["country"])
    st.markdown("**Market Capital **: " + str(info["marketCap"]))
    st.markdown("**Volume **: " + str(info["volume"]))
    st.markdown("**Currency **: " + info["currency"])
    st.markdown("**Exchange **: " + info["exchange"])
    st.markdown("**Symbol **: " + info["symbol"])
    st.markdown("**Quote Type **: " + info["quoteType"])
    st.markdown('** Market **: ' + info['market'])
    st.info(info["longBusinessSummary"])

    fundInfo = {
        'Previous Close (INR)': info['previousClose'],
        'Enterprise Value (INR)': info['enterpriseValue'],
        'Enterprise To Revenue Ratio': info['enterpriseToRevenue'],
        'Enterprise To Ebitda Ratio': info['enterpriseToEbitda'],
        'Net Income (INR)': info['netIncomeToCommon'],
        'Profit Margin Ratio': info['profitMargins'],
        'Forward PE Ratio': info['forwardPE'],
        'PEG Ratio': info['pegRatio'],
        'Price to Book Ratio': info['priceToBook'],
        'Forward EPS (INR)': info['forwardEps'],
        'Beta ': info['beta'],
        'Book Value (INR)': info['bookValue'],
        'Dividend Rate (%)': info['dividendRate'],
        'Dividend Yield (%)': info['dividendYield'],
        'Five year Avg Dividend Yield (%)': info['fiveYearAvgDividendYield'],
        'Payout Ratio': info['payoutRatio'],
        'Last Fiscal Year End': info["lastFiscalYearEnd"]
    }

    fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
    fundDF = fundDF.rename(columns={0: 'Value'})
    st.subheader('Fundamental Info')
    st.table(fundDF)

    start = dt.datetime.today() - dt.timedelta(2 * 365)
    end = dt.datetime.today()
    df = yf.download(ticker, start, end)
    df = df.reset_index()
    fig = go.Figure(
        data=go.Scatter(x=df['Date'], y=df['Adj Close'])
    )
    fig.update_layout(
        title={
            'text': "Stock Prices Over Past Two Years",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)

    marketInfo = {
        "Volume": info['volume'],
        "Average Volume": info['averageVolume'],
        "Market Cap": info["marketCap"],
        "Float Shares": info['floatShares'],
        "Regular Market Price (USD)": info['regularMarketPrice'],
        'Bid Size': info['bidSize'],
        'Ask Size': info['askSize'],
        "Share Short": info['sharesShort'],
        'Short Ratio': info['shortRatio'],
        'Share Outstanding': info['sharesOutstanding']

    }

    marketDF = pd.DataFrame(data=marketInfo, index=[0])
    st.table(marketDF)

if info_type == "Technical Indicators":
    HtmlFile = open("Datasets/Indicators.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code)
    st.markdown('<style>iframe{position: fixed;background: #000;border: none;top: 0; right: 0;bottom: 0; left: '
                '0;width: 100%;height: 100%;}</style>',
                unsafe_allow_html=True)

if info_type == "Company Statistics":
    st.header(ticker + "  Statistics")
    r = requests.get(f"https://finance.yahoo.com/quote/{ticker}/key-statistics")

    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find(id="Main")
    st.markdown(results, unsafe_allow_html=True)

if info_type == "Market News":
    HtmlFile = open("Datasets/News.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code)
    st.markdown('<style>iframe{position: fixed;background: #000;border: none;top: 0; right: 0;bottom: 0; left: '
                '0;width: 100%;height: 100%;}</style>',
                unsafe_allow_html=True)

if info_type == "Top Winners/Losers":
    nse = Nse()
    st.subheader("Winner")
    Gainers = nse.get_top_gainers()
    Gainers = pd.DataFrame(Gainers)
    st.table(Gainers)
    st.subheader("Losers")
    Losers = nse.get_top_losers()
    Losers = pd.DataFrame(Losers)
    st.table(Losers)
