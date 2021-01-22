'''
@author: Lahari Sengupta
Created on 20.01.21
Abstract Payment class
'''

from abc import ABC, abstractmethod


class Payment(ABC):
    
    @abstractmethod
    def pay(self):
        pass