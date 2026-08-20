.. _ref_release_notes:

Release notes
#############

This document contains the release notes for PyWorkbench.

.. vale off

.. towncrier release notes start

`0.7.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.7.0>`_ - 2024-10-23
================================================================================

Changed
^^^^^^^

- chore: update CHANGELOG for v0.6.0 `#114 <https://github.com/ansys/pyworkbench/pull/114>`_
- maint: migrate to ansys sphinx theme 1.0.9 `#121 <https://github.com/ansys/pyworkbench/pull/121>`_


Fixed
^^^^^

- fix: update cicd for bot secrets `#136 <https://github.com/ansys/pyworkbench/pull/136>`_


Dependencies
^^^^^^^^^^^^

- chore: bump bandit from 1.7.8 to 1.7.9 `#90 <https://github.com/ansys/pyworkbench/pull/90>`_
- chore: bump pytest from 8.2.2 to 8.3.1 `#106 <https://github.com/ansys/pyworkbench/pull/106>`_
- chore: bump sphinx from 7.4.6 to 7.4.7 `#107 <https://github.com/ansys/pyworkbench/pull/107>`_
- chore: bump ansys/actions from 6 to 7 `#109 <https://github.com/ansys/pyworkbench/pull/109>`_
- bump version to 0.7.dev0 `#115 <https://github.com/ansys/pyworkbench/pull/115>`_
- chore: bump numpydoc from 1.7.0 to 1.8.0 `#120 <https://github.com/ansys/pyworkbench/pull/120>`_
- chore: bump ansys-sphinx-theme[autoapi] from 0.16.6 to 1.0.10 `#122 <https://github.com/ansys/pyworkbench/pull/122>`_
- chore: bump safety from 3.2.4 to 3.2.7 `#123 <https://github.com/ansys/pyworkbench/pull/123>`_
- chore: bump sphinx from 7.4.7 to 8.0.2 `#124 <https://github.com/ansys/pyworkbench/pull/124>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.0.10 to 1.0.11 `#125 <https://github.com/ansys/pyworkbench/pull/125>`_
- chore: bump bandit from 1.7.9 to 1.7.10 `#126 <https://github.com/ansys/pyworkbench/pull/126>`_
- chore: bump pytest from 8.3.1 to 8.3.3 `#128 <https://github.com/ansys/pyworkbench/pull/128>`_
- chore: bump safety from 3.2.7 to 3.2.8 `#129 <https://github.com/ansys/pyworkbench/pull/129>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.0.11 to 1.1.1 `#130 <https://github.com/ansys/pyworkbench/pull/130>`_
- chore: bump sphinx-autodoc-typehints from 2.2.0 to 2.5.0 `#134 <https://github.com/ansys/pyworkbench/pull/134>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.1.1 to 1.1.3 `#137 <https://github.com/ansys/pyworkbench/pull/137>`_
- chore: bump sphinx from 8.0.2 to 8.1.0 `#138 <https://github.com/ansys/pyworkbench/pull/138>`_
- chore: bump sphinx from 8.1.0 to 8.1.3 `#140 <https://github.com/ansys/pyworkbench/pull/140>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.1.3 to 1.1.7 `#146 <https://github.com/ansys/pyworkbench/pull/146>`_


Miscellaneous
^^^^^^^^^^^^^

- support launching workbench in non-UI mode `#118 <https://github.com/ansys/pyworkbench/pull/118>`_
- update argument name for UI mode `#119 <https://github.com/ansys/pyworkbench/pull/119>`_
- try fixing accept.txt file `#135 <https://github.com/ansys/pyworkbench/pull/135>`_


Documentation
^^^^^^^^^^^^^

- support variables in script; change argument release to version `#143 <https://github.com/ansys/pyworkbench/pull/143>`_
- support downloading project archive; suppress console window `#145 <https://github.com/ansys/pyworkbench/pull/145>`_

`0.6.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.6.0>`_ - 2024-08-16
================================================================================

Changed
^^^^^^^

- chore: update CHANGELOG for v0.5.0 `#111 <https://github.com/ansys/pyworkbench/pull/111>`_


Dependencies
^^^^^^^^^^^^

- bump version to 0.6.dev0 `#112 <https://github.com/ansys/pyworkbench/pull/112>`_


Miscellaneous
^^^^^^^^^^^^^

- fix example repo URL; add server release requirement in doc `#113 <https://github.com/ansys/pyworkbench/pull/113>`_

`0.5.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.5.0>`_ - 2024-08-15
================================================================================

Changed
^^^^^^^

- chore: update CHANGELOG for v0.4.0 `#87 <https://github.com/ansys/pyworkbench/pull/87>`_


Fixed
^^^^^

- docs: update docs links and `check-swicher` `#89 <https://github.com/ansys/pyworkbench/pull/89>`_
- fix: make `WMI` windows only dependency `#105 <https://github.com/ansys/pyworkbench/pull/105>`_


Dependencies
^^^^^^^^^^^^

- chore: bump ansys-sphinx-theme[autoapi] from 0.16.5 to 0.16.6 `#94 <https://github.com/ansys/pyworkbench/pull/94>`_
- chore: bump sphinx-autodoc-typehints from 2.1.1 to 2.2.0 `#95 <https://github.com/ansys/pyworkbench/pull/95>`_
- chore: bump safety from 3.2.3 to 3.2.4 `#98 <https://github.com/ansys/pyworkbench/pull/98>`_


Miscellaneous
^^^^^^^^^^^^^

- fix some doc mistakes `#91 <https://github.com/ansys/pyworkbench/pull/91>`_

`0.4.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.4.0>`_ - 2024-06-12
================================================================================

Added
^^^^^

- tests: add the basic units tests `#79 <https://github.com/ansys/pyworkbench/pull/79>`_


Changed
^^^^^^^

- ci: update the release workflow to trusted publishers `#71 <https://github.com/ansys/pyworkbench/pull/71>`_


Fixed
^^^^^

- fix: update ``ci-cd`` and repo url `#68 <https://github.com/ansys/pyworkbench/pull/68>`_
- docs: improve docstring and api reference `#69 <https://github.com/ansys/pyworkbench/pull/69>`_


Dependencies
^^^^^^^^^^^^

- doc: update documentation to match PyAnsys standards `#63 <https://github.com/ansys/pyworkbench/pull/63>`_
- docs: update the common pyansys documents `#64 <https://github.com/ansys/pyworkbench/pull/64>`_
- MAINT: bump ansys-sphinx-theme[autoapi] from 0.16.4 to 0.16.5 `#73 <https://github.com/ansys/pyworkbench/pull/73>`_
- MAINT: bump sphinx-autodoc-typehints from 2.1.0 to 2.1.1 `#75 <https://github.com/ansys/pyworkbench/pull/75>`_
- chore: bump safety from 3.2.0 to 3.2.1 `#77 <https://github.com/ansys/pyworkbench/pull/77>`_
- chore: bump pytest from 8.2.1 to 8.2.2 `#82 <https://github.com/ansys/pyworkbench/pull/82>`_
- chore: bump safety from 3.2.1 to 3.2.3 `#84 <https://github.com/ansys/pyworkbench/pull/84>`_
- chore: update api version `#86 <https://github.com/ansys/pyworkbench/pull/86>`_


Miscellaneous
^^^^^^^^^^^^^

- feat: adding API for connecting to a running server `#80 <https://github.com/ansys/pyworkbench/pull/80>`_
- doc: technical review `#81 <https://github.com/ansys/pyworkbench/pull/81>`_
- Overall review based on skimming the doc `#83 <https://github.com/ansys/pyworkbench/pull/83>`_

.. vale on
