Contribute as a developer
#########################

.. grid:: 1 1 3 3

    .. grid-item-card:: :fa:`code-fork` Fork the repository
        :padding: 2 2 2 2
        :link: fork-the-repository
        :link-type: ref

        Fork the project to create a copy.

    .. grid-item-card:: :fa:`download` Clone the repository
        :padding: 2 2 2 2
        :link: clone-the-repository
        :link-type: ref

        Clone the repository to download the copy to your local machine.

    .. grid-item-card:: :fa:`download` Install for developers
        :padding: 2 2 2 2
        :link: install-for-developers
        :link-type: ref

        Install the project in editable mode.

    .. grid-item-card:: :fa:`vial-circle-check` Run the tests
        :padding: 2 2 2 2
        :link: run-tests
        :link-type: ref

        Verify your changes to the project by running tests.


.. _fork-the-repository:

Fork the repository
===================

Forking the repository is the first step to contributing to the project. This
allows you to have your own copy of the project so that you can make changes without
affecting the main project. Once you have made your changes, you can submit a
pull request to the main project to have your changes reviewed and merged.

.. button-link:: https://github.com/ansys/pyworkbench/fork
    :color: primary
    :align: center

    :fa:`code-fork` Fork this project

.. note::

    If you are an Ansys employee, you can skip this step.

.. _clone-the-repository:

Clone the repository
====================

Make sure that you `configure SSH`_ with your GitHub
account. This allows you to clone the repository without having to use tokens
or passwords. Also, make sure you have `git`_ installed on your machine.

Clone the repository using SSH:

.. code-block:: bash

    git clone git@github.com:ansys/pyworkbench

.. note::

    If you are not an Ansys employee, you must fork the repository and
    replace ``ansys`` with your GitHub username in the ``git clone`` command.

.. _install-for-developers:

Install for developers
======================

Installing PyWorkbench in development mode lets you change the code
and see these changes reflected in your environment without having to reinstall
the library every time you make a change.

Virtual environment
-------------------

Start by navigating to the project's root directory:

.. code-block::

    cd pyworkbench

Then, create a new virtual environment named ``.venv`` to isolate your system's
Python environment:

.. code-block:: text

    python -m venv .venv

Finally, activate this environment:

.. tab-set::

    .. tab-item:: Windows

        .. tab-set::

            .. tab-item:: CMD

                .. code-block:: text

                    .venv\Scripts\activate.bat

            .. tab-item:: PowerShell

                .. code-block:: text

                    .venv\Scripts\Activate.ps1

    .. tab-item:: macOS/Linux/UNIX

        .. code-block:: text

            source .venv/bin/activate

Development mode
----------------

Now, install PyWorkbench in editable mode:

.. code-block:: text

    python -m pip install --editable .

Verify the installation by checking the version of the library:


.. code-block:: python

    from ansys.workbench.core import __version__


    print(f"pyworkbench version is {__version__}")

.. jinja::

    .. code-block:: text

       >>> pyworkbench version is {{ PYWORKBENCH_VERSION }}

Install Tox
-----------

Once the project is installed, you can install `Tox`_. This is a cross-platform
automation tool. The main advantage of Tox is that it allows you to test your
project in different environments and configurations in a temporary and
isolated Python virtual environment.

Install Tox:

.. code-block:: text

    python -m pip install tox

Verify the Tox installation by listing all the different environments
(automation rules) for PyWorkbench:

.. code-block:: text

    tox list

.. _run-tests:

Run the tests
=============

Once you have made your changes, you can run the tests to verify that your
changes did not break the project. PyWorkbench tests support different markers
to avoid running the whole suite of tests. These markers are associated with a
dedicated Tox environment.

.. code-block:: text

    tox -e tests
