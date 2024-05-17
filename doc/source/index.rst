PyWorkbench documentation |version|
###################################

PyWorkbench provides an environment where you can make use of the capabilities
of various PyAnsys modules for which the Ansys applications have been
integrated with Workbench.

.. grid:: 2

    .. grid-item-card:: Getting started :fa:`person-running`
        :link: getting-started
        :link-type: doc

        Step-by-step guidelines on how to set up your environment to work with
        PyWorkbench and verify your installation.

    .. grid-item-card:: User guide :fa:`book-open-reader`
        :link: user-guide
        :link-type: doc

        Learn about the capabilities, features, and key topics in PyWorkbench.
        This guide provides useful background information and explanations.

.. jinja:: main_toctree

    {% if build_api or build_examples %}
    .. grid:: 2

       {% if build_api %}
       .. grid-item-card:: API reference :fa:`book-bookmark`
           :link: api/index
           :link-type: doc

           A detailed guide describing the PyWorkbench API. This guide documents all the
           methods and properties for each interface, class, and
           enumerations of each PyWorkbench module.
        {% endif %}

       {% if build_examples %}
       .. grid-item-card:: Gallery of examples :fa:`laptop-code`
           :link: examples
           :link-type: doc

           Learn how to use PyWorkbench for creating custom applications and automating
           your existing Workbench workflows. This guide contains a gallery of examples
           showing how to integrate PyWorkbench with other popular tools in the Python
           ecosystem.
        {% endif %}
    {% endif %}


.. jinja:: main_toctree

    .. toctree::
       :hidden:
       :maxdepth: 3

       getting-started
       user-guide
       {% if build_examples %}
       examples
       {% endif %}
       {% if build_api %}
       api/index
       {% endif %}

