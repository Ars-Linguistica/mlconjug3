=====
Usage
=====


Command Line Interface
----------------------

Example of using mlconjug3 through a remote ssh connection:


.. image:: https://raw.githubusercontent.com/Ars-Linguistica/mlconjug3/master/docs/images/to_be.png
        :alt: Conjugation for the verb to be.


To see a list of mlconjug3's commands type 'mlconjug3 -h' from the command line:

.. code-block:: console

    $ mlconjug3 -h
    Usage: mlconjug3 [OPTIONS] [VERBS]...

    Examples of how to use mlconjug3 from the terminal
  
    To conjugate a verb in English, abbreviated subject format : $ mlconjug3 -l
    en -s abbrev 'have'
  
    To conjugate multiple verbs in French, full subject format : $ mlconjug3 -l
    fr -s pronoun 'aimer' 'être' 'aller'
  
    To conjugate a verb in Spanish, full subject format and save the conjugation
    table in a json file: $ mlconjug3 -l es -s pronoun -f json 'hablar' -o
    'conjugation_table.json'
  
    To conjugate multiple verbs in Italian, abbreviated subject format and save
    the conjugation table in a csv file: $ mlconjug3 -l it -s abbrev -f json
    'parlare' 'avere' 'essere' -o 'conjugation_table.json'

    Examples of how to use mlconjug3 from the terminal with a config file:

    To use a config file in your home directory:
    $ mlconjug3 -c

    To use a specific config file:
    $ mlconjug3 -c /path/to/config.toml

    To use a specific config file and override some of the settings:
    $ mlconjug3 -c /path/to/config.toml -l en -s pronoun -o conjugation_table.json -f json
  
  Options:
    -l, --language TEXT     The language for the conjugation pipeline. The
                            values can be 'fr', 'en', 'es', 'it', 'pt' or 'ro'.
                            The default value is fr.
    -o, --output TEXT       Path of the filename for storing the conjugation
                            tables.
    -s, --subject TEXT      The subject format type for the conjugated forms.
                            The values can be 'abbrev' or 'pronoun'. The default
                            value is 'abbrev'.
    -f, --file_format TEXT  The output format for storing the conjugation
                            tables. The values can be 'json', 'csv'. The default
                            value is 'json'.
    -c, --config FILE       Path of the configuration file for specifying
                          language, subject, output file name and format, as
                          well as theme settings for the conjugation table
                          columns. Supported file formats: toml, yaml
    -h, --help              Show this message and exit.


.. NOTE:: The default language is French.

    When called without specifying a language, the library will try to conjugate the verb in French.


To conjugate a verb in English, abbreviated subject format :

.. code-block:: console

    $ mlconjug3 -l en -s abbrev 'have'
    

To conjugate multiple verbs in French, full subject format :

.. code-block:: console

    $ mlconjug3 -l fr -s pronoun 'aimer' 'être' 'aller'
    

To conjugate a verb in Spanish, full subject format and save the conjugation table in a json file:

.. code-block:: console

    $ mlconjug3 -l es -s pronoun -f json 'hablar' -o 'conjugation_table.json'
    

To conjugate multiple verbs in Italian, abbreviated subject format and save the conjugation table in a csv file:

.. code-block:: console

    $ mlconjug3 -l it -s abbrev -f csv 'parlare' 'avere' 'essere' -o 'conjugation_table.csv'



Examples of how to use mlconjug3 from the terminal with a config file:

To use a config file in your home directory:

.. code-block:: console

    $ mlconjug3 -c hablar

To use a specific config file:

.. code-block:: console

    $ mlconjug3 -c /path/to/config.toml manger parler

To use a specific config file and override some of the settings:

.. code-block:: console

    $ mlconjug3 -c /path/to/config.toml -l en -s pronoun -o conjugation_table.json -f json have



Using Configuration Files
~~~~~~~~~~~~~~~~~~~~~~~~~

mlconjug3 allows you to specify various settings using configuration files so that you don't have to type them at the command line.
These files can be in either TOML or YAML format and mlcnjug3 will automatically check if a configuration file is located in a directory in your home folder called /mlconjug3/. 
You can also pass the path to your configuration file by using the '-c' option.

Here is an example of a config.toml file:

.. code-block:: toml

    language = "en"
    subject = "abbrev"
    output = "conjugation_table.json"
    file_format = "json"

    [theme]
    header_style = "bold #0D47A1"
    mood_style = "bold #F9A825"
    tense_style = "bold bright_magenta"
    person_style = "bold cyan"
    conjugation_style = "bold #4CAF50"


And here is an example of a config.yamll file:

.. code-block:: yaml

    language: fr
    subject: pronoun
    output: conjugation_table.json
    file_format: json

    theme:
      header_style: bold blue
      mood_style: bold yellow
      tense_style: bold green
      person_style: bold bright_cyan
      conjugation_style: bold bright_magenta



Use mlconjug3 in your own code
------------------------------

This library provides an easy-to-use interface for conjugating verbs using machine learning models.
It includes a pre-trained model for French, English, Spanish, Italian, Portuguese and Romanian verbs,
as well as interfaces for training custom models and conjugating verbs in multiple languages.

The main class of the library is Conjugator, which provides the conjugate() method for conjugating verbs.
The class also manages the Verbiste data set and provides an interface with the scikit-learn pipeline.
The class can be initialized with a specific language and a custom model, otherwise the default language is French
and the pre-trained French conjugation pipeline is used.

