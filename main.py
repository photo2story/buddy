# Main.py

from flask import Flask
from threading import Thread
import os

# Initialize Flask
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))

# Start the Flask server in a new thread
def keep_alive():
    server = Thread(target=run)
    server.start()

# Make sure to call keep_alive() before starting the Discord bot
keep_alive()

# Your Discord bot setup and run logic should follow here

import asyncio
import os
from datetime import datetime
import pandas as pd
import numpy as np
import discord
import requests
from discord.ext import commands
from flask import Flask
import pprint

from buy_stock import buy_us_stock, sell_us_stock  # buy_stock.py 파일을 가져옵니다.
from estimate_stock import estimate_snp, estimate_stock
from get_account_balance import (
    calculate_buyable_balance,
    get_balance,
    get_market_from_ticker,
    get_ticker_from_korean_name,
    get_ticker_price,
)
from get_earning import get_earning_alpha
from get_ranking import get_ranking_alpha
from get_ticker import load_tickers, search_tickers, get_ticker_name,update_stock_market_csv
from Results_plot import plot_comparison_results, plot_results_all
from get_compare_stock_data import merge_csv_files, load_sector_info
from discord.ext import tasks
from Results_plot_mpl import plot_results_mpl
import tracemalloc
tracemalloc.start()

key = os.environ['H_APIKEY']
secret = os.environ['H_SECRET']
acc_no = os.environ['H_ACCOUNT']
ACC_NO_8 = os.environ['H_ACCOUNT_8']
# Discord 봇 토큰 및 채널 ID 가져오기
TOKEN = os.environ['DISCORD_APPLICATION_TOKEN']
channel_id = os.environ['DISCORD_CHANNEL_ID']

# 감시할 주식 종목 리스트' 5490포홀ks, 86520kq 에코,373220.ks 엔솔,  
stocks = [
    'VOO', 'QQQ', 'AAPL', 'GOOGL', 'MSFT','U', 'SPOT', 'PLTR','ADBE', 'TSLA', 'APTV', 'FSLR',  'PFE', 'INMD', 'UNH',  'TDOC', 'OXY', 'FSLR', 'ALB','AMZN', 'NFLX', 'LLY', 'EL',
    'NKE', 'LOW', 'ADSK', 'NIO', 'F', 'BA', 'GE', 'JPM', 'BAC', 'SQ', 'HD', 'PG', 'IONQ','086520','NVDA','AMD']
# stocks = ['086520']

start_date = "2022-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')  # 오늘 날짜 문자열로 변환하기
initial_investment = 30000000
monthly_investment = 1000000

# app = Flask(__name__)

# message = {}

# @app.route("/")
# def hello_world():
#     name = os.environ.get("NAME", message)
#     return "status {}!".format(name)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)

# 봇이 준비되었을 때 실행되는 이벤트 핸들러
@bot.event
async def on_ready():
    print(f'Bot이 성공적으로 로그인했습니다: {bot.user.name}')
    # The channel_id should be fetched within an async context
    channel = bot.get_channel(int(channel_id))
    if channel:
        await channel.send(f'Bot이 성공적으로 로그인했습니다: {bot.user.name}')


@bot.command()
async def buy(ctx, *args):
    buy_option = ' '.join(args)
    await ctx.send(f'명령어로 전달된 인자: {buy_option}')
    # await ctx.send(f'명령어로 전달된 인자: {buy_option}')
    try:
        # args에서 ticker와 last,quantity 추출
        ticker, last_price, quantity = buy_option.split(',')
        ticker = ticker.strip().upper()
        # 시장 정보 가져오기
        market_info = get_market_from_ticker(ticker)
        last_price = get_ticker_price(key, secret, acc_no, market_info, ticker)
        last_price = round(float(last_price), 2)  # 소수점 두 자리로 반올림
        await ctx.send(f'주문단가: {last_price}')
        quantity = int(quantity.strip())  # 수량은 정수로 변환
        resp = buy_us_stock(key, secret, acc_no, market_info, ticker, last_price, quantity)  # 적절한 값 사용
  
        # 주문이 성공한 경우
        if 'msg_cd' in resp and resp['msg_cd'] == 'APBK0013':
            await ctx.send(f'{quantity}주의 {ticker}를 매수했습니다.')
        # 주문이 실패한 경우
        else:
            await ctx.send(f'주문에 실패했습니다. 오류 메시지: {resp["msg1"]}')
    except ValueError as e:
        await ctx.send(f'오류가 발생했습니다: {e}')
    except Exception as e:
        await ctx.send(f'알 수 없는 오류가 발생했습니다: {e}')
  
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))



