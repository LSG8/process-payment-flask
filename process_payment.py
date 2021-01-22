'''
@author: Lahari Sengupta
Created on 20.01.21
Main page
'''

from cheapPayment import CheapPayment
from expensivePayment import ExpensivePayment
from premiumPayment import PremiumPayment
import ast, re
import flask
from flask import Flask, render_template, request, redirect, url_for
from flask_api import status

app = Flask(__name__)
app.config.from_pyfile('pay.cfg')

#validates credit card number
def luhn_check(number):  
    sum_val = 0
    number = list(number)
    number = number[::-1]
    number = [int(i) for i in number]
    odds = number[0::2]
    evens = number[1::2]
    sum_val+=sum(odds)
    doubled_evens = [i*2 for i in evens]
    for i in range(len(doubled_evens)):
        if doubled_evens[i]>9:
            doubled_evens[i] = 1+(doubled_evens[i]%10)
    sum_val+=sum(doubled_evens)
    return (sum_val%10 == 0)

#checks user data validity
def valid_request(data):
    return (data['number'].isnumeric() and (len(data['number'])==16) 
        and luhn_check(data['number']) and (data['cvv'].isnumeric() or (len(data['cvv'])==0))
        and ((len(data['cvv'])==0) or (len(data['cvv'])==3)))

#processes data and chooses suitable gateway
@app.route('/process')      
def process():
    data = request.args.get('data', None)
    data_dict = ast.literal_eval(data)
    if data_dict['amount'] <= 20:
        pay_obj = CheapPayment(app,data_dict)
        return(pay_obj.pay())
    elif 20 < data_dict['amount'] <= 500:
        if "EXPENSIVE" in app.config["PAYMENT_GATEWAYS"]:
            pay_obj = ExpensivePayment(app,data_dict)
            return(pay_obj.pay())
        else:
            pay_obj = CheapPayment(app,data_dict)
            return(pay_obj.pay())
    else: 
        pay_obj = PremiumPayment(app,data_dict)
        return(pay_obj.pay())

#home page
@app.route('/')
def home():
    return render_template('index.html')
 
#collects data from user 
@app.route('/datacollect', methods=['POST'])
def datacollect():
    try:
        user_form =  request.form
        number = user_form.get("cardNumber")
        name = user_form.get("cardName")
        exp = user_form.get("expYear")
        cvv = user_form.get("cvv")
        amount = user_form.get("amount")
        data = {"name" : name,"number" : number,"exp" : exp,"cvv" : cvv,"amount" : int(amount)}
        if valid_request(data):
            return redirect(url_for('process',data=data))
        else:
            return "The request is invalid (Not a valid credit card)", status.HTTP_400_BAD_REQUEST
    except:
        return "Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR
    

if __name__ == '__main__':
    app.run()