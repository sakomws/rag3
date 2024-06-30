import openai
import yfinance as yf
import requests
def real_time_data_yahoo(query, stock_name="TSLA"):
    msft = yf.Ticker(stock_name)

    # get all stock info

    # get historical market data
    hist = msft.history(period="1d", interval='1m')
    
    hist.to_csv('stock_data.csv', index=False)

    # with open('path_to_your_file.txt', 'r') as file:
    #   file_content = file.read()


    # Initialize OpenAI client
    client = openai.OpenAI(api_key="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")

    # with open('stock_data.csv', 'rb') as f:
    #     response = openai.File.create(
    #         purpose='answers',
    #         file=f
    #     )
    # file_id = response['id']

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant here is the stock data: {hist}, you should not include disclaimer, just the answer, even if you are not sure"},
            {"role": "user", "content": query},
        ],
       # files=[file_id]
    )

    print(response.choices[0].message.content)


def real_time_data_eodhd(query, stock_name="TSLA"):
    url = f'https://eodhd.com/api/real-time/TSLA.US?api_token=6680b4ada95ad7.06901661&fmt=json'
    data = requests.get(url).json()

    # with open('path_to_your_file.txt', 'r') as file:
    #   file_content = file.read()


    # Initialize OpenAI client
    client = openai.OpenAI(api_key="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")

    # with open('stock_data.csv', 'rb') as f:
    #     response = openai.File.create(
    #         purpose='answers',
    #         file=f
    #     )
    # file_id = response['id']

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant here is the stock data: {data}, you should not include disclaimer, just the answer, even if you are not sure"},
            {"role": "user", "content": query},
        ],
       # files=[file_id]
    )

    print(response.choices[0].message.content)
