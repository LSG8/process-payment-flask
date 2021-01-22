'''
@author: Lahari Sengupta
Created on 20.01.21
Cheap payment class
'''
from payment import Payment
import urllib
from flask import render_template, redirect

class CheapPayment(Payment):

    def __init__(self, app, data):
        self.data = data
        self.app = app
        self.url =  app.config['CHEAP_PAYMENT_URL']
    
    def pay(self):
        print("Cheap payment")
        server_url = self.app.config['SERVER_NAME']
        self.data['RETURNURL'] = server_url +'/success' #after payments, returns here
        updated_url = self.url+urllib.parse.urlencode(self.data)
        try:
            return(redirect(updated_url,code=307)) #redirects to payment gateway
        except:
            return(render_template('fail.html')) #if payment fails