@bot.command()
async def sell(ctx, *args):
    sell_option = ' '.join(args)
    await ctx.send(f'명령어로 전달된 인자: {sell_option}')
    # await ctx.send(f'명령어로 전달된 인자: {buy_option}')
    try:
        # args에서 ticker와 last,quantity 추출
        ticker, last_price, quantity = sell_option.split(',')
        ticker = ticker.strip().upper()
        ticker = ticker.upper()
        market_info = get_market_from_ticker(ticker)
        last_price = get_ticker_price(key,secret,acc_no,market_info,ticker)
        last_price = round(float(last_price), 2)  # 소수점 두 자리로 반올림
        await ctx.send(f'주문단가: {last_price}')
        quantity = int(quantity.strip())  # 수량은 정수로 변환
        resp = sell_us_stock(key, secret, acc_no, market_info, ticker, last_price, quantity)

        if 'msg_cd' in resp and resp['msg_cd'] == 'APBK0013':
            await ctx.send(f'{quantity}주의 {ticker}를 매도했습니다.')
        else:
            if 'ordy' in resp['output'] and resp['output']['ordy'] == '매도불가':
                await ctx.send(f'{quantity}주의 {ticker}는 현재 주문 단가보다 높아 매도가 불가능합니다.')
            else:
                await ctx.send(f'주문에 실패했습니다. 오류 메시지: {resp["msg1"]}')
    except ValueError as e:
        await ctx.send(f'오류가 발생했습니다: {e}')
    except Exception as e:
        await ctx.send(f'알 수 없는 오류가 발생했습니다: {e}')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

@bot.command()
async def ping(ctx):
  await ctx.send(f'pong: {bot.user.name}')

authorized_ids = [channel_id]  # Replace these numbers with valid Discord IDs

@bot.command()
@commands.has_role('Bot Controller')  # Only users with the 'Bot Controller' role can use this command
async def run(ctx):
  if ctx.author.id in authorized_ids:
      global is_running
      if is_running:
          is_running = False  # Set the signal to False to stop the balance loop
          await ctx.send("Stopping the balance check...")
      else:
          await ctx.send("Balance check is not running.")
      pass
  else:
      await ctx.send("You do not have permission to use this command.")

