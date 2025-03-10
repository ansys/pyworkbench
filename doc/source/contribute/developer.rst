Contributing as a developer
###########################

.. grid:: 1 1 3 3

    .. grid-item-card:: :fa:`code-fork` Fork the repository
        :padding: 2 2 2 2
        :link: fork-the-repository
        :link-type: ref

        Learn how to fork the project and get your own copy.

    .. grid-item-card:: :fa:`download` Clone the repository
        :padding: 2 2 2 2
        :link: clone-the-repository
        :link-type: ref

        Download your own copy in your local machine.

    .. grid-item-card:: :fa:`download` Install for developers
        :padding: 2 2 2 2
        :link: install-for-developers
        :link-type: ref

        Install the project in editable mode.

    .. grid-item-card:: :fa:`vial-circle-check` Run the tests
        :padding: 2 2 2 2
        :link: run-tests
        :link-type: ref

        Verify your changes by testing the project.


.. _fork-the-repository:

Fork the repository
===================

Forking the repository is the first step to contributing to the project. This
allows you to have your own copy of the project so you can make changes without
affection the main project. Once you have made your changes, you can submit a
pull-request to the main project to have your changes reviewed and merged.

.. button-link:: https://github.com/ansys/pyworkbench/fork
    :color: primary
    :align: center

    :fa:`code-fork` Fork this project

.. note::

    If you are an Ansys employee, you can skip this step.

.. _clone-the-repository:

Clone the repository
====================

Make sure you `configure SSH`_ with your GitHub
account. This allows you to clone the repository without having to use tokens
or passwords. Also, make sure you have `git`_ installed in your machine.

To clone the repository using SSH, run:

.. code-block:: bash

    git clone git@github.com:ansys/pyworkbench

.. note::

    If you are not an Ansys employee, you need to fork the repository and
    replace ``ansys`` with your GitHub user name in the ``git clone`` command.

.. _install-for-developers:

Install for developers
======================

Installing pyworkbench in development mode allows you to perform changes to the code
and see the changes reflected in your environment without having to reinstall
the library every time you make a change.

Virtual environment
-------------------

Start by navigating to the project's root directory by running:

.. code-block::

    cd pyworkbench

Then, create a new virtual environment named ``.venv`` to isolate your system's
Python environment by running:

.. code-block:: text

    python -m venv .venv

Finally, activate this environment by running:

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

Now, install pyworkbench in editable mode by running:

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
isolated Python virtual environment. To install Tox, run:

.. code-block:: text

    python -m pip install tox

Finally, verify the installation by listing all the different environments
(automation rules) for pyworkbench:

.. code-block:: text

    python -m tox list

.. _run-tests:

Run the tests
=============

Once you have made your changes, you can run the tests to verify that your
modifications did not break the project. pyworkbench tests support different markers
to avoid running the whole suite of tests. These markers are associated to a
dedicated `Tox`_ environment.
