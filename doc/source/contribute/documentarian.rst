Contributing as a documentarian
###############################

.. grid:: 1 1 3 3

    .. grid-item-card:: :fa:`pencil` Write documentation
        :padding: 2 2 2 2
        :link: write-documentation
        :link-type: ref

        Learn how to get started, use, and contribute to the project.

    .. grid-item-card:: :fa:`laptop-code` Add a new example
        :padding: 2 2 2 2
        :link: write-examples
        :link-type: ref

        Write a new example to showcase the capabilities of PyWorkbench.

    .. grid-item-card:: :fa:`file-code` Build the documentation
        :padding: 2 2 2 2
        :link: build-documentation
        :link-type: ref

        Render the documentation to see your changes reflected.

.. _write-documentation:

Write documentation
===================

`Sphinx`_ is the tool used to generate PyWorkbench documentation. You write most of the content
in `ReStructuredText`_ files. However, some of the content, like the
:ref:`examples <Examples>`, use a mix of `Markdown`_ and Python. If
you are interested in writing examples, see :ref:`writing examples <write-examples>`.

The documentation is located in the ``doc/source`` directory. The landing page
is declared in the ``doc/source/index.rst`` file. The subdirectories contain
the pages of different documentation sections. Finally, the
``doc/source/_static/`` folder contains various assets like images, and CSS
files.

The layout of the ``doc/source`` directory is reflected in the URLs of the
online documentation pages. For example, the
``doc/source/contribute/documentarian.rst``file renders as
``https://workbench.docs.pyansys.com/contribute/documentarian`` URL.

Thus, if you create a file, it important to follow these rules:

- Use lowercase letters for file and directory names.
- Use short and descriptive names.
- Use hyphens to separate words.
- Play smart with the hierarchy of the files and directories.

You must include all files in a table of contents. No orphan files are
permitted. If a file is not included in the table of contents, Sphinx raises a
warning that causes the build to fail.

A table of contents can be declared using a directive like this:

.. code-block:: rst

    .. toctree::
        :hidden:
        :maxdepth: 3

        path-to-file-A
        path-to-file-B
        path-to-file-C
        ...

The path to the file is relative to the directory where the table of contents
is declared.

.. _write-examples:

Write a new example
===================

The :ref:`examples <Examples>` section of the documentation showcases different
capabilities of PyWorkbench. Each example is a standalone Python script. Despite
being PY files, they are written in a mix of `Markdown`_ and Python. This
is possible thanks to the `myst-parser`_ Sphinx extension. In addition, these
Python files can be opened as Jupyter Notebooks thanks to the `jupytext`_
extension.

Documentarians writing new examples are encouraged to open a new Jupyter Lab
session and write the example as a Jupyter Notebook. This way, the
documentarian can test the code and see the output in real time. The created
Jupyter Notebook gets stored as a Python file automatically.

Note that the examples are contained in its own repository, which you can find
in `PyWorkbench examples repository`_.

Finally, here are some tips for writing examples:

- Start the example with an explanation of the main topic. For example, if you
  are discussing a certain orbital maneuver, explain what that maneuver
  entails. Similarly, if an example is centered around satellite coverage,
  provide an explanation of what coverage is. Try to use as many relevant
  keywords as possible in this section to optimize for Search Engine
  Optimization.

- The second section of the example must be a problem statement. This statement
  must include all of the parameters needed in the example, as well as a
  description of what the example aims to determine. Write this section in an
  imperative form.

- Include an explanation with each code cell. In a Jupyter Notebook, this
  entails adding a Markdown cell before each code cell. The explanations should
  be included before, not after, the corresponding code.

.. _build-documentation:

Build the documentation
=======================

`Tox`_ is used for automating the build of the documentation. There are
different environments for cleaning the build, building the documentation
in different formats such as HTML, and running the tests.

The following environments are available:

.. dropdown:: Documentation environments
    :animate: fade-in
    :icon: three-bars

    .. list-table::
        :header-rows: 1
        :widths: auto

        * - Environment
          - Command
        * - doc-style
          - python -m tox -e doc-style
        * - doc-links
          - python -m tox -e doc-links
        * - doc-html
          - python -m tox -e html
