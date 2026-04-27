.. highlight:: shell

============
Contributing
============

Welcome to the mlconjug3 project!

We're thrilled that you're interested in joining our community of contributors and helping us make this project even better.
We believe that everyone has something valuable to offer, and we're excited to see how your unique skills and perspectives can help shape the future of this project.

Whether you're a seasoned developer or just starting out, we have plenty of opportunities for you to get involved.
From fixing bugs to adding new features, there's something for everyone.
And with support for Python 3.9 to 3.14 and the use of modern best practices like the build manager Poetry and the pyproject.toml file, you'll be able to work with the latest tools in the Python ecosystem.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/Ars-Linguistica/mlconjug3/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

mlconjug3 could always use more documentation, whether as part of the official docs,
in docstrings, or even in blog posts and articles.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/Ars-Linguistica/mlconjug3/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible to make it easier to implement.
* Remember that this is a volunteer-driven project, and contributions are welcome.

Get Started!
------------

To get started, you'll need to fork the mlconjug3 repository on GitHub and clone your fork locally.
You can do this by running the following commands in your terminal:

.. code-block:: console

    $ git clone git@github.com:Ars-Linguistica/mlconjug3.git

We recommend using Poetry as our build manager and the pyproject.toml file to manage dependencies. Make sure you have Poetry installed, then:

.. code-block:: console

    $ cd mlconjug3
    $ poetry install

Before you begin working on a new feature or bugfix, create a new branch for it. This makes it easier to isolate changes and submit them in a pull request. You can create a new branch by running the following command:

.. code-block:: console

    $ git checkout -b name-of-your-bugfix-or-feature

We support Python versions 3.9 to 3.14. Make sure your code is compatible with all of them by running the tests:

.. code-block:: console

    $ poetry run pytest
    $ poetry run tox

When you're ready to submit your changes, first make sure all tests pass. Then commit your changes and push your branch:

.. code-block:: console

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

Finally, submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit, make sure that:

1. All tests pass.
2. The pull request includes a clear description of changes.
3. You've added yourself to the CONTRIBUTORS.rst file.
4. You've run the appropriate GitHub Actions workflows and verified they passed.

We may ask you to make changes before merging. Thank you for contributing.

Checking GitHub Actions
-----------------------

To check workflow status for a pull request:

1. Go to the pull request page on GitHub.
2. Look at the "Checks" section.
3. Review workflow names and statuses.
4. Click a workflow for details in the "Actions" tab.
5. Inspect job logs if failures occur.
6. Fix issues and update your PR if needed.

Once all workflows pass, the PR is ready for review.

Tips
----

To run a subset of tests:

.. code-block:: console

    $ poetry run pytest tests/test_module.py

To run tests with coverage:

.. code-block:: console

    $ poetry run pytest --cov=mlconjug3

To run type checks:

.. code-block:: console

    $ poetry run mypy mlconjug3

To check style issues:

.. code-block:: console

    $ poetry run flake8 mlconjug3

To format code:

.. code-block:: console

    $ poetry run black mlconjug3

It is recommended to use pre-commit hooks:

.. code-block:: console

    $ poetry add pre-commit
    $ pre-commit install

To update dependencies:

.. code-block:: console

    $ poetry update

Regularly updating dependencies helps maintain compatibility and security.

By following these practices and using these tools, you help ensure high-quality contributions to the project.
