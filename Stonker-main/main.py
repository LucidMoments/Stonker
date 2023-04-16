
import telebot
import yfinance as yf
import plotly.graph_objects as go
import kaleido

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Greet', 'greet'])
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['hello','Hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello! If you would like to check the r/WallStreetBets stocks type /WSB, If you want to check the price of another stock just write '/price ' and the stocks name")

@bot.message_handler(commands=['wsb','WSB'])
def get_stocks(message):
  response = ""
  stocks = ['gme', 'amc', 'nok']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()
  response = "Stock Data\n\n"
  response += f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  
  print(response)
  bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['price','Price'])
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")

@bot.message_handler(commands=['graph','Graph'])
def send_graph(message):
  request = message.text.split()[1]
  tickers = request
  
 
  stock = yf.Ticker(tickers)
  hist = stock.history(period='1y')
  hist.head()
  fig = go.Figure(data=go.Scatter(x=hist.index,y=hist['Close'], mode='lines'))
  
  #fig.write_image("fig1.png",format='png',engine='kaleido')
  photo1 = open("//home//runner//Stonker//fig1.png", 'rb')
  bot.send_photo(message.chat.id, photo1)
  
  
bot.polling()