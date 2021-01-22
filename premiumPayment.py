'''
@author: Lahari Sengupta
Created on 20.01.21
Premium payment class
'''

from payment import Payment
import urllib
from flask import render_template, redirect

class PremiumPayment(Payment):

    def __init__(self, app, data):
        self.data = data
        self.app = app
        self.url =  app.config['PREMIUM_PAYMENT_URL']
    
    def pay(self):
        print("Premium payment")
        server_url = self.app.config['SERVER_NAME']
        self.data['RETURNURL'] = server_url +'/success' #after payments, returns here
        updated_url = self.url+urllib.parse.urlencode(self.data)
        for i in range(3):
            try:
                return(redirect(updated_url,code=307)) #redirects to payment gateway
            except:
                continue #tries three times
        return(render_template('fail.html')) #if payment fails