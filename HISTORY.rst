=======
History
=======

3.10.0 (2023-26-01)
-------------------

We are excited to announce the release of mlconjug3 version 3.10! This release brings a number of new features and improvements to make your experience even better.

* Config files for ease of use of the command line: You can now use config files to specify your preferences for the command line interface. This allows you to easily set your language, subject, output file, and file format, as well as customize the styling of the conjugation table.
* Caching of xml conjugation files for faster loading: We have implemented caching of the xml conjugation files, which will greatly speed up the loading time of the conjugator.
* Complete overhaul of the documentation: We have completely overhauled the documentation for mlconjug3, making it more comprehensive and user-friendly.
* Signed release using sigstore: We have signed this release using sigstore_, which ensures that the release has not been tampered with and comes from a trusted source.

.. _sigstore: https://www.sigstore.dev

3.9.0 (2023-24-01)
------------------

* Added support for Python 3.11
* Updated dependencies to scikit-learn 1.2.0 with a noticeable speed inrease in training and inference performance.
* Added ConjugatorTrainer class to easily and flexibly train new conjugators.
* Added support for the rich library for better visuals. Now the conjugation tables are pretty printed, themed and formatted.
* Added multi-processing conjugation of multiple verbs for better performance on server applications using mlconjug3.
* Added LRU cache to the the Conjugator.conjugate() method for better performance on applications with long running time.
* Updated documentation with the new classes and more detailed information and visuals.
* Refactor of internal classes, but keeping the same public interface in preparation for mlconjug3 v4.

3.8.3 (2022-01-03)
------------------

* Tweaked optimal learning parameters for the various language models.
* Project Metadata in pyproject.toml file for building the package from source is 100% compliant.
* Migrated build system to poetry/ PyPa build.
* Updated dependencies to scikit-learn 1.0.2 with a noticeable speed inrease in training and inference performance.
* Updated documentation.

3.8.2 (2021-28-10)
------------------

* Fixed issue with the pyproject.toml file which caused the dependency solver to fail on install when using pip instead of poetry.

3.8.1 (2021-28-10)
------------------

* Updated documentation and Package metadata.

3.8.0 (2021-28-10)
------------------

* Fixed bug that would silently skip uppercase characters in the CountVectorizer. See: https://github.com/scikit-learn/scikit-learn/pull/19401
* Retrained all models with fixed CountVectorizer.
* Added full support for pyproject.toml file for building the package from source.
* Migrated build system to poetry.
* Updated dependencies.
* Updated documentation.

3.7.22 (2021-22-10)
-------------------

* Fixed typo in requirements specification.

3.7.21 (2021-22-10)
-------------------

* Retrained all models with scikit-learn 1.0.
* Updated documentation.
* Updated dependencies.
* Removed support for python 3.6.

3.7.20 (2021-04-05)
-------------------

* Retrained all models with scikit-learn 0.24.2
* The Portuguese model has improved and is now also at 99%+ accuracy.
* Updated documentation.
* Updated dependencies.

3.7.19 (2021-25-04)
-------------------

* Unknown verb inference is now faster.
* Added more tests to the test suite.
* Automated setup.py dependency injection.
* Updated documentation.
* Updated dependencies.

3.7.17 (2021-18-04)
-------------------

* | Added new `GitHub Actions Workflows`_ to automatically build, install and test mlconjug3
  | on Windows-x64, MacOs-x64 and Linux-x64 for maximum copmatibilty.
  | The package should build and install even on the newest MacBook with an Apple ARM M1 processor
  | by installing mlconjug3 through conda_ instead of pip:

.. code-block:: console

    $  conda install -c conda-forge mlconjug3

* Updated the documentation to make it clearer.
* Updated development dependencies.

3.7.16 (2021-16-04)
-------------------

* Added support for pipenv environments.
* | Added mlconjug3 to conda-forge_.
  | It is especially useful if you want to install mlconjug3 on a MacBook with an Apple M1 processor.
* Now mlconjug3 can be installed using:

.. code-block:: console

    $  conda install -c conda-forge mlconjug3

* Updated documentation.
* Updated dependencies.


.. _`GitHub Actions Workflows`: https://github.com/Ars-Linguistica/mlconjug3/actions
.. _conda: https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html
.. _conda-forge: https://anaconda.org/conda-forge/

3.7.15 (2021-15-04)
-------------------

* Updated documentation.
* Updated dependencies.

3.7.14 (2021-14-04)
-------------------

* Updated documentation.
* Retrained all models with scikit-learn 0.24.1
* Updated dependencies.

3.7.13 (2020-14-10)
-------------------

