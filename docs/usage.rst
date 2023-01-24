=====
Usage
=====

.. NOTE:: The default language is French.
    When called without specifying a language, the library will try to conjugate the verb in French.


Command Line Interface
----------------------

To use mlconjug3 from the command line::

    To conjugate a verb in English, abbreviated subject format :
    $ mlconjug3 -l en -s abbrev 'have'
    
    To conjugate multiple verbs in French, full subject format :
    $ mlconjug3 -l fr -s pronoun 'aimer' 'être' 'aller'
    
    To conjugate a verb in Spanish, full subject format and save the conjugation table in a json file:
    $ mlconjug3 -l es -s pronoun -f json 'hablar' -o 'conjugation_table.json'
    
    To conjugate multiple verbs in Italian, abbreviated subject format and save the conjugation table in a csv file:
    $ mlconjug3 -l it -s abbrev -f csv 'parlare' 'avere' 'essere' -o 'conjugation_table.csv'


Using mlconjug3 in your own code
---------------------------------

This library provides an easy-to-use interface for conjugating verbs using machine learning models.
It includes a pre-trained model for French, English, Spanish, Italian, Portuguese and Romanian verbs,
as well as interfaces for training custom models and conjugating verbs in multiple languages.

The main class of the library is Conjugator, which provides the conjugate() method for conjugating verbs.
The class also manages the Verbiste data set and provides an interface with the scikit-learn pipeline.
The class can be initialized with a specific language and a custom model, otherwise the default language is French
and the pre-trained French conjugation pipeline is used.

The library also includes helper classes for managing verb data, such as VerbInfo and Verb, as well as utility
functions for feature extraction and evaluation.

Using the Conjugator class:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the Conjugator class, you need to first import the class.


.. code-block:: python

    from mlconjug3.conjugator import Conjugator

    conjugator = Conjugator(language='fr')

    conjugations = conjugator.conjugate("aimer")

    conjugations = conjugator.conjugate(["aimer", "aller", "être"])

    conjugations = conjugator.conjugate("aimer", subject='pronoun')


You can also provide your own trained model to the Conjugator class if you have trained a model using the ConjugatorTrainer class. To do this, pass the trained model object as the second argument to the Conjugator class.

For example, if you have trained a French conjugation model and saved it to the file "my_french_model.pickle", you can load this model and use it with the Conjugator class as follows:

.. code-block:: python

    import joblib
    from mlconjug3.conjugator import Conjugator

    # load the trained model from file
    my_french_model = joblib.load("my_french_model.pickle")

    # create an instance of the Conjugator class with the custom model
    conjugator = Conjugator(language='fr', model=my_french_model)

    # conjugate a verb
    conjugations = conjugator.conjugate("aimer")

Note that the Conjugator class expects the model object to have a similar structure as the default model, with the following methods and properties:

The model should have:
    * a fit() method for training the model on a dataset
    * a predict() method for making predictions on new data
    * a '__classes__' property that returns an array of the class labels
As long as your custom model has these properties and methods, it should be compatible with the Conjugator class.


To use mlconjug3 in a project and train a new model:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following sample script demonstrates how to train your own model using the mlconjug3 library.
The script uses the ConjugatorTrainer class, which wraps the scikit-learn classifier,
feature selector and vectorizer into a single object, making it easy to train, predict and evaluate the model. 
    
The script starts by importing the necessary modules and setting the parameters for the model.
    
The parameters are:
    * lang: the language of the conjugator. The default language is 'fr' for French.
    
    * output_folder: the location where the trained model will be saved.
    
    * split_proportion: the proportion of the data that will be used for training. The remaining data will be used for testing.
    
    * dataset: the dataset object which contains the data for the model.
    
    * model: the model object which wraps the classifier, feature selector and vectorizer.
    
Once the parameters are set, the script creates an instance of the ConjugatorTrainer class, passing the parameters as keyword arguments.
    
The script then calls the train() method on the ConjugatorTrainer object to train the model.
This step may take a while, depending on the size of the dataset and the complexity of the model.
    
Once the model is trained, the script calls the predict() method to make predictions on the test data.
    
It then calls the evaluate() method to evaluate the model's performance.
    
Finally, the script saves the model to the specified output folder.
    
It is important to note that this script uses the default parameters for the model, and these may not be optimal for your specific use case.
We recommend experimenting with different parameters and evaluating the model's performance to find the best configuration for your use case.
    
.. code-block:: python

    """
    Script to train a new french Conjugator model
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



In conclusion, the mlconjug3 library provides a simple interface for conjugating verbs using machine learning models, with support for multiple languages and the ability to train custom models.

The main class of the library is the Conjugator, which can be used to conjugate verbs in the supported languages using the pre-trained models, or custom models trained using the ConjugatorTrainer class.
