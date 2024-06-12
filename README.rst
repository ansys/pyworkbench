PyWorkbench
===========

|pyansys| |python| |pypi| |GH-CI| |MIT| |ruff|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-workbench-core?logo=pypi
   :target: https://pypi.org/project/ansys-workbench-core/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-workbench-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-workbench-core
   :alt: PyPI

.. |GH-CI| image:: https://github.com/ansys/pyworkbench/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/ansys/pyworkbench/actions/workflows/ci.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/blog/license/mit
   :alt: MIT

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

PyWorkbench is a Python client library for Ansys Workbench.

Installation
------------

To install PyWorkbench in user mode, use `pip <https://pypi.org/project/pip/>`_ :

.. code-block:: bash

    pip install ansys-workbench-core

To install the latest development version of PyWorkbench, use the following commands:

.. code-block:: bash

    git clone https://github.com/ansys/pyworkbench
    cd pyworkbench
    pip install -e .

For more information, see `Getting started <https://workbench.docs.pyansys.com/version/dev/getting-started.html>`_
in the PyWorkbench documentation.

Documentation and issues
------------------------

Documentation of the latest stable release of PyWorkbench can be found at
`PyWorkbench documentation <https://workbench.docs.pyansys.com>`_.

The documentation has these sections:

- `Getting started <https://workbench.docs.pyansys.com/version/dev/getting-started.html>`_: Learn
  how to install PyWorkbench and connect to Workbench.
- `User guide <https://workbench.docs.pyansys.com/version/dev/user-guide.html>`_: Understand key
  concepts and approaches for using PyWorkbench with the Workbench gRPC service.
- `API reference <https://workbench.docs.pyansys.com/version/stable/api/index.html>`_: Understand
  how to use Python to interact programmatically with PyWorkbench.
- `Examples <https://workbench.docs.pyansys.com/version/dev/examples.html>`_: Explore examples that
  show how to use PyWorkbench to create custom applications, automate your existing Workbench
  workflows, and integrate with other popular tools in the Python ecosystem.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the
latest stable release to viewing the documentation for the development version or previously released versions.

On the `PyWorkbench Issues <https://github.com/ansys/pyworkbench/issues>`_
page, you can create issues to report bugs and request new features. On the
`Discussions <https://discuss.ansys.com/>`_ page on the Ansys Developer portal,
you can post questions, share ideas, and get community feedback.

If you have general questions about the PyAnsys ecosystem, email
`pyansys.core@ansys.com <pyansys.core@ansys.com>`_. If your
question is specific to PyWorkbench, ask your
question in an issue as described in the previous paragraph.
