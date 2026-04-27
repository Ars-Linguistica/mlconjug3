=======
History
=======

Pending
-------

* Fix `subject=="abbrev"` option.

3.11.0 (2023-06-09)
-------------------

* Fixed rendering issue for italian verbs in the command line interface.
* Updated dependencies.
* Updated documentation.

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

This is a **major release** of mlconjug3 with significant improvements to the
machine learning core, better cross-version compatibility, and a modernized
build system.

⚠️ **Important compatibility notes**

* Python support: **3.9 → 3.14**
* `scikit-learn` is now **dynamically selected based on Python version**:

  - Python < 3.13 → scikit-learn 1.3 – 1.7
  - Python ≥ 3.13 → scikit-learn ≥ 1.8

* Pretrained models are built with **scikit-learn 1.7** for maximum backward compatibility.
* Models remain usable across newer versions but retraining is recommended for strict reproducibility.

⚠️ **Known issues**

* On **Windows + Python 3.13+**, upstream `scipy` / `scikit-learn` may cause:

  - segmentation faults
  - access violations during import

  This is **NOT caused by mlconjug3**, but by the scientific Python stack.

  Workarounds:

  * Use Python ≤ 3.12 on Windows for production stability
  * Or use Linux/macOS for Python 3.13+

---

🚀 **Machine Learning Improvements**

* Complete redesign of the internal ML pipeline:

  - New **feature extraction strategy** for verbs
  - Improved linguistic representation
  - Better handling of morphological patterns

* New default classifier:

  - `SGDClassifier` with:
    - `log_loss`
    - `elasticnet` regularization
    - optimized hyperparameters

* Improved accuracy for:

  - **Italian verbs**
  - **Romanian verbs**

* More stable and deterministic training behavior

---

🧠 **Model & API changes (internal)**

* Refactored `Model` class:

  - Clear separation of vectorizer and classifier
  - Explicit `Pipeline` usage (now guaranteed)

* Added safer training wrapper
* Improved probability prediction handling

⚠️ Public API remains **fully backward compatible**

---

📦 **Packaging & Build System**

* Fully modernized Poetry configuration
* Fixed dependency resolution across all Python versions
* Prevented source builds of NumPy / SciPy in CI
* Improved cross-platform reproducibility

---

🧪 **CI / Testing**

* CI now runs on:

  - Linux
  - macOS
  - Windows

* Full Python matrix:

  - 3.9 → 3.14

* Improved stability and deterministic test results

---

📚 **Documentation**

* Updated to reflect:

  - new ML pipeline
  - compatibility guarantees
  - platform-specific caveats

---

⚡ Summary

This release makes mlconjug3:

* More accurate
* More stable across Python versions
* Future-proof for Python 3.13+
* Easier to maintain and extend

---

3.11.0 (2023-06-09)
-------------------

* Fixed rendering issue for Italian verbs in the CLI output.
* Updated dependencies for better stability.
* Minor documentation improvements.

---

3.10.0 (2023-01-26)
-------------------

This release focused on usability and performance improvements.

* Added **config file support** for CLI usage.
* Implemented **XML conjugation caching** for faster loading.
* Complete documentation overhaul.
* Signed release using sigstore for supply chain security.

---

3.9.0 (2023-01-24)
------------------

Major feature and performance release.

* Added support for **Python 3.11**
* Upgraded to **scikit-learn 1.2**
* Introduced `ConjugatorTrainer` for custom model training
* Added **rich-based CLI output**
* Enabled multiprocessing for batch conjugation
* Added LRU caching for faster repeated queries
* Internal refactor in preparation for v4

---

3.8.3 (2022-01-03)
------------------

* Improved training parameters across all models
* Fully compliant `pyproject.toml`
* Migration to Poetry build system
* Updated to scikit-learn 1.0.2

---

3.8.2 (2021-10-28)
------------------

* Fixed dependency resolution issues when installing with pip

---

3.8.1 (2021-10-28)
------------------

* Metadata and documentation updates

---

3.8.0 (2021-10-28)
------------------

* Fixed CountVectorizer uppercase bug
* Retrained all models
* Full Poetry migration
* Improved packaging reliability

---

3.7.x Series (2020–2021)
------------------------

Stabilization and performance improvements:

* Frequent model retraining with newer scikit-learn versions
* Improved accuracy across all supported languages
* Added multiprocessing and caching
* Expanded test coverage
* Introduced CI pipelines (GitHub Actions)
* Added conda-forge distribution

---

3.6.x and earlier (2019–2020)
-----------------------------

Foundation and expansion phase:

* Introduction of multiple languages:

  - French, English, Spanish, Italian, Portuguese, Romanian

* Transition to:

  - joblib model persistence
  - typed codebase (PEP 561)

* Major improvements in:

  - feature extraction
  - model accuracy (approaching 99–100%)

---

3.0.0 (2018-06-22)
------------------

* Major API redesign
* Introduction of pipeline-based ML models
* Significant accuracy improvements
* First large-scale model distribution

---

2.x Series (2018)
-----------------

* Added multilingual support
* Introduced ML-based conjugation
* Localization of UI and documentation

---

1.0.0 (2018-06-10)
------------------

* Initial release on PyPI
* French conjugation support