@bot.command()
@commands.has_permissions(administrator=True)  # Only users with admin permissions can use this command
async def balance(ctx):
  global is_running
  is_running = True
  while is_running:
    # 여기에 기존의 balance 로직을 넣습니다.
  
    # Discord로 결과 전송하기
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
    # won_psbl_amt, us_psbl_amt, frst_bltn_exrt, buyable_balance = calculate_buyable_balance(key, secret, acc_no)
    won_psbl_amt, us_psbl_amt, frst_bltn_exrt, buyable_balance = calculate_buyable_balance(key,secret,acc_no)
    # print(f'won_psbl_amt: {won_psbl_amt}, us_psbl_amt: {us_psbl_amt}, frst_bltn_exrt: {frst_bltn_exrt}, buyable_balance: {buyable_balance}')
  
    # message = f'현재 매수가능금액은 {won_psbl_amt:.3f}원입니다.'
    message = f'현재 매수가능금액은 {buyable_balance:.3f}$입니다.'
    response = requests.post(DISCORD_WEBHOOK_URL, data={'content': message})
  
    # 잔고 정보 가져오기
    balance_data = get_balance(key, secret, acc_no)

    for item in balance_data:
        ticker = item['ticker']
        profit_amount = float(item.get('profit_amount', 0))
        my_quantity = float(item.get('holding_quantity', 0))
        average_price = float(item.get('average_price', 0))
        current_price = float(item.get('current_price', 0))
        my_rate = float(item.get('profit_rate', 0))
        name = item.get('name', '')

        # Assuming DISCORD_WEBHOOK_URL is defined elsewhere in your code
        message = {
            'content': (f"{ticker}({name})\n"
                        f"보유 수량 {my_quantity:.2f}, "
                        f"수익 금액 {profit_amount:.4f}, "
                        f"평균 가격 {average_price:.4f}, "
                        f"수익율 {my_rate:.4f}, "
                        f"현재 가격 {current_price:.4f} \n")
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)

  
  
        # Discord 메시지가 전송되었는지 확인
        if response.status_code != 204:
            print(f'Discord 메시지 전송 실패: {ticker}')
        else:
            print(f'Discord 메시지 전송 성공: {ticker}')
  
  
        # 매도 조건 확인 및 매도 명령 실행
        if my_rate < -3.0 and my_quantity > 1:
          sell_quantity = my_quantity // 2 if my_rate >= -5.0 else max(my_quantity - 1, 0)
  
          # 매도 명령 실행
          # sell 함수 호출 시, 필요한 인자를 전달
          # Ensure sell_quantity is an integer and format the string with two commas
          formatted_sell_quantity = f"{ticker},,{int(sell_quantity)}"
          await sell(ctx, formatted_sell_quantity)  # Passes the formatted string as a single argument.

        # 1분(60초) 대기
        await asyncio.sleep(10)

          # 백테스팅 로직을 별도의 함수로 분리합니다.
async def backtest_and_send(ctx, stock, option_strategy):
    total_account_balance, total_rate, str_strategy, invested_amount, str_last_signal, min_stock_data_date, file_path,result_df = estimate_stock(
        stock, start_date, end_date, initial_investment, monthly_investment, option_strategy)
    min_stock_data_date = str(min_stock_data_date)
    min_stock_data_date = min_stock_data_date.split(' ')[0]
    user_stock_file_path1 = file_path
    # print(user_stock_file_path1)

    file_path = estimate_snp(stock,'VOO', min_stock_data_date, end_date, initial_investment, monthly_investment, option_strategy,result_df)

    user_stock_file_path2 = file_path #'result_VOO_{}.csv'.format(stock)
    # print(user_stock_file_path2)
    # estimate_snp('VOO', first_date, end_date, initial_investment, monthly_investment, option_strategy)

    # 티커 이름 가져오기
    name = get_ticker_name(stock)
    # Discord로 결과 전송하기
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
    message = {
        'content': f"Stock: {stock} ({name})\n"
                   f"Total_rate: {total_rate:,.0f} %\n"
                   f"Invested_amount: {invested_amount:,.0f} $\n"
                   f"Total_account_balance: {total_account_balance:,.0f} $\n"
                   f"Last_signal: {str_last_signal} \n"
                   f" "
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)

    if response.status_code != 204:
        print('Discord 메시지 전송 실패')
    else:
        print('Discord 메시지 전송 성공')

    # 결과 그래프 그리기
    # 두 주식의 백테스팅 결과를 비교하는 그래프 그리기
    plot_comparison_results(user_stock_file_path1, user_stock_file_path2, stock, 'VOO',total_account_balance, total_rate, str_strategy,invested_amount, min_stock_data_date)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

# 'run' 커맨드를 사용하여 모든 주식에 대해 백테스팅을 자동으로 수행합니다.
# @bot.command()
# async def buddy(ctx):
#     for stock in stocks:  # 주식 리스트를 순회하며 백테스팅 수행
#         await backtest_and_send(ctx, stock, 'modified_monthly')
#         plot_results_mpl(stock, start_date, end_date)
        
#         await asyncio.sleep(2)  # 1초 타임슬립 추가
#     # 백테스팅 결과를 섹터별로 정리
#     update_stock_market_csv('stock_market.csv', stocks)
#     sector_dict = load_sector_info()  # 섹터 정보 로드
#     folder_path = '.'  # CSV 결과가 저장된 폴더 경로
#     merge_csv_files(folder_path, sector_dict)  # 섹터별로 결과 파일 생성

