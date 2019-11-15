# -*- coding: utf-8 -*-

"""
train_model.

| Trains a collection of new conjugation models.


| The conjugation data conforms to the JSON structure of the files in mlconjug/data/conjug_manager/
| or to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

import mlconjug
import pickle
import pprint
from functools import partial

# Set a language to train the Conjugator on
langs = ('ro', 'it', 'en', 'es', 'fr', 'pt')

managers = (mlconjug.Verbiste, mlconjug.ConjugManager)
results = {}

for lang in langs:
    # Set a ngram range sliding window for the vectorizer
    ngrange = (2, 7)

    # Transforms dataset with CountVectorizer. We pass the function extract_verb_features to the CountVectorizer.
    vectorizer = mlconjug.CountVectorizer(analyzer=partial(mlconjug.extract_verb_features,
                                                           lang=lang,
                                                           ngram_range=ngrange),
                                          binary=True)

    # Feature reduction
    feature_reductor = mlconjug.SelectFromModel(mlconjug.LinearSVC(penalty="l1",
                                                                   max_iter=12000,
                                                                   dual=False,
                                                                   verbose=0))

    # Prediction Classifier
    classifier = mlconjug.SGDClassifier(loss="log",
                                        penalty='elasticnet',
                                        l1_ratio=0.15,
                                        max_iter=40000,
                                        alpha=1e-5,
                                        random_state=42,
                                        verbose=0)

    # Initialize Data Set
    dataset = mlconjug.DataSet(mlconjug.Verbiste(language=lang).verbs)
    dataset.split_data(proportion=0.95)

    # Initialize Conjugator
    model = mlconjug.Model(vectorizer, feature_reductor, classifier)
    conjugator = mlconjug.Conjugator(lang, model)

    # Training and prediction
    conjugator.model.train(dataset.train_input, dataset.train_labels)
    predicted = conjugator.model.predict(dataset.test_input)

    # Assess the performance of the model's predictions
    score = len([a == b for a, b in zip(predicted, dataset.test_labels) if a == b]) / len(predicted)
    print('The score of the {0} model is {1} with the {2} model.'.format(lang, score, managers[0].__name__))

    results[lang] = score

    # Save trained model
    with open('raw_data/experiments/trained_model-{0}-final.pickle'.format(lang), 'wb') as file:
        pickle.dump(conjugator.model, file)
pprint.pprint(results)