* Updated documentation.
* Fixed issue#89.
* Added more examples
* Updated dependencies.

3.7.12 (2020-08-10)
-------------------

* Updated documentation.
* Added code highnliting for examples.
* Added more examples
* Updated dependencies.

3.7.11 (2020-21-09)
-------------------

* Updated documentation.
* Updated dependencies.

3.7.10 (2020-12-09)
-------------------

* Fixed errors in English training corpus.
* Retrained English model.
* Updated dependencies.

3.7.9 (2020-30-08)
------------------

* Added Bibtex entry for easier citation in academic publication.

3.7.8 (2020-26-08)
------------------

* Fixed issue #79: Repeated person keys in English present continuous.
* Now the 'person' key of the conjugated forms dictionary can be consistently accessed by [person] for all moods and tenses for a more consistent API.

3.7.7 (2020-24-08)
------------------

* Fixed issue #65 : Infinitive inserted before some conjugated English verbs.
* Fixed issue #66 : Some spanish verbs were not conjugated correctly.
* Retrained all models with scikit-learn 0.23.2.
* Updated dependencies.
* Optimized code to train and predict faster.

3.7.6 (2020-17-05)
------------------

* Fixed issue #47 and #48 where some English and Spanish verbs were not conjugated correctly.
* Fixed issue #50 dealing with some spurious data for Spanish.
* Updated dependencies.

3.7.5 (2020-03-05)
------------------

* Updated the documentation.

3.7.4 (2020-03-05)
------------------

* Fixed issue #44 where Spanish gerunds were not conjugated properly.
* Updated dependencies.

3.7.3 (2020-30-04)
------------------

* Updated the documentation.

3.7.2 (2020-30-04)
------------------

* Fixed issue with package renaming.
* Fixed bug with Portuguese verbs ending in 'ar'.
* Retrained all models with scikit-learn 0.22.2.

3.7.1 (2020-29-01)
------------------

* Updated the pre-trained models for better accuracy (Now all models have more than 99.9% accuracy) .
* Added new utilities for model training and persistence.
* Now all training and GridSearch results are reproducible from run to run.
* Retrained all models with scikit-learn 0.22.1.
* Corrected mutliple edge cases and enlarged the test suite.

3.6.1 (2019-28-11)
------------------

* Updated the pre-trained models for better accuracy (Now all models have more than 99.9% accuracy) .
* Added new utilities for model training and persistence.
* Now all training and GridSearch results are reproducible from run to run.
* Updated development dependencies.

3.6.0 (2019-14-11)
------------------

* Updated scikit-learn dependency to 0.21.3.
* Updated other dependencies.

3.5.1 (2019-18-07)
------------------

* Fixed bug in issue #80 and #81 reported by @rongybika and @NoelHVincent.
* Added new option '-o' to the CLI allowing to specify output file to save results to json file.
* Use logging instead of print() whenever appropriate.
* Use joblib for model persistence instead.
* Updated Type declarations.
* Added more tests in the test-suite.
* Implemented results_parser to select and train the best performing models.
* Implemented multicore grid search.
* Display prettier output in the CLI.
* Updated scikit-learn dependency.
* Updated other dependencies.

3.4 (2019-29-04)
------------------

* Fixed bug when verbs with no common roots with their conjugated form get their root inserted as a prefix.
* Added the method iterate() to the Verb Class as per @poolebu's feature request.
* Updated Dependencies.

3.3.2 (2019-06-04)
------------------

* Corrected bug with regular english verbs not being properly regulated. Thanks to @vectomon
* Updated Dependencies.

3.3.1 (2019-02-04)
------------------

* Corrected bug when updating dependencies to use scikit-learn v 0.20.2 and higher.
* Updated Dependencies.

3.3 (2019-04-03)
------------------

* Updated Dependencies to use scikit-learn v 0.20.2 and higher.
* Updated the pre-trained models to use scikit-learn v 0.20.2 and higher.

3.2.3 (2019-26-02)
------------------

* Updated Dependencies.
* Fixed bug which prevented the installation of the pre-trained models.

3.2.2 (2018-18-11)
------------------

* Updated Dependencies.

3.2.0 (2018-04-11)
------------------

* Updated Dependencies.

3.1.3 (2018-07-10)
------------------

* Updated Documentation.
* Added support for pipenv.
* Included tests and documentation in the package distribution.


3.1.2 (2018-06-27)
------------------

* Updated `Type annotations`_ to the whole library for PEP-561 compliance.


3.1.1 (2018-06-26)
------------------

* Minor Api enhancement (see `API documentation`_)


3.1.0 (2018-06-24)
------------------