#     await ctx.send("백테스팅 결과가 섹터별로 정리되었습니다.")
@bot.command()
async def buddy(ctx):
    loop = asyncio.get_running_loop()  # Get the current event loop

    for stock in stocks:  # 주식 리스트를 순회하며 백테스팅 수행
        await backtest_and_send(ctx, stock, 'modified_monthly')

        # Check if plot_results_mpl should be awaited or run in executor based on its implementation
        plot_results_mpl(stock, start_date, end_date)  # Assuming it's synchronous

        await asyncio.sleep(2)  # 1초 타임슬립 추가

    # Run synchronous functions in the executor
    await loop.run_in_executor(None, update_stock_market_csv, 'stock_market.csv', stocks)
    sector_dict = await loop.run_in_executor(None, load_sector_info) # run_in_executor returns a future, await it if function is synchronous
    path = '.'  # Assuming folder path
    await loop.run_in_executor(None, merge_csv_files, path, sector_dict)

    await ctx.send("백테스팅 결과가 섹터별로 정리되었습니다.")

@bot.command()
async def ranking(ctx):
    try:
        # 함수 호출 및 결과 가져오기
        result = get_ranking_alpha()

        # Discord 웹훅 URL을 설정하세요.
        DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

        # 웹훅을 사용하여 메시지를 디스코드로 전송합니다.
        message_content = f'```\n{result}\n```'
        data = {
            'content': message_content
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)

        if response.status_code != 204:
            print('Discord 메시지 전송 실패')
        else:
            print('Discord 메시지 전송 성공')
    except Exception as e:
        await ctx.send(f"실행 중 오류 발생: {e}")

@bot.command()
async def earning(ctx, *args):
    stock_name = ' '.join(args)
    await ctx.send(f'명령어로 전달된 인자: {stock_name}')
    try:
        info_stock = str(stock_name).upper()  # 여기에 .upper()를 추가합니다.
        # 함수 호출 및 결과 가져오기
        result = get_earning_alpha(info_stock)

        # Discord 웹훅 URL을 설정하세요.
        DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

        # 웹훅을 사용하여 메시지를 디스코드로 전송합니다.
        message_content = f'```\n{result}\n```'
        data = {
            'content': message_content
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)

        if response.status_code != 204:
            print('Discord 메시지 전송 실패')
        else:
            print('Discord 메시지 전송 성공')
    except Exception as e:
        await ctx.send(f"실행 중 오류 발생: {e}")


@bot.command()
async def ticker(ctx, *, query: str = None):
    if query is None:
        await ctx.send("주식명을 입력해주세요.")
        return

    ticker_dict = load_tickers()
    matching_tickers = search_tickers(query, ticker_dict)

    if not matching_tickers:
        await ctx.send("검색 결과가 없습니다.")
        return

    # Symbol과 Name을 함께 표시
    # Assuming matching_tickers contains the result you want to send
    response_message = "검색 결과:\n"
    response_messages = []
    for symbol, name in matching_tickers:  # Correct this line according to your actual tuple format
        line = f"{symbol} - {name}\n"
        if len(response_message) + len(line) > 2000:  # Send the message if the limit is reached
            response_messages.append(response_message)
            response_message = "검색 결과(계속):\n"  # Start new message with a header
        response_message += line
  
    # Add the last chunk if it's not empty
    if response_message:
        response_messages.append(response_message)
  
    # Send all messages
    for message in response_messages:
        await ctx.send(message)


  
