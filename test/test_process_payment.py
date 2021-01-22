'''
@author: Lahari Sengupta
Created on 22.01.21
Test application
'''

import pytest
import sys, os, inspect
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
import process_payment as m

from flask import Flask


class TestApp():

    def test_home(self):
        response = m.app.test_client().get('/')
        assert response.status_code == 200
        
    def test_valid_request1(self, data=dict(name='abc asd',number='1234',exp='2021-04',cvv='',amount='56')):
        result = m.valid_request(data)
        assert result == False
        
    def test_valid_request2(self, data=dict(name='abc asd',number='1234123412341234',exp='2021-04',cvv='',amount='56')):
        result = m.valid_request(data)
        assert result == False
        
    def test_valid_request3(self, data=dict(name='abc asd',number='4318711136979995',exp='2021-04',cvv='',amount='56')):
        result = m.valid_request(data)
        assert result == True
    
    def test_valid_request4(self, data=dict(name='abc asd',number='4318711136979995',exp='2021-04',cvv='654',amount='56')):
        result = m.valid_request(data)
        assert result == True
        
    def test_valid_request5(self, data=dict(name='abc asd',number='4318711136979995',exp='2021-04',cvv='64',amount='56')):
        result = m.valid_request(data)
        assert result == False
        
    def test_valid_request6(self, data=dict(name='abc asd',number='4318711136979995',exp='2021-04',cvv='sed',amount='56')):
        result = m.valid_request(data)
        assert result == False
        
    def test_valid_request7(self, data=dict(name='abc asd',number='abcdabcdabcdabcd',exp='2021-04',cvv='',amount='56')):
        result = m.valid_request(data)
        assert result == False
        