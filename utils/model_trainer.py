import mlconjug3
from functools import partial

ct = ConjugatorTrainer(
    lang = "fr", 
    output_folder = "raw_data/experiments", 
    split_proportion = 1, 
    feature_extractor = mlconjug3.CountVectorizer(analyzer=partial(mlconjug3.extract_verb_features, lang= "fr", ngram_range=(2, 7)), binary=True), 
    DataSet = mlconjug3.DataSet, 
    Model = mlconjug3.Model(
        mlconjug3.SelectFromModel(mlconjug3.LinearSVC(penalty = "l1", max_iter = 12000, dual = False, verbose = 0)), 
        mlconjug3.SGDClassifier(loss = "log", penalty = "elasticnet", l1_ratio = 0.15, max_iter = 40000, alpha = 1e-5, verbose = 0)
    )
)
ct.train()
ct.predict()
ct.evaluate()
ct.save()