* Updated the conjugation models for Spanish and Portuguese.
* Internal changes to the format of the verbiste data from xml to json for better handling of unicode characters.
* New class ConjugManager to more easily add new languages to mlconjug3.
* Minor Api enhancement (see `API documentation`_)


3.0.1 (2018-06-22)
------------------

* Updated all provided pre-trained prediction models:
    - Implemented a new vectrorizer extracting more meaningful features.
    - As a result the performance of the models has gone through the roof in all languages.
    - Recall and Precision are intesimally close to 100 %. English being the anly to achieve a perfect score at both Recall and Precision.

* Major API changes:
    - I removed the class EndingCustomVectorizer and refactored it's functionnality in a top level function called extract_verb_features()
    - The provided new improved model are now being zip compressed before release because the feature space has so much grown that their size made them impractical to distribute with the package.
    - Renamed "Model.model" to "Model.pipeline"
    - Renamed "DataSet.liste_verbes" and "DataSet.liste_templates" to "DataSet.verbs_list" and "DataSet.templates_list" respectively. (Pardon my french ;-) )
    - Added the attributes "predicted" and "confidence_score" to the class Verb.
    - The whole package have been typed check. I will soon add mlconjug3's type stubs to typeshed.


2.1.11 (2018-06-21)
-------------------

* Updated all provided pre-trained prediction models
    - The French Conjugator has accuracy of about 99.94% in predicting the correct conjugation class of a French verb. This is the baseline as i have been working on it for some time now.
    - The English Conjugator has accuracy of about 99.78% in predicting the correct conjugation class of an English verb. This is one of the biggest improvement since version 2.0.0
    - The Spanish Conjugator has accuracy of about 99.65% in predicting the correct conjugation class of a Spanish verb. It has also seen a sizable improvement since version 2.0.0
    - The Romanian Conjugator has accuracy of about 99.06% in predicting the correct conjugation class of a Romanian verb.This is by far the bigger gain. I modified the vectorizer to better take into account the morphological features or romanian verbs. (the previous score was about 86%, so it wil be nice for our romanian friends to have a trusted conjugator)
    - The Portuguese Conjugator has accuracy of about 96.73% in predicting the correct conjugation class of a Portuguese verb.
    - The Italian Conjugator has accuracy of about 94.05% in predicting the correct conjugation class of a Italian verb.


2.1.9 (2018-06-21)
------------------

* Now the Conjugator adds additional information to the Verb object returned.
    - If the verb under consideration is already in Verbiste, the conjugation for the verb is retrieved directly from memory.
    - If the verb under consideration is unknown in Verbiste, the Conjugator class now sets the boolean attribute 'predicted' and the float attribute confidence score to the instance of the Verb object the Conjugator.conjugate(verb) returns.
* Added `Type annotations`_ to the whole library for robustness and ease of scaling-out.
* The performance of the Engish and Romanian Models have improved significantly lately. I guess in a few more iteration they will be on par with the French Model which is the best performing at the moment as i have been tuning its parameters for a caouple of year now. Not so much with the other languages, but if you update regularly you will see nice improvents in the 2.2 release.
* Enhanced the localization of the program.
* Now the user interface of mlconjug3 is avalaible in French, Spanish, Italian, Portuguese and Romanian, in addition to English.
* `All the documentation of the project`_ have been translated in the supported languages.


.. _Type annotations: https://github.com/python/typeshed
.. _All the documentation of the project: https://mlconjug3.readthedocs.io/en/latest/
.. _API documentation: https://mlconjug3.readthedocs.io/en/latest/modules.html


2.1.5 (2018-06-15)
------------------

* Added localization.
* Now the user interface of mlconjug3 is avalaible in French, Spanish, Italian, Portuguese and Romanian, in addition to English.


2.1.2 (2018-06-15)
------------------

* Added invalid verb detection.


2.1.0 (2018-06-15)
------------------

* Updated all language models for compatibility with scikit-learn 0.19.1.


2.0.0 (2018-06-14)
------------------

* Includes English conjugation model.
* Includes Spanish conjugation model.
* Includes Italian conjugation model.
* Includes Portuguese conjugation model.
* Includes Romanian conjugation model.


1.2.0 (2018-06-12)
------------------

* Refactored the API. Now a Single class Conjugator is needed to interface with the module.
* Includes improved french conjugation model.
* Added support for multiple languages.


1.1.0 (2018-06-11)
------------------

* Refactored the API. Now a Single class Conjugator is needed to interface with the module.
* Includes improved french conjugation model.


1.0.0 (2018-06-10)
------------------

* First release on PyPI.




