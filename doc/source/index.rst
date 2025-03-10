PyWorkbench documentation |version|
###################################

PyWorkbench provides an environment where you can make use of the capabilities
of various PyAnsys modules for Ansys applications that have been integrated
with Workbench.

.. jinja:: main_toctree

    .. grid:: 1 2 3 3
        :gutter: 1 2 3 3
        :padding: 1 2 3 3

        .. grid-item-card:: Getting started :material-regular:`directions_run`
            :link: getting-started
            :link-type: doc

            Learn how to install PyWorkbench and connect to Workbench.

        .. grid-item-card:: User guide :material-regular:`menu_book`
            :link: user-guide
            :link-type: doc

            Understand key concepts and approaches for using PyWorkbench with
            the Workbench gRPC service.

        {% if build_api %}
        .. grid-item-card:: API reference :material-regular:`bookmark`
            :link: api/index
            :link-type: doc

            Understand how to use Python to interact programmatically with PyWorkbench.
        {% endif %}

        {% if build_examples %}
        .. grid-item-card:: Examples :material-regular:`play_arrow`
            :link: examples
            :link-type: doc

            Learn how to use PyWorkbench to create custom applications,
            automate your existing Workbench workflows.
        {% endif %}

        .. grid-item-card:: Contribute :fa:`people-group`
            :link: contribute
            :link-type: doc

            Learn how to contribute to the PyWorkbench project.

        .. grid-item-card:: Artifacts :fa:`download`
            :link: artifacts
            :link-type: doc

            Download different assets related to PyWorkbench, such as
            documentation, package wheelhouse, and related files.

.. jinja:: main_toctree

    .. toctree::
       :hidden:
       :maxdepth: 3

       getting-started
       user-guide
       {% if build_api %}
       api/index
       {% endif %}
       {% if build_examples %}
       examples
       {% endif %}
       changelog
       contribute
       artifacts
