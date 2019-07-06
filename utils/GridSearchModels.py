# -*- coding: utf-8 -*-

"""
train_model.

| Trains a collection of new conjugation models.


| The conjugation data conforms to the JSON structure of the files in mlconjug/data/conjug_manager/
| or to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""


import logging
import sys
import os
import warnings
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import mlconjug
import json
from pprint import pprint
from functools import partial
from time import time

print(__doc__)



# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


# #############################################################################
# Initialize Data Set
lang = 'fr'
dataset = mlconjug.DataSet(mlconjug.Verbiste(language=lang).verbs)
dataset.construct_dict_conjug()
dataset.split_data(proportion=0.90)

# #############################################################################
# Define a pipeline.

# Transforms dataset with CountVectorizer. We pass the function extract_verb_features to the CountVectorizer.
ngrange = (2, 7)
vectorizer = mlconjug.CountVectorizer(analyzer=partial(mlconjug.extract_verb_features,
                                                       lang=lang,
                                                       ngram_range=ngrange),
                                      binary=True)

# Feature reduction
feature_reductor = mlconjug.SelectFromModel(mlconjug.LinearSVC(random_state=42,
                                                               penalty="l1",
                                                               dual=False,
                                                               verbose=0))

# Prediction Classifier
classifier = mlconjug.SGDClassifier(random_state=42,
                                    verbose=0)

pipeline = Pipeline([
    ('vect', vectorizer),
    ('feat', feature_reductor),
    ('clf', classifier),
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
parameters = {
    'feat__estimator__max_iter': (12000, 8400, 3600, 4800, 6400),
    'feat__estimator__tol': (1e-3, 1e-4, 1e-5),
    'feat__estimator__C': (1e-1, 1),
    'clf__alpha': (0.00001, 0.000001),
    'clf__penalty': ('l2', 'elasticnet'),
    'clf__tol': (1e-3, 1e-4, 1e-5),
    'clf__l1_ratio': (0.15, 0.3, 0.45, 0.6),
    'clf__loss': ('log', 'modified_huber'),
    'clf__max_iter': (30000, 40000, 50000),
}

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block
    if not sys.warnoptions:
        warnings.simplefilter("ignore")
        os.environ["PYTHONWARNINGS"] = "ignore"

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, cv=5,
                               n_jobs=3, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(dataset.train_input, dataset.train_labels)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
    # Save experiments results
    with open('/home/ubuntu/PycharmProjects/mlconjug/utils/raw_data/experiments/results{0}.json'.format(lang), 'w',
              encoding='utf-8') as file:
        json.dump(best_parameters, file, ensure_ascii=False, indent=4)
