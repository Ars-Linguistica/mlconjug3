# -*- coding: utf-8 -*-

"""
train_model.

| Trains a collection of new conjugation models.


| The conjugation data conforms to the JSON structure of the files in mlconjug/data/conjug_manager/
| or to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

from sklearn.exceptions import ConvergenceWarning
import warnings

import mlconjug
import pickle
import json
from pprint import pprint
from functools import partial
from collections import defaultdict
# from tabulate import tabulate
from time import time

# Set a language to train the Conjugator on
langs = ('en', 'es', 'fr', 'it', 'pt', 'ro')
reductor_tols = (1e-3, 1e-4, 1e-5)
classifier_tols = (1e-3, 1e-4, 1e-5)
feature_reductor_max_iter = (3600, 4800, 6400)

managers = (mlconjug.Verbiste, mlconjug.ConjugManager)
results = defaultdict(dict)
start = time()
experiment = 0

for red_tol in reductor_tols:
    for class_tol in classifier_tols:
        for feat_max_iter in feature_reductor_max_iter:
            for lang in langs:
                max_score = 0
                for manager in managers:

                    # Set a ngram range sliding window for the vectorizer
                    ngrange = (2, 7)

                    # Transforms dataset with CountVectorizer. We pass the function extract_verb_features to the CountVectorizer.
                    vectorizer = mlconjug.CountVectorizer(analyzer=partial(mlconjug.extract_verb_features,
                                                                           lang=lang,
                                                                           ngram_range=ngrange),
                                                          binary=True)

                    # Feature reduction
                    feature_reductor = mlconjug.SelectFromModel(mlconjug.LinearSVC(penalty="l1",
                                                                                   max_iter=feat_max_iter,
                                                                                   dual=False,
                                                                                   verbose=0,
                                                                                   tol=red_tol))

                    # Prediction Classifier
                    classifier = mlconjug.SGDClassifier(loss="log",
                                                        penalty='elasticnet',
                                                        l1_ratio=0.15,
                                                        max_iter=40000,
                                                        alpha=1e-5,
                                                        random_state=42,
                                                        verbose=0,
                                                        tol=class_tol)

                    # Initialize Data Set
                    dataset = mlconjug.DataSet(manager(language=lang).verbs)
                    dataset.construct_dict_conjug()
                    dataset.split_data(proportion=0.90)

                    # Initialize Conjugator
                    model = mlconjug.Model(vectorizer, feature_reductor, classifier)
                    model_parameters = {'feature_reductor_tol': red_tol,
                                        'classifier_tol': class_tol,
                                        'feature_reductor_max_iter': feat_max_iter}
                    conjugator = mlconjug.Conjugator(lang, model)

                    # Training and prediction
                    with warnings.catch_warnings(record=True) as w:
                        model_start = time()
                        conjugator.model.train(dataset.train_input, dataset.train_labels)
                        predicted = conjugator.model.predict(dataset.test_input)
                        model_duration = round(time() - model_start, 3)
                        if w:
                            caught_warnings = [warning._category_name for warning in w]
                        else:
                            caught_warnings = False

                    # Assess the performance of the model's predictions
                    score = len([a == b for a, b in zip(predicted, dataset.test_labels) if a == b]) / len(predicted)
                    if score > max_score:
                        max_score = score
                    results[lang][manager.__name__] = {'language': lang,
                                                       'manager': manager.__name__,
                                                       'score': score,
                                                       'model_training_duration': str(model_duration) + ' seconds.',
                                                       'model_parameters': model_parameters,
                                                       'current_max_score': max_score,
                                                       'warnings': caught_warnings}
                    pprint(results[lang][manager.__name__])

                    # # Save trained model
                    # with open('/home/ubuntu/PycharmProjects/mlconjug/utils/raw_data/experiments/trained_model-{0}- {1}.pickle'.format(lang, manager), 'wb') as file:
                    #     pickle.dump(conjugator.model, file)

                    # Save experiments results
                    with open('/home/ubuntu/PycharmProjects/mlconjug/utils/raw_data/experiments/results.json', 'w', encoding='utf-8') as file:
                        json.dump(results, file, ensure_ascii=False, indent=4)
                    print('Saved experiments data to json file.')
            results[lang]['max_score'] = {'max_score': max_score, 'manager': manager.__name__, 'model_parameters': model_parameters}
duration = round(time() - start, 3)
print('The training took {0} seconds in total.'.format(duration))
pprint(results)
