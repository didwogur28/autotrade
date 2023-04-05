import pyupbit
import time
import datetime
import pandas as pd
from pyupbit.request_api import _send_get_request, _send_post_request, _send_delete_request

def set_initial_order(ticker):

    orderCnt = 0

    buyPrice = pyupbit.get_orderbook(ticker=ticker)['orderbook_units'][0]['ask_price']
    selPrice = pyupbit.get_orderbook(ticker=ticker)['orderbook_units'][0]['ask_price']

    while orderCnt < 10:
        orderCnt += 1

        selPrice = int(selPrice / rateValue)
        buyPrice = int(buyPrice * rateValue)

        upbit.sell_limit_order(ticker, selPrice, 20)
        upbit.buy_limit_order(ticker, buyPrice, 20)

        print("Sell price: %d" % (selPrice))
        print("Buy price: %d" % (buyPrice))
        print("=====================")

        time.sleep(1)

    print("초기 셋팅 끝")

def orders_status(self, ticker):

    try:
        url = "https://api.upbit.com/v1/orders"
        data = {"market": ticker,
                "page" : 1
                }
        headers = self._request_headers(data)
        return _send_get_request(url, headers=headers, params=data)

    except Exception as x:
        print(x.__class__.__name__)
        return None

def get_target_price(ticker, interval, k):  # 변동성 돌파 전략으로 매수 목표가 정하기
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker, interval):  # 시작 시간 조회
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=1)
    start_time = df.index[0]
    return start_time


def get_current_price(ticker):  # 현재 가격 가져오기

    return pyupbit.get_orderbook(ticker=ticker)['orderbook_units'][0]['ask_price']


def get_balance(currency):  # 잔고 조회
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == currency:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_buy_average(currency):  # 매수평균가
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == currency:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0


def get_trade_time(ticker):  # 최근 거래 채결 날짜 가져오기
    df = pd.DataFrame(upbit.get_order(ticker, state="done"))
    trade_done = df.iloc[0]["created_at"]
    trade_done_time = datetime.datetime.strptime(trade_done[:-6], "%Y-%m-%dT%H:%M:%S")
    return trade_done_time


##########################################################################################################

# 로그인
access = '[ACCESS_KEY]'
secret = '[SECRET_kEY]'

upbit = pyupbit.Upbit(access, secret)
print("Login OK")

# 총 매수 할 원화, 분할 매수 비율
total = 100000
rate30 = 0.3
rate40 = 0.4
rateValue = 0.99

# 시간 간격
interval = "day"

# ticker, currency
ticker = "KRW-GMT"
currency = "KRW"

# 초기 셋팅 (1퍼센트당 매도 10개 / 매수 10개), 코인 수량, 판매 금액
# set_initial_order(ticker)
coin_amount = upbit.get_balance(ticker=ticker)
sell_amount = 0

print(coin_amount)
print(upbit.get_order(ticker))

# 자동 매매 무한반복
while True:
    print(upbit.GetTradesTicks())
    time.sleep(1)
    # 상태 조회


#     # 시간 설정
#     start_time = get_start_time(ticker, interval)
#     now = datetime.datetime.now()
#     end_time = start_time + datetime.timedelta(days=1) - datetime.timedelta(seconds=5)
#     # end_time = start_time + datetime.timedelta(minutes=240) - datetime.timedelta(seconds=5)
#
#     # 매매 시작
#     if start_time < now < end_time:
#
#         print("Start: %s" % (start_time))
#         print("End: %s" % (end_time))
#
#         i = 0
#         while i < 3:
#             now = datetime.datetime.now()
#             current_price = get_current_price(ticker)
#             time.sleep(0.5)
#
#             # 매수 1차
#             if i == 0 and (target_price - 50) <= current_price < (target_price + 100):
#                 upbit.buy_market_order(ticker, total * rate30)
#                 time.sleep(1)
#                 buy_average = get_buy_average(currency)
#                 i += 1
#                 print("%dst Buy OK" % (i))
#
#                 # 매수 2차
#             if i == 1 and current_price < buy_average * rate_minus:
#                 upbit.buy_market_order(ticker, total * rate30)
#                 time.sleep(1)
#                 buy_average = get_buy_average(currency)
#                 i += 1
#                 print("%dnd Buy OK" % (i))
#
#             # 매수 3차
#             if i == 2 and current_price < buy_average * rate_minus:
#                 upbit.buy_market_order(ticker, total * rate40)
#                 time.sleep(1)
#                 buy_average = get_buy_average(currency)
#                 i += 1
#                 print("%drd Buy OK" % (i))
#
#             if now > end_time:
#                 break
#
#     elif now > end_time:
#         coin = get_balance(currency)
#         upbit.sell_market_order(ticker, coin)
#         time.sleep(1)
#         print("Sell OK")