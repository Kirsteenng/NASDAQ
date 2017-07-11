1. parsing_CNBC.py and reuters_parsing.py serve the purpose of parsing .json files that contain article contents from CNBC and Reuters articles which have been crawled using scripts from the crawler folder.

2. The .json files will be read into Pandas DataFrame using built-in function **pd.read_json()**. Each article is now a record in the Dataframe structure. Each record will be lemmatized using Python's NLTK package. Specific stopwords will also be removed from the dataframe. 

3. In the main for-loop(line 151), each record is being filtered using the function **search()** and only keywords remained in the dataframe. Using SentiWordNet, each article was being labelled a score. The scores and the keywords will then be used for Naive Bayes Classification for the article in the second part of the project.
