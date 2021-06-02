from random import randrange

import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.downloader.download('vader_lexicon')

quotes = None


def quote_setup(quotes_path):
    global quotes

    # load the csv file

    quotes = pd.read_csv(quotes_path)

    # instantiate SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    compounds_list = []

    # loops through each score and assign the value to a list
    for sentence in quotes['quote']:
        scores = sia.polarity_scores(sentence)
        for score in sorted(scores):
            if score == 'compound':
                compounds_list.append(scores[score])

    # add the quotes polarity score to quote
    quotes['sentiment_score'] = compounds_list

    # Sort with sentiment score from lower to higher
    quotes = quotes.sort_values('sentiment_score')

    # Add indexes to quotes
    quotes['index'] = [index for index in range(len(quotes))]

    return quotes


def get_a_quote(direction=None, current_index=None):
    global max_index
    random_index = randrange(max_index)
    brighter = None
    darker = None

    if current_index is None:
        brighter = random_index

    if direction == 'brighter':
        brighter = current_index
    else:
        darker = current_index

    if darker is not None:
        current_index = random_index
        try:
            current_index = int(darker)
        except ValueError:
            # Someone is tampering with System
            current_index = random_index

        if current_index > 0:
            # Which means there are darker index possible
            random_index = randrange(0, current_index)
            print("Darker")
        else:
            print("Already at darkest")
            random_index = random_index
    elif brighter is not None:
        try:
            current_index = int(brighter)
        except ValueError:
            # Someone is tampering with System
            current_index = random_index
        if current_index < max_index - 1:
            # Which means there are darker index possible
            random_index = randrange(current_index, max_index)
            print("Brighter")
        else:
            print("Already brightest")
            random_index = random_index
    else:
        random_index = random_index
    return random_index


if __name__ == '__main__':
    quote_setup('quotes_path.csv')
    print(quotes)
    max_index = np.max(quotes['index'].values)
    index = quotes['index'] == get_a_quote("darker", 10)
