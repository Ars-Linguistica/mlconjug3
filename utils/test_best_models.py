import logging
import sys
import os
import warnings
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import mlconjug
import joblib
from pprint import pprint
from functools import partial
from time import time
import datetime
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


# langs = ('ro', 'it', 'en', 'es', 'fr', 'pt')
langs =  ('ro', 'fr')

for lang in langs:
    with open('raw_data/models/best_model_{0}.pkl'.format(lang), 'rb') as file:
        best_model = joblib.load(file)

    # Save best model parameters
    with open('raw_data/experiments/best_model_parameters_{0}.pkl'.format(lang),
              'rb') as file:
        best_params = joblib.load(file)

    dataset = mlconjug.DataSet(mlconjug.Verbiste(language=lang).verbs)
    dataset.split_data(proportion=0.95)

    predicted = best_model.predict(dataset.test_input)
    predicted2 = best_model.predict(dataset.verbs_list)

    score = len([a == b for a, b in zip(predicted, dataset.test_labels) if a == b]) / len(predicted)
    print('The score of the {0} model trained on the train set is {1} on test set.'.format(lang, score))

    score2 = len([a == b for a, b in zip(predicted2, dataset.templates_list) if a == b]) / len(predicted2)
    print('The score of the {0} model trained on the train set is {1} on full dataset.'.format(lang, score2))
    print('ok')

print('ok')
