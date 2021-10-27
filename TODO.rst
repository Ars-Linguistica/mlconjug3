=====
TODOS
=====

General
-------

* DONE: use logging instead of print() whenever appropriate.
* DONE: implement safe pickling/persistence of trained Pipelines. Use joblib for model persistence instead.
* INPROGRESS: use as much generators/FP as possible.
* DONE: check types with mypy/MonkeyType.
* INPROGRESS: refactor as much as possible.
* TODO: use the package asq or similar to better handle nested dictionaries.
* TODO: update pipenv dependencies.
* DONE: use MonkeyType to generate type information.

CLI
---

* TODO: use the package colorama to colorize output.
* DONE: allow to specify output file to save results to json file or potentially other formats.

mlconjug
--------

* FIXED: fix verb formation bug. Example 'beat' or some verbs from issue#80.
* FIXED: investigate the quality of predicted verbs like 'flabbergast' => 'run' 'rob' => 'mob' from issue#82.
* TODO: add more magic methods following Python data model.
* TODO: investigate the use of None.
* DONE: Raise error indicating that the verb is unknown and that no model has been provided.

PyVerbiste
----------

* TODO: add more magic methods following Python data model.
* TODO: Investigate the use of dataclasses.
* TODO: check that the latest Verbiste data is correct.
* TODO: investigate the use of None.
* DONE: write tests for conjugation file saving feature.

test_mlconjug
-------------

* TODO: use the package colorama to colorize output.
* TODO: add more tests for each language Verb class.

train_models
------------

* DONE: implement results_parser to select and train the best performing models.
* DONE: display prettier output.
* DONE: implement multicore grid search.

conjug_formatter
----------------

* TODO: Implement xml and json formatter of raw conjugation data.
* TODO: allow to specify output file to save results to json or xml file.
* TODO: verify generated data with gold standard.
