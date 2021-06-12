# About
This project aims to predict stock price using sentiment analysis on articles describing each stock ticker. The articles are scraped from CNBC and Martketwatch, two big finance stories providers. 

# Depositary details

1. train_test_split.py is the script that separates the original results which are in the Labelling result folder (I did not include it here because the files are big)

2. cnbc_train.csv contains 20% of the original result set. The 20% is randomly selected.
   cnbc_test.csv contains the remaining 80%. The label column has been removed in cnbc_test.csv. But it can be generated from the code commented out in the python script.

