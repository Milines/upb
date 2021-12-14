import requests
import json
import pandas as pd
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import time


def coins(current):
    url = "https://api.upbit.com/v1/market/all?isDetails=false"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    response_json=json.loads(response.text)

    krw=[]
    btc=[]
    usdt=[]

    for a in response_json:
        if "KRW-" in a['market']:
            krw.append(a['market'])
        elif "BTC-" in a['market']:
            btc.append(a['market'])
        elif "USDT-" in a['market']:
            usdt.append(a['market'])

    tickers={
        "KRW":krw,
        "BTC":btc,
        "USDT":usdt
    }

    return tickers[current]
  

def coin_price(coin):
    url = "https://api.upbit.com/v1/orderbook?markets="+coin
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    response_json=json.loads(response.text)
    current_price=response_json[0]['orderbook_units'][0]['ask_price']
    return current_price
  
def coin_history(coin,time1='minutes',time2=''):
    url = f"https://api.upbit.com/v1/candles/{time1}/{time2}?market={coin}&count=200"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    response_json=json.loads(response.text)
    df=pd.DataFrame(response_json)
    return df
  
def login():
    global access_key
    global secret_key
    access_key=input("access_key : ")
    secret_key=input("secret_key : ")
    
#     ----------------------

def balance():
    server_url ="https://api.upbit.com"
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
    return res.json()

def buy_limit(coin,volume,price):
    server_url = "https://api.upbit.com"
    query = {
        'market': coin,
        'side': 'bid',
        'volume': volume,
        'price': price,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(res.json())
    return res.json()
  
def buy_market(coin,price):
    server_url = "https://api.upbit.com"
    query = {
        'market': coin,
        'side': 'bid',
        'volume': '',
        'price': price,
        'ord_type': 'price',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(res.json())
    return res.json()
  
def sell_limit(coin,volume,price):
    server_url = "https://api.upbit.com"        
    query = {
        'market': coin,
        'side': 'ask',
        'volume': volume,
        'price': price,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(res.json())
    return res.json()
  
def sell_market(coin,volume):
    server_url = "https://api.upbit.com"
    query = {
        'market': coin,
        'side': 'ask',
        'volume': volume,
        'price': '',
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(res.json())
    return res.json()
  
def price_trim(price_trim):
    if price_trim<10:
        price_trim=round(price_trim,2)
    elif price_trim<100:
        price_trim=round(price_trim,1)
    elif price_trim<1000:
        price_trim=round(price_trim)
    elif price_trim<10000:
        price_trim=round(price_trim*2,-1)/2
    elif price_trim<100000:
        price_trim=round(price_trim,-1)
    elif price_trim<500000:
        price_trim=round(price_trim*2,-2)/2        
    elif price_trim<1000000:
        price_trim=round(price_trim,-2)
    elif price_trim<2000000:
        price_trim=round(price_trim*2,-3)/2
    else:
        price_trim=round(price_trim,-3)
    return price_trim
  
#   --------------------------------

while True:
    try:
        tickers=coins("KRW")
        decrease_top_score=0.001

        for a in tickers:
            time.sleep(1)
            print(f"{a} {tickers.index(a)+1}/{len(tickers)} 진행중입니다")
            coin_1_m=coin_history(a,'minutes',1)
            max_high_price=coin_1_m["high_price"].max() #값들중 가장 큰 가격 출력
            now_price=coin_price(a)
            decrease_percent=round(((1-(now_price/max_high_price))*100),3)
            if decrease_percent>decrease_top_score:
                decrease_top_score=decrease_percent
                decrease_top_score_ticker=[a,max_high_price,now_price,(-1)*decrease_percent]
        print(decrease_top_score_ticker)       

        for a in balance():
            if a['currency']=="KRW":
                print(a['balance'])
                buy_amount=float(a['balance'])*0.10
                print(round(buy_amount,-2))
                buy_amount=round(buy_amount,-2)
        buy_market(decrease_top_score_ticker[0],buy_amount)
        time.sleep(3)
        
        sell_price=price_trim(coin_price(decrease_top_score_ticker[0])*1.02)
        for a in balance():
            if a['currency']==decrease_top_score_ticker[0].replace("KRW-",""):
                sell_balance=a['balance']
        sell_limit(decrease_top_score_ticker[0],sell_balance,sell_price)
        time.sleep(180)
    except:
        time.sleep(180)
