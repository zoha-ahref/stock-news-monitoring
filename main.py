import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
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



# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data['4. close']




# TODO 2. - Get the day before yesterday's closing stock price
day_before_data = data_list[1]
day_before_closing = day_before_data['4. close']

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
diff = float(yesterday_closing) - float(day_before_closing)
up_down = None
if diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round(diff / float(yesterday_closing)) * 100

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").


## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
parameters_news = {
    "qInTitle": COMPANY_NAME,
    "apiKey": "a018ff3136a64976844527f5fc617388",

}
response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
response_news.raise_for_status()
data_news = response_news.json()["articles"]
get_news = data_news[:3]
print(get_news)
if diff_percent > 5:
    print(get_news)
# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadlines: {article['title']} \nBrief: {article['description']}" for article in get_news]

# TODO 9. - Send each article as a separate message via Twilio.
client = Client(account_sid, auth_token)
for article in formatted_articles:
    message = client.messages.create(
            body=article,
            from_='+19735574099',
            to=CONTACT
        )
    print(message.status)


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
