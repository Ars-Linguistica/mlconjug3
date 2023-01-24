import mlconjug3
from mlconjug.feature_extractor import extract_verv_features
from functools import partial

lang = "fr"

params = {'lang': lang,
          'output_folder': "models", 
          'split_proportion': 0.8,
          'dataset': mlconjug3.DataSet, 
          'model': mlconjug3.Model(
              language=lang,
              vectorizer=CountVectorizer(analyzer=partial(extract_verb_features, lang=lang, ngram_range=(2, 7)),
                                         binary=True, lowercase=False)
              feature_selector=mlconjug3.SelectFromModel(mlconjug3.LinearSVC(penalty = "l1", max_iter = 12000, dual = False, verbose = 0)), 
              classifier=mlconjug3.SGDClassifier(loss = "log", penalty = "elasticnet", l1_ratio = 0.15, max_iter = 40000, alpha = 1e-5, verbose = 0)
          )
         }

ct = mlconjug3.utils.ConjugatorTrainer(**params)

ct.train()
ct.predict()
ct.evaluate()
ct.save()
