.. highlight:: shell

============
Contributing
============

Welcome to the mlconjug3 project!

We're thrilled that you're interested in joining our community of contributors and helping us make this project even better. 
We believe that everyone has something valuable to offer, and we're excited to see how your unique skills and perspectives can help shape the future of this project.

Whether you're a seasoned developer or just starting out, we have plenty of opportunities for you to get involved. 
From fixing bugs to adding new features, there's something for everyone.
And with the support for python 3.8 to 3.11 and the use of modern best practices like the use of the build manager poetry and the pyproject.toml file, you'll be able to work with the latest and greatest tools in the Python ecosystem.

You can contribute in many ways::

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

mlconjug3 could always use more documentation, whether as part of the
official MLConjug docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/Ars-Linguistica/mlconjug3/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

To get started, you'll need to fork the mlconjug3 repository on GitHub and clone your fork locally.
You can do this by running the following commands in your terminal:

.. code-block:: console

    $ git clone git@github.com:Ars-Linguistica/mlconjug3.git

We recommend using poetry as our build manager and the pyproject.toml file to manage our dependencies. Make sure you have poetry installed, then

.. code-block:: console

    $ cd mlconjug3
    $ poetry install

Before you begin working on a new feature or bugfix, create a new branch for it. This makes it easier to isolate changes and submit them in a pull request. You can create a new branch by running the following command:

.. code-block:: console

    $ git checkout -b name-of-your-bugfix-or-feature

We support Python versions 3.8 to 3.11, make sure that your code is compatible with all of them by running the tests:

.. code-block:: console

    $ poetry run pytest
    $ poetry run tox

When you're ready to submit your changes, first make sure that all tests pass. Then, commit your changes and push your branch to your fork on GitHub:

.. code-block:: console

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

Finally, submit a pull request through the GitHub website.


Pull Request Guidelines
-----------------------

Before you submit, make sure that all of the following are true::

1. All tests pass
2. The pull request includes a clear description of the changes you've made
3. You've added yourself to the CONTRIBUTORS.rst file
4. You've added and ran the appropriate GitHub action workflows and checked that they have passed.

Please note that we may ask you to make changes to your pull request before it is merged. We'll review your changes and provide feedback as soon as possible. Thank you for your contribution!

Checking GitHub Actions
-----------------------

Checking the status of the GitHub workflows of a pull request can be done by following these steps::

1. Go to the pull request on GitHub that you want to check the status of.
2. Look at the "Checks" section of the pull request, which is located at the bottom of the pull request page, next to the "Files changed" tab.
3. Here, you will see the status of all the workflows that are associated with the pull request. Each workflow will have a name and a status (e.g. "continuous-integration/travis-ci/pr", "success").
4. Click on the name of the workflow to view more details about it. This will take you to the "Actions" tab of the pull request, where you can see the output of each job that is associated with that workflow.
5. Look for the "Status" field of each job to see if it has passed or failed. If a job has failed, you can click on the job name to view more details about the failure, such as the error message or log output.
6. If any of the workflows fail, make changes to your pull request to address the issues and update the pull request.

Once all workflows have passed, your pull request will be ready for review and merging.
It's also worth noting that you can also check the status of the workflows on the GitHub Actions tab of the repository, where you can see all the recent workflows runs and their statuses.


Tips
----

Here are a few tips to assist you in your development.

To run a subset of the tests:

.. code-block:: console

    $ poetry run pytest tests/test_module.py


To run pytest with coverage:

.. code-block:: console

    $ poetry run pytest --cov=mlconjug3


To run mypy type checks:

.. code-block:: console

    $ poetry run mypy mlconjug3


To check for any code style issues using flake8:

.. code-block:: console

    $ poetry run flake8 mlconjug3


To automatically format your code using black:

.. code-block:: console

    $ poetry run black mlconjug3

It is also recommended to use pre-commit hooks to automatically run these checks before committing your changes. This can be easily set up using pre-commit by installing it in your virtual environment with 

.. code-block:: console

    $ poetry add pre-commitand 

then running 

.. code-block:: console

    $ pre-commit install

in the root of your local repository.

Additionally, it is a good practice to regularly update your dependencies to ensure compatibility and security.
This can be done by running 

.. code-block:: console

    $ poetry update

and committing the updated pyproject.toml and poetry.lock files.

By following these best practices and utilizing these tools, you can ensure that your contributions adhere to the project's standards and maintain the overall quality of the codebase.
