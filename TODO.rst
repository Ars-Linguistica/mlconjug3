=====
TODOS
=====

General
-------

* TODO: use logging instead of print() whenever appropriate.
* TODO: implement safe pickling/persistence of trained Pipelines.
* TODO: use as much generators/FP as possible.
* TODO: check types with mypy.
* TODO: refactor as much as possible.
* TODO: use the package asq or similar to better handle nested dictionaries.

CLI
---

* TODO: use the package colorama to colorize input.
* TODO: allow to specify output file to save results to json file or potentially other formats.

mlconjug
--------

* FIXME: fix verb formation bug. Example 'flabergast' or some verbs from issue#80.
* TODO: add more magic methods following Python data model.

PyVerbiste
----------

* TODO: add more magic methods following Python data model.
* TODO: Investigate the use of dataclasses.

test_mlconjug
-------------

* TODO: use the package colorama to colorize input.
* TODO: add more tests for each language Verb class.

train_models
------------

* TODO: implement results_parser to select and train the best performing models.
* TODO: display prettier output.
* TODO: implement multicore grid search.

conjug_formatter
----------------

* TODO: Implement xml and json formatter of raw conjugation data.
* TODO: allow to specify output file to save results to json or xml file.
* TODO: verify generated data with gold standard.
