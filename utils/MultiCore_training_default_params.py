# -*- coding: utf-8 -*-

"""
train_model.

| Trains and ranks a collection of new conjugation models.


| The conjugation data conforms to the JSON structure of the files in mlconjug3/data/conjug_manager/
| or to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

import logging
import sys
import os
import warnings
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import mlconjug3
import joblib
from pprint import pprint
from functools import partial
from time import time
import datetime
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


print(__doc__)

# Displays progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

langs = ('ro', 'it', 'en', 'es', 'pt', 'fr')

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block
    for lang in langs:
        my_file = Path('raw_data/models/Multicore/best_model_{0}.pkl'.format(lang))
        if my_file.is_file():
            continue
        else:
            # #############################################################################
            # Initialize Data Set
            dataset = mlconjug3.DataSet(mlconjug3.Verbiste(language=lang).verbs)
            dataset.split_data(proportion=1)

            # #############################################################################
            # Define a pipeline.

            # Transforms dataset with CountVectorizer. We pass the function extract_verb_features to the CountVectorizer.
            ngrange = (2, 7)
            vectorizer = mlconjug3.CountVectorizer(analyzer=partial(mlconjug3.extract_verb_features,
                                                                    lang=lang,
                                                                    ngram_range=ngrange),
                                                   binary=True)

            # Feature reduction
            feature_reductor = mlconjug3.SelectFromModel(mlconjug3.LinearSVC(random_state=42,
                                                                             penalty="l1",
                                                                             max_iter=12000,
                                                                             dual=False,
                                                                             verbose=0))

            # Prediction Classifier
            classifier = mlconjug3.SGDClassifier(random_state=42,
                                                 loss="log",
                                                 penalty='elasticnet',
                                                 l1_ratio=0.15,
                                                 max_iter=40000,
                                                 alpha=1e-5,
                                                 verbose=0)

            pipeline = Pipeline([
                ('vectoriser', vectorizer),
                ('feature_reductor', feature_reductor),
                ('classifier', classifier),
            ])

            parameters = {
                'feature_reductor__estimator__random_state': (42, ),
                'feature_reductor__estimator__penalty': ('l1', ),
                'feature_reductor__estimator__max_iter': (40000, ),
                'feature_reductor__estimator__dual': (False, ),
                'feature_reductor__estimator__verbose': (0,),
                'classifier__alpha': (1e-5,),
                'classifier__random_state': (42, ),
                'classifier__penalty': ('elasticnet', ),
                'classifier__l1_ratio': (0.15, ),
                'classifier__loss': ('log',),
                'classifier__max_iter': (40000,),
                'classifier__verbose': (0,),
            }

            # ignores CnvergenceWarnings during model selection
            if not sys.warnoptions:
                warnings.simplefilter("ignore")
                os.environ["PYTHONWARNINGS"] = "ignore"

            # find the best parameters for both the feature extraction and the
            # classifier
            grid_search = GridSearchCV(pipeline, parameters, cv=3,
                                       n_jobs=-1, verbose=1,)

            print("Performing grid search for language '{0}' started at {1}...".format(lang, datetime.datetime.now()))
            print("pipeline:", [name for name, _ in pipeline.steps])

            t0 = time()
            grid_search.fit(dataset.verbs_list, dataset.templates_list)
            print("done in %0.3fs" % (time() - t0))
            print()

            print("Best score: %0.3f" % grid_search.best_score_)
            print("Best parameters set:")
            best_estimator = grid_search.best_estimator_

            # Save best model
            with open('raw_data/models/Multicore/best_model_{0}.pkl'.format(lang),
                      'wb') as file:
                joblib.dump(best_estimator, file, compress=('gzip', 6))
            print('\nSaved the best "{0}" model found by the GridSearch as a joblib file.\n'.format(lang))

            # Save best model parameters
            with open('raw_data/experiments/Multicore/best_model_parameters_{0}.pkl'.format(lang),
                      'wb') as file:
                joblib.dump(grid_search.best_params_, file, compress=('gzip', 6))
            print('\nSaved the parameters of the best "{0}" model found by the GridSearch as a joblib file.\n'.format(lang))

    pprint("Done.")
