PyWorkbench documentation |version|
###################################

PyWorkbench provides an environment where you can make use of the capabilities
of various PyAnsys modules for Ansys applications that have been integrated
with Workbench.

.. grid:: 2

    .. grid-item-card:: Getting started :material-regular:`directions_run`
        :link: getting-started
        :link-type: doc

        Learn how to install PyWorkbench and connect to Workbench.

    .. grid-item-card:: User guide :material-regular:`menu_book`
        :link: user-guide
        :link-type: doc

        Understand key concepts and approaches for using PyWorkbench with
        the Workbench gRPC service.

.. jinja:: main_toctree

    {% if build_api or build_examples %}
    .. grid:: 2

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

           Explore examples that show how to use PyWorkbench to create custom applications,
           automate your existing Workbench workflows, and integrate with other popular tools
           in the Python ecosystem.
        {% endif %}
    {% endif %}


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
       artifacts
