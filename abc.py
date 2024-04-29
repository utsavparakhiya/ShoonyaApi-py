#!/usr/bin/env python
# coding: utf-8

# In[70]:


from NorenRestApiPy.NorenApi import  NorenApi
import pandas as pd

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
        global api
        api = self


# In[71]:


import pyotp


api = ShoonyaApiPy()


# In[72]:


token = "YP5547Q565DAT5753NBH54K72J234SC5"
otp = pyotp.TOTP(token).now()
user    = 'FA178801'
pwd     = 'Uts@v302001'
factor2 = otp
vc      = 'FA178801_U'
apikey  = '6e36d5954503b5d18e6d6059461febe1'
imei    = 'abc1234'


# In[73]:



ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=apikey, imei=imei)


# In[74]:


from time import sleep
import time
import datetime
from datetime import datetime,timedelta

feed_opened = False
socket_opened = False
feedJson={}


# In[75]:


def event_handler_feed_update(tick_data):
    UPDATE = False
    if 'tk' in tick_data:
        token = tick_data['tk']
        timest = datetime.fromtimestamp(int(tick_data['ft'])).isoformat()
        feed_data = {'tt': timest}
        if 'lp' in tick_data:
            feed_data['ltp'] = float(tick_data['lp'])
        if 'ts' in tick_data:
            feed_data['Tsym'] = str(tick_data['ts'])
        if 'oi' in tick_data:
            feed_data['openi'] = float(tick_data['oi'])
        if 'poi' in tick_data:
            feed_data['pdopeni'] = str(tick_data['poi'])
        if 'v' in tick_data:
            feed_data['Volume'] = str(tick_data['v'])     
        if feed_data:
            UPDATE = True
            if token not in feedJson:
                feedJson[token] = {}
            feedJson[token].update(feed_data)
        if UPDATE:
             pass

def event_handler_order_update(order_update):
    pass#print(f"order feed {order_update}") 

def open_callback():
    global feed_opened
    feed_opened = True
    print("Websocket opened")

def setupWebSocket():
    global feed_opened
    print("waiting for socket opening")
    api.start_websocket(order_update_callback=event_handler_order_update,
                         subscribe_callback=event_handler_feed_update, 
                         socket_open_callback=open_callback)    
    while(feed_opened==False):        
        pass


# In[76]:


setupWebSocket()


# In[77]:


def get_expiry_dates(exchange, symbol):
    import re
    import datetime
    sd = api.searchscrip(exchange, symbol)
    sd = (sd['values'])
    tsym_values = [Symbol['tsym'] for Symbol in sd]
    dates = [re.search(r'\d+[A-Z]{3}\d+', tsym).group() for tsym in tsym_values]
    formatted_dates = [datetime.datetime.strptime(date, '%d%b%y').strftime('%Y-%m-%d') for date in dates]
    sorted_formatted_dates = sorted(formatted_dates)
    sorted_dates = [datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d%b%y').upper() for date in sorted_formatted_dates]
    expiry_dates = sorted_dates
    return expiry_dates


# In[78]:


expiry_date = get_expiry_dates('NFO', 'NIFTY')[0]
print(expiry_date)


# In[79]:



ret = api.get_quotes(exchange='NSE', token='26000')
ltp = ret.get("lp")
ltp = float(ltp)
ltp_str = str(ltp)
sym = ret.get("symname")
TYPE = "P"
Strike = int(round(ltp/50,0)*50)
For_token = sym+expiry_date+TYPE+str(Strike)
optionchain = api.get_option_chain('NFO', For_token , Strike, 20)
optionchainsym = (optionchain['values'])
for Symbol in optionchainsym:
     (Symbol['token']) 
    
token= [Symbol['token'] for Symbol in optionchainsym]
modified_tokens = []
for Symbol in optionchainsym:
    token = Symbol['token']
    modified_token = 'NFO|' + token
    modified_tokens.append(modified_token)

print(modified_tokens)


# In[80]:



def get_closest_ltp_symbols(ltp_value):
    api.subscribe(modified_tokens)
    df = pd.DataFrame()
    while df.empty:
        df = pd.DataFrame.from_dict(feedJson,orient='index', columns=['ltp', 'Tsym','openi','pdopeni'])
    import pdb
    pdb.set_trace()
    df['diff'] = abs(df['ltp'] - ltp_value)
    df_c = df[df['Tsym'].str.contains('C')]
    df_p = df[df['Tsym'].str.contains('P')]
    min_diff_c = df_c['diff'].min()
    min_diff_p = df_p['diff'].min()
    closest_symbols_c = df_c[df_c['diff'] == min_diff_c]['Tsym'].values[0]
    closest_symbols_p = df_p[df_p['diff'] == min_diff_p]['Tsym'].values[0]
    api.unsubscribe(modified_tokens)
    return closest_symbols_c, closest_symbols_p


# In[82]:
# sleep(5)
try:
    closest_symbols_c, closest_symbols_p = get_closest_ltp_symbols(600)
except Exception as e:
    pass

closest_symbols_c, closest_symbols_p = get_closest_ltp_symbols(600)
print(closest_symbols_c)
print(closest_symbols_p)


# In[83]:


ret = api.place_order(buy_or_sell='B', product_type='C',
                        exchange='NSE', tradingsymbol='CANBK-EQ', 
                        quantity=1, discloseqty=0,price_type='SL-LMT', price=200.00, trigger_price=199.50,
                        retention='DAY', remarks='my_order_001')


# In[ ]:




