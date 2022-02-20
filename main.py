import requests
from datetime import *
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# get today's date
today = date.today()
yesterday_date = today - timedelta(days=1)
before_yesterday_date = today - timedelta(days=2)

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# get stock price and increase/decrease
params_stock = {
    "function" : "TIME_SERIES_INTRADAY",
    "symbol" : STOCK_NAME,
    "interval" : "60min",
    "apikey" : "QVZE36KP1O1EAE03"
}
resource = requests.get(url=STOCK_ENDPOINT, params=params_stock)
resource.raise_for_status()
data_stock = resource.json()
price_yesterday = float(data_stock["Time Series (60min)"][f"{yesterday_date} 16:00:00"]["4. close"])
price_before_yesterday = float(data_stock["Time Series (60min)"][f"{before_yesterday_date} 16:00:00"]["4. close"])

difference = (price_yesterday - price_before_yesterday)/price_yesterday * 100

up_down = None
if difference > 0:
    up_down = "😃"
else:
    up_down = "😔"

if abs(difference) > 5:
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    params_news = {
        "q" : COMPANY_NAME,
        "from" : price_before_yesterday,
        "apiKey" : "b00bc8a003974e3290b797553e2cdf89"
    }
    resource_news = requests.get(url=NEWS_ENDPOINT, params=params_news)
    resource_news.raise_for_status()
    data_news = resource_news.json()
    first_three = data_news["articles"][:3]

        ## STEP 3: Use twilio.com/docs/sms/quickstart/python
        #to send a separate message with each article's title and description to your phone number.
    title_list = [items["title"] for items in first_three]
    brief_list = [items["description"] for items in first_three]
    formatted_list = [f"{COMPANY_NAME}:{up_down}%\nHeadline:{items['title']}.\nBrief:{items['description']}" for items in first_three]


#TODO 9. - Send each article as a separate message via Twilio. 


    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC6137dc4dbbe738c9c004fc1508f834e7'
    auth_token = 'e64e78d2bc25adb2ac3c00d9c863376b'
    client = Client(account_sid, auth_token)

    for number in range(0,3):
        message = client.messages \
            .create(
            body= formatted_list[number],
            from_='+19402513447',
            to='+447421993043'
        )

        print(message.status)

