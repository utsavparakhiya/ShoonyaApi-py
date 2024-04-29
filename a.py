from NorenRestApiPy.NorenApi import  NorenApi
import pandas as pd

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
        global api
        api = self

import logging
import pyotp

#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = ShoonyaApiPy()
token = "YP5547Q565DAT5753NBH54K72J234SC5"
otp = pyotp.TOTP(token).now()
#credentials
user    = 'FA178801'
pwd     = 'Uts@v302001'
factor2 = otp
vc      = 'FA178801_U'
apikey  = '6e36d5954503b5d18e6d6059461febe1'
imei    = 'abc1234'


ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=apikey, imei=imei)
# print(api.searchscrip("NFO", "NIFTY18JAN24C18500"))

ret = api.place_order(buy_or_sell='B', product_type='C',
                        exchange='NSE', tradingsymbol='CANBK-EQ', 
                        quantity=1, discloseqty=0,price_type='SL-LMT', price=200.00, trigger_price=199.50,
                        retention='DAY', remarks='my_order_001')
   
 