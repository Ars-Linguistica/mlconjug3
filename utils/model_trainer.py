"""
This script demonstrates how to train your own model using the mlconjug3 library. The script uses the ConjugatorTrainer class, which wraps the scikit-learn classifier, feature selector and vectorizer into a single object, making it easy to train, predict and evaluate the model. 

The script starts by importing the necessary modules and setting the parameters for the model.

The parameters are:

- lang: the language of the conjugator. The default language is 'fr' for French.

- output_folder: the location where the trained model will be saved.

- split_proportion: the proportion of the data that will be used for training. The remaining data will be used for testing.

- dataset: the dataset object which contains the data for the model.

- model: the model object which wraps the classifier, feature selector and vectorizer.

Once the parameters are set, the script creates an instance of the ConjugatorTrainer class, passing the parameters as keyword arguments.

The script then calls the train() method on the ConjugatorTrainer object to train the model. This step may take a while, depending on the size of the dataset and the complexity of the model.

Once the model is trained, the script calls the predict() method to make predictions on the test data.

It then calls the evaluate() method to evaluate the model's performance.

Finally, the script saves the model to the specified output folder.

It is important to note that this script uses the default parameters for the model, and these may not be optimal for your specific use case. We recommend experimenting with different parameters and evaluating the model's performance to find the best configuration for your use case.

"""


import mlconjug3
from mlconjug3.feature_extractor import extract_verb_features
from functools import partial

lang = "fr"

params = {'lang': lang,
          'output_folder': "models", 
          'split_proportion': 0.8,
          'dataset': mlconjug3.DataSet(mlconjug3.Verbiste(lang).verbs), 
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