The library mlconjug3 also includes helper classes for managing verb data, such as VerbInfo and Verb,
as well as utility functions for feature extraction and evaluation.

Using the Conjugator class:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the Conjugator class, you need to first import the class in your code.


.. code-block:: python
    
    from mlconjug3.conjugator import Conjugator
    
    # initialize the conjugator
    conjugator = Conjugator()
    
    # conjugate the verb "parler"
    verb = conjugator.conjugate("parler")
    
    # print all the conjugated forms as a list of tuples.
    print(verb.iterate())
    
    
The class Verb and it's children adhere to the Python Data Model and can be accessed as a dictionary.
This way you can conveniently access parts of the conjugation either in the form
Verb[mood][tense][person] or the form Verb[(mood, tense, person)].

Using the form Verb[mood][tense][person] to access the conjugated forms:

.. code-block:: python
    
    # get the conjugation for the indicative mood, present tense, first person singular
    print(verb["Indicatif"]["Présent"]["1s"])
    
    # get the conjugation for the indicative mood, present tense
    print(verb["Indicatif"]["Présent"])
    
    # get the conjugation for the indicative mood
    print(verb["Indicatif"])
    
    
Using the form Verb[(mood, tense, person)] to access the conjugated forms:

.. code-block:: python

    # get the conjugation for the indicative mood, present tense, first person singular
    print(verb["Indicatif", "Présent", "1s"])
    
    # get the conjugation for the indicative mood, present tense
    print(verb["Indicatif", "Présent"])
    
    # get the conjugation for the indicative mood
    print(verb["Indicatif"])


You can check if a conjugated form is present in the verb:

.. code-block:: python
    
    # check if the form "je parle" is in the conjugated forms. Prints True.
    print("je parle" in verb)
    
    # check if the form "tu parles" is in the conjugated forms. Prints True.
    print("tu parles" in verb)
    
    # check if the form "parlent" is in the conjugated forms. Prints True.
    print("parlent" in verb)
    
    # check if the form "tu manges" is in the conjugated forms. Prints False.
    print("tu manges" not in verb)
    

You can also access the conjugated forms in the attribute conjug_info

.. code-block:: python
    
    # print all the conjugations for the indicative mood
    print(verb.conjug_info["Indicatif"])
    
    # print the conjugation for the indicative mood, present tense, first person singular
    print(verb.conjug_info["Indicatif"]["Présent"]["1s"])
    
    # print the conjugation for the indicative mood, present tense
    print(verb.conjug_info["Indicatif"]["Présent"])
    
    # print the conjugation for the indicative mood
    print(verb.conjug_info["Indicatif"])
    

Providing a pre-trained model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can provide your own trained model to the Conjugator class if you have trained a model using the ConjugatorTrainer class.
To do this, pass the trained model object as the second argument to the Conjugator class.

For example, if you have trained a French conjugation model and saved it to the file "my_french_model.pickle",
you can load this model and use it with the Conjugator class as follows:

.. code-block:: python

    import joblib
    from mlconjug3.conjugator import Conjugator

    # load the trained model from file
    my_french_model = joblib.load("my_french_model.pickle")

    # create an instance of the Conjugator class with the custom model
    conjugator = Conjugator(language='fr', model=my_french_model)

    # conjugate a verb
    conjugations = conjugator.conjugate("aimer")


Note that the Conjugator class expects the model object to have a similar structure as the default model,
with the following methods and properties.

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
    
Once the parameters are set, the script creates an instance of the ConjugatorTrainer class,
passing the parameters as keyword arguments.
    
The script then calls the train() method on the ConjugatorTrainer object to train the model.
This step may take a while, depending on the size of the dataset and the complexity of the model.
    
Once the model is trained, the script calls the predict() method to make predictions on the test data.
    
It then calls the evaluate() method to evaluate the model's performance.
    
Finally, the script saves the model to the specified output folder.
    
It is important to note that this script uses the default parameters for the model,
and these may not be optimal for your specific use case.
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


Alternatively you can load the model parameters from a yaml file using PyYaml, Hydra or any other library.

Here is an example of a yaml file to store the model settings:


.. code-block:: python

    # config.yaml
    
    language: fr
    
    output_folder: models
    
    split_proportion: 0.8
    
    vectorizer:
        type: mlconjug3.CountVectorizer
        kwargs:
            analyzer: 
                type: functools.partial
                kwargs:
                    func: mlconjug3.feature_extractor.extract_verb_features
                    lang: fr
                    ngram_range: [2, 7]
            binary: true
            lowercase: false
    
    feature_selector:
        type: mlconjug3.SelectFromModel
        kwargs:
            estimator:
                type: mlconjug3.LinearSVC
                kwargs:
                    penalty: l1
                    max_iter: 12000
                    dual: false
                    verbose: 0
    
    classifier:
        type: mlconjug3.SGDClassifier
        kwargs:
            loss: log
            penalty: elasticnet
            l1_ratio: 0.15
            max_iter: 40000
            alpha: 1e-5
            verbose: 0



In conclusion, the mlconjug3 library provides a simple and flexible interface for conjugating verbs using machine learning models, with support for multiple languages and the ability to train custom models.

The main class of the library is the Conjugator, which can be used to conjugate verbs in the supported languages using the pre-trained models, or custom models trained using the ConjugatorTrainer class.
