import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"  #stock you want to track
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = "AC358bfdd0f5bbe9ba3e487710fa863dd1"
auth_token = "949fa0d95b574619099330aa40e87b33"

CONTACT = os.environ.get("RECEIVER")

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": "SBRW4SZEIHKIURKL",

}



# Get yesterday's closing stock price
response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data['4. close']




# Get the day before yesterday's closing stock price
day_before_data = data_list[1]
day_before_closing = day_before_data['4. close']

# Find the positive difference
diff = float(yesterday_closing) - float(day_before_closing)
up_down = None
if diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round(diff / float(yesterday_closing)) * 100
print(diff_percent)



## STEP 2: https://newsapi.org/
# if percentage greater than 5, get the first 3 news pieces for the COMPANY_NAME.

if abs(diff_percent) > 1:
    parameters_news = {
        "qInTitle": COMPANY_NAME,
        "apiKey": "a018ff3136a64976844527f5fc617388",

    }
    response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    data_news = response_news.json()["articles"]
    get_news = data_news[:3] #creates a list that contain the first 3 articles
    print(get_news)



##  Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadlines: {article['title']} \nBrief: {article['description']}" for article in get_news]
    print(formatted_articles)
# Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
                body=article,
                from_='+19735574099',
                to=CONTACT,
            )




"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
