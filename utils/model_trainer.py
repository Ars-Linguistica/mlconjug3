import mlconjug3
from mlconjug3.feature_extractor import extract_verb_features
from functools import partial

lang = "fr"

verbiste = mlconjug3.Verbiste(lang)

params = {'lang': lang,
          'output_folder': "models", 
          'split_proportion': 0.8,
          'dataset': mlconjug3.DataSet(verbiste.verbs), 
          'model': mlconjug3.Model(
              language=lang,
              vectorizer=mlconjug3.CountVectorizer(analyzer=partial(extract_verb_features, lang=lang, ngram_range=(2, 7)),
                                         binary=True, lowercase=False),
              feature_selector=mlconjug3.SelectFromModel(mlconjug3.LinearSVC(penalty = "l1", max_iter = 12000, dual = False, verbose = 0)), 
              classifier=mlconjug3.SGDClassifier(loss = "log", penalty = "elasticnet", l1_ratio = 0.15, max_iter = 40000, alpha = 1e-5, verbose = 0)
          )
         }

ct = mlconjug3.utils.ConjugatorTrainer(**params)

print("training model...")
ct.train()
print("model has benn trained.")

ct.predict()

print("evaluating model")
ct.evaluate()

print("saving model")
ct.save()
