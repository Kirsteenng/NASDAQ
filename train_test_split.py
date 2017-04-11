#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 18:42:47 2017

@author: Kirsteenng
"""

# TODO: randomly pick 20% of the training set, 80% test
import pandas as pd
from sklearn.model_selection import train_test_split

reuters = pd.read_csv('/Users/Kirsteenng/Desktop/NASDAQ/testresultReuters.csv')
reuters_test, reuters_train = train_test_split(reuters, test_size = 0.2, random_state = 42)
reuters_train.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/reuters_train.csv',encoding='utf-8', header=True, index=False,)
#reuters_test_validate.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/reuters_test_validate.csv',encoding='utf-8', header=True, index=False,)

reuters_test = reuters_test.drop('Label',1)
reuters_test.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/reuters_test.csv',encoding='utf-8', header=True, index=False,)



market = pd.read_csv('/Users/Kirsteenng/Desktop/NASDAQ/testresultMarket.csv')
market_test, market_train = train_test_split(market, test_size = 0.1, random_state = 42)
market_train.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/market_train.csv',encoding='utf-8', header=True, index=False,)
#market_test_validate.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/market_test_validate.csv',encoding='utf-8', header=True, index=False,)


market_test = market_test.drop('Label',1)
market_test.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/market_test.csv',encoding='utf-8', header=True, index=False,)


cnbc = pd.read_csv('/Users/Kirsteenng/Desktop/NASDAQ/testresultCNBC.csv')
cnbc_test, cnbc_train = train_test_split(cnbc, test_size = 0.1, random_state = 42)    
cnbc_train.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/rcnbc_train.csv',encoding='utf-8', header=True, index=False,)
#cnbc_test_validate.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/cnbc_test_validate.csv',encoding='utf-8', header=True, index=False,)


cnbc_test = cnbc_test.drop('Label',1)
cnbc_test.to_csv('/Users/Kirsteenng/Desktop/NASDAQ/cnbc_test.csv',encoding='utf-8', header=True, index=False,)
              



            
        
    
        