@bot.command()
async def stock(ctx, *args):
    stock_name = ' '.join(args)
    await ctx.send(f'명령어로 전달된 인자: {stock_name}')
    try:
        info_stock = str(stock_name).upper()  # 여기에 .upper()를 추가합니다.
        if info_stock.startswith('K '):  # 'stock k 흥국화재'
            korean_stock_name = info_stock[2:].upper()
            korean_stock_code = get_ticker_from_korean_name(korean_stock_name)  # 000540.KS,흥국화재,KOSPI
            if korean_stock_code is None:
                await ctx.send(f'{korean_stock_name} 주식을 찾을 수 없습니다.')
                return
            else:
                info_stock = korean_stock_code

        # 옵션 선택을 위한 메시지 전송
        await ctx.send(
            "백테스팅 옵션을 선택해주세요:\n"
            "1: 디폴트 옵션\n"
            "2: 적립식 투자\n"
            "3: 변형 적립식투자(이익금 안정화)"
        )

        # check 함수 정의
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content in ['1', '2', '3']

        try:
            option_msg = await bot.wait_for('message', check=check, timeout=5.0)  # Wait for a valid option
            option = option_msg.content
        except asyncio.TimeoutError:
            option = '3'
            await ctx.send("시간 초과: 변형 적립식투자(이익금 안정화) 옵션을 자동으로 선택합니다.")

        # 옵션 번호를 확인합니다.
        if option not in ['1', '2', '3']:
            await ctx.send("잘못된 옵션입니다. 1, 2, 또는 3 중에서 선택해주세요.")
            return

        # 옵션에 따라 전략을 설정하고 백테스팅을 실행합니다.
        option_strategy = 'default' if option == '1' else 'monthly' if option == '2' else 'modified_monthly'
        # 사용자에게 선택한 옵션에 대한 확인 메시지 전송
        option_text = '디폴트 옵션' if option == '1' else '적립식 투자' if option == '2' else '변형 적립식투자'
        await ctx.send(f"{stock_name} 주식을 {option_text}으로 검토하겠습니다.")

        # 옵션에 따라 백테스트 및 결과 전송
        await backtest_and_send(ctx, info_stock, option_strategy)
        plot_results_mpl(info_stock, start_date, end_date)
    except Exception as e:  # Replace Exception with more specific exceptions if possible
        await ctx.send(f'An error occurred: {e}')


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send("명령이 존재하지 않습니다.")
#     elif isinstance(error, OptionValueError):
#         await ctx.send(str(error))
#     else:
#         await ctx.send(f"An error occurred: {type(error).__name__} – {error}")


@bot.command()
async def show_all(ctx):
    try:
        await plot_results_all()  # plot_results_all 함수를 비동기로 호출
        # plot_results_mpl(info_stock, start_date, end_date)
        await ctx.send("모든 결과가 성공적으로 표시되었습니다.")
    except Exception as e:
        await ctx.send(f"오류가 발생했습니다: {e}")
        print(f"오류: {e}")




@bot.command()
async def stream(ctx, *args):
    # args에서 티커 추출
    stream_option = ' '.join(args)
    await ctx.send(f'명령어로 전달된 인자: {sell_option}')
    # await ctx.send(f'명령어로 전달된 인자: {buy_option}')
    try:
        # args에서 ticker와 last,quantity 추출
        ticker, quantity = stream_option.split(',')
        ticker = ticker.strip().upper()
        ticker = ticker.upper()
        market_info = get_market_from_ticker(ticker)
        last_price = get_ticker_price(key,secret,acc_no,market_info,ticker)
        last_price = round(float(last_price), 2)  # 소수점 두 자리로 반올림
        await ctx.send(f'현재가: {last_price}')
        quantity = int(quantity.strip())  # 수량은 정수로 변환
        resp = sell_us_stock(key, secret, acc_no, market_info, ticker, last_price, quantity)
  
        if 'msg_cd' in resp and resp['msg_cd'] == 'APBK0013':
            await ctx.send(f'{quantity}주의 {ticker}를 매도했습니다.')
        else:
            if 'ordy' in resp['output'] and resp['output']['ordy'] == '매도불가':
                await ctx.send(f'{quantity}주의 {ticker}는 현재 주문 단가보다 높아 매도가 불가능합니다.')
            else:
                await ctx.send(f'주문에 실패했습니다. 오류 메시지: {resp["msg1"]}')
    except ValueError as e:
        await ctx.send(f'오류가 발생했습니다: {e}')
    except Exception as e:
        await ctx.send(f'알 수 없는 오류가 발생했습니다: {e}')
  
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))
  

bot.run(TOKEN)

# if __name__ == "__main__":
#   app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
    
# .\\.venv\\Scripts\\activate
# python main.py    