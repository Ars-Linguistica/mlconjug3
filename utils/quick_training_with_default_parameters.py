import multiprocessing
import mlconjug3
import pickle
import numpy as np
from functools import partial
from time import time

np.random.seed(42)

# Set languages to train the Conjugator on
langs = ("ro", "it", "en", "es", "fr", "pt")

# Initialize Data Sets
datasets = {
    lang: mlconjug3.DataSet(mlconjug3.Verbiste(language=lang).verbs) for lang in langs
}
for dataset in datasets.values():
    dataset.split_data(proportion=1)

# Initialize Conjugators
conjugators = {
    lang: mlconjug3.Conjugator(
        lang,
        mlconjug3.Model(
            mlconjug3.CountVectorizer(
                analyzer=partial(
                    mlconjug3.extract_verb_features, lang=lang, ngram_range=(2, 7)
                ),
                binary=True,
            ),
            mlconjug3.SelectFromModel(
                mlconjug3.LinearSVC(penalty="l1", max_iter=12000, dual=False, verbose=0)
            ),
            mlconjug3.SGDClassifier(
                loss="log",
                penalty="elasticnet",
                l1_ratio=0.15,
                max_iter=40000,
                alpha=1e-5,
                verbose=0,
            ),
        ),
    )
    for lang in langs
}

# Train Conjugators with multiprocessing
with multiprocessing.Pool() as pool:
    results = pool.starmap(
        lambda conjugator, dataset: conjugator.model.train(
            dataset.verbs_list, dataset.templates_list
        ),
        [(conjugators[lang], datasets[lang]) for lang in langs],
    )

# Print training duration
for lang, result in zip(langs, results):
    print(f"{lang} model trained on full data set in {result} seconds.")

# Make predictions
predictions = {
    lang: conjugators[lang].model.predict(datasets[lang].verbs_list) for lang in langs
}

# Assess the performance of the model's predictions
for lang, prediction in predictions.items():
    score = len(
        [a == b for a, b in zip(prediction, datasets[lang].templates_list) if a == b]
    ) / len(prediction)
    misses = len(
        [a != b for a, b in zip(prediction, datasets[lang].templates_list) if a != b]
    )
    entries = len(prediction)
    print(
        f"The score of the {lang} model is {score} with {misses} misses out of {entries} entries."
    )

