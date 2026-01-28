.. _ref_release_notes:

Release notes
#############

This document contains the release notes for PyWorkbench.

.. vale off

.. towncrier release notes start

`0.11.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.11.0>`_ - January 28, 2026
========================================================================================

.. tab-set::


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Chore: update CHANGELOG for v0.10.0
          - `#285 <https://github.com/ansys/pyworkbench/pull/285>`_

        * - Bump version after release 0.10
          - `#286 <https://github.com/ansys/pyworkbench/pull/286>`_

        * - Chore: bump actions/upload-artifact from 5 to 6
          - `#287 <https://github.com/ansys/pyworkbench/pull/287>`_

        * - Chore: bump actions/download-artifact from 6.0.0 to 7.0.0
          - `#288 <https://github.com/ansys/pyworkbench/pull/288>`_

        * - Update copyright year
          - `#291 <https://github.com/ansys/pyworkbench/pull/291>`_

        * - Version argument is optional
          - `#293 <https://github.com/ansys/pyworkbench/pull/293>`_

        * - User can specify port when launching WB
          - `#294 <https://github.com/ansys/pyworkbench/pull/294>`_

        * - Chore: bump ansys-sphinx-theme[autoapi] from 1.6.4 to 1.7.0
          - `#295 <https://github.com/ansys/pyworkbench/pull/295>`_

        * - Version check must be done after version identification
          - `#296 <https://github.com/ansys/pyworkbench/pull/296>`_


`0.10.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.10.0>`_ - December 12, 2025
=========================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: bump ansys-sphinx-theme[autoapi] from 1.3.3 to 1.4.4
          - `#214 <https://github.com/ansys/pyworkbench/pull/214>`_

        * - bump to 0.10.dev0
          - `#216 <https://github.com/ansys/pyworkbench/pull/216>`_

        * - chore: bump ansys-sphinx-theme[autoapi] from 1.4.4 to 1.4.5
          - `#220 <https://github.com/ansys/pyworkbench/pull/220>`_

        * - chore: bump ansys-sphinx-theme[autoapi] from 1.4.5 to 1.5.0
          - `#221 <https://github.com/ansys/pyworkbench/pull/221>`_

        * - chore: bump bandit from 1.8.3 to 1.8.6
          - `#234 <https://github.com/ansys/pyworkbench/pull/234>`_

        * - chore: bump ansys-sphinx-theme[autoapi] from 1.5.0 to 1.6.0
          - `#241 <https://github.com/ansys/pyworkbench/pull/241>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Chore: bump ansys/actions from 9 to 10
          - `#223 <https://github.com/ansys/pyworkbench/pull/223>`_

        * - Chore: bump actions/download-artifact from 4.3.0 to 5.0.0
          - `#236 <https://github.com/ansys/pyworkbench/pull/236>`_

        * - remote-connection server API changed.
          - `#237 <https://github.com/ansys/pyworkbench/pull/237>`_

        * - Chore: bump actions/checkout from 4 to 5
          - `#239 <https://github.com/ansys/pyworkbench/pull/239>`_

        * - Docs: update ``html_context`` with PyAnsys tags
          - `#240 <https://github.com/ansys/pyworkbench/pull/240>`_

        * - Chore: bump safety from 3.3.0 to 3.6.1
          - `#242 <https://github.com/ansys/pyworkbench/pull/242>`_

        * - Chore: bump actions/setup-python from 5 to 6
          - `#244 <https://github.com/ansys/pyworkbench/pull/244>`_

        * - Chore: bump pytest from 8.3.5 to 8.4.2
          - `#245 <https://github.com/ansys/pyworkbench/pull/245>`_

        * - Chore: bump pytest-cov from 6.1.1 to 7.0.0
          - `#247 <https://github.com/ansys/pyworkbench/pull/247>`_

        * - Add SECURITY.md
          - `#248 <https://github.com/ansys/pyworkbench/pull/248>`_

        * - Fli/add server version handling
          - `#249 <https://github.com/ansys/pyworkbench/pull/249>`_

        * - Chore: bump actions/labeler from 5 to 6
          - `#251 <https://github.com/ansys/pyworkbench/pull/251>`_

        * - Chore: bump ansys-sphinx-theme[autoapi] from 1.6.0 to 1.6.1
          - `#252 <https://github.com/ansys/pyworkbench/pull/252>`_

        * - Chore: bump numpydoc from 1.8.0 to 1.9.0
          - `#253 <https://github.com/ansys/pyworkbench/pull/253>`_

        * - Fli/handle api change for remote connection
          - `#254 <https://github.com/ansys/pyworkbench/pull/254>`_, `#260 <https://github.com/ansys/pyworkbench/pull/260>`_, `#269 <https://github.com/ansys/pyworkbench/pull/269>`_

        * - Chore: bump safety from 3.6.1 to 3.6.2
          - `#256 <https://github.com/ansys/pyworkbench/pull/256>`_

        * - Fix: general improvements and errors on subprocess calls
          - `#257 <https://github.com/ansys/pyworkbench/pull/257>`_

        * - Try adding security check
          - `#259 <https://github.com/ansys/pyworkbench/pull/259>`_

        * - Feat: vulnerability check
          - `#261 <https://github.com/ansys/pyworkbench/pull/261>`_

        * - Chore: bump peter-evans/create-or-update-comment from 4 to 5
          - `#263 <https://github.com/ansys/pyworkbench/pull/263>`_

        * - Chore: bump ansys-sphinx-theme[autoapi] from 1.6.1 to 1.6.3
          - `#264 <https://github.com/ansys/pyworkbench/pull/264>`_

        * - Chore: bump actions/download-artifact from 5.0.0 to 6.0.0
          - `#265 <https://github.com/ansys/pyworkbench/pull/265>`_

        * - Chore: bump actions/upload-artifact from 4 to 5
          - `#266 <https://github.com/ansys/pyworkbench/pull/266>`_

        * - Chore: Update missing or outdated files
          - `#267 <https://github.com/ansys/pyworkbench/pull/267>`_

        * - Chore: bump safety from 3.6.2 to 3.7.0
          - `#270 <https://github.com/ansys/pyworkbench/pull/270>`_

        * - Chore: bump pytest from 8.4.2 to 9.0.1
          - `#272 <https://github.com/ansys/pyworkbench/pull/272>`_

        * - Chore: bump bandit from 1.8.6 to 1.9.1
          - `#273 <https://github.com/ansys/pyworkbench/pull/273>`_

        * - Chore: bump actions/checkout from 5 to 6
          - `#274 <https://github.com/ansys/pyworkbench/pull/274>`_

        * - Chore: bump bandit from 1.9.1 to 1.9.2
          - `#276 <https://github.com/ansys/pyworkbench/pull/276>`_

        * - Docs: fix typo in CONTRIBUTING.md
          - `#279 <https://github.com/ansys/pyworkbench/pull/279>`_

        * - Chore: bump numpydoc from 1.9.0 to 1.10.0
          - `#280 <https://github.com/ansys/pyworkbench/pull/280>`_

        * - Docs: Update \`\`CONTRIBUTORS.md\`\` with the latest contributors
          - `#281 <https://github.com/ansys/pyworkbench/pull/281>`_

        * - Chore: bump pytest from 9.0.1 to 9.0.2
          - `#282 <https://github.com/ansys/pyworkbench/pull/282>`_

        * - Chore: bump ansys-sphinx-theme[autoapi] from 1.6.3 to 1.6.4
          - `#284 <https://github.com/ansys/pyworkbench/pull/284>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: update CHANGELOG for v0.9.0
          - `#215 <https://github.com/ansys/pyworkbench/pull/215>`_

        * - docs: revert cheatsheet in docs
          - `#217 <https://github.com/ansys/pyworkbench/pull/217>`_

        * - docs: improve install instructions by adding pypi install
          - `#219 <https://github.com/ansys/pyworkbench/pull/219>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: bump pypa/gh-action-pypi-publish from 1.12.4 to 1.13.0
          - `#243 <https://github.com/ansys/pyworkbench/pull/243>`_

        * - Fli/handle api change for remote connection
          - `#277 <https://github.com/ansys/pyworkbench/pull/277>`_


`0.9.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.9.0>`_ - May 15, 2025
==================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - bump version to 0.9.dev0
          - `#191 <https://github.com/ansys/pyworkbench/pull/191>`_

        * - chore: bump bandit from 1.8.2 to 1.8.3
          - `#192 <https://github.com/ansys/pyworkbench/pull/192>`_

        * - chore: bump sphinx-autodoc-typehints from 3.0.1 to 3.1.0
          - `#193 <https://github.com/ansys/pyworkbench/pull/193>`_

        * - chore: bump sphinx from 8.1.3 to 8.2.0
          - `#194 <https://github.com/ansys/pyworkbench/pull/194>`_

        * - chore: bump ansys-sphinx-theme[autoapi] from 1.2.7 to 1.3.2
          - `#195 <https://github.com/ansys/pyworkbench/pull/195>`_

        * - chore: bump sphinx from 8.2.0 to 8.2.1
          - `#196 <https://github.com/ansys/pyworkbench/pull/196>`_

        * - chore: bump sphinx from 8.2.1 to 8.2.3
          - `#197 <https://github.com/ansys/pyworkbench/pull/197>`_

        * - chore: bump pytest from 8.3.4 to 8.3.5
          - `#198 <https://github.com/ansys/pyworkbench/pull/198>`_

        * - chore: bump ansys-sphinx-theme[autoapi] from 1.3.2 to 1.3.3
          - `#202 <https://github.com/ansys/pyworkbench/pull/202>`_

        * - chore: bump pytest-cov from 6.0.0 to 6.1.1
          - `#207 <https://github.com/ansys/pyworkbench/pull/207>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - allow user to specify port to use for pymechanical
          - `#201 <https://github.com/ansys/pyworkbench/pull/201>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: update CHANGELOG for v0.8.0
          - `#190 <https://github.com/ansys/pyworkbench/pull/190>`_

        * - docs: remove .tex file from cheatsheet dir
          - `#200 <https://github.com/ansys/pyworkbench/pull/200>`_

        * - support launching pywb on linux
          - `#209 <https://github.com/ansys/pyworkbench/pull/209>`_

        * - python version support: drop 3.9 and add 3.13; bump ansys/action to 9
          - `#213 <https://github.com/ansys/pyworkbench/pull/213>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - docs: Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#206 <https://github.com/ansys/pyworkbench/pull/206>`_


`0.8.0 <https://github.com/ansys/pyworkbench/releases/tag/v0.8.0>`_ - 2025-02-14
================================================================================

Added
^^^^^

- feat: add cheatsheet `#169 <https://github.com/ansys/pyworkbench/pull/169>`_
- PyWB Cheatsheet reviewed and corrected `#172 <https://github.com/ansys/pyworkbench/pull/172>`_


Fixed
^^^^^

- fix: contributors file `#153 <https://github.com/ansys/pyworkbench/pull/153>`_
- fix: use title case in CONTRIBUTORS.md `#161 <https://github.com/ansys/pyworkbench/pull/161>`_
- FIX: Minor typo correction `#185 <https://github.com/ansys/pyworkbench/pull/185>`_


Dependencies
^^^^^^^^^^^^

- chore: bump safety from 3.2.8 to 3.2.9 `#149 <https://github.com/ansys/pyworkbench/pull/149>`_
- chore: bump safety from 3.2.9 to 3.2.10 `#150 <https://github.com/ansys/pyworkbench/pull/150>`_
- chore: bump pytest-cov from 5.0.0 to 6.0.0 `#151 <https://github.com/ansys/pyworkbench/pull/151>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.1.7 to 1.2.0 `#152 <https://github.com/ansys/pyworkbench/pull/152>`_
- chore: bump safety from 3.2.10 to 3.2.11 `#154 <https://github.com/ansys/pyworkbench/pull/154>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.2.0 to 1.2.1 `#155 <https://github.com/ansys/pyworkbench/pull/155>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.2.1 to 1.2.2 `#157 <https://github.com/ansys/pyworkbench/pull/157>`_
- chore: bump bandit from 1.7.10 to 1.8.0 `#160 <https://github.com/ansys/pyworkbench/pull/160>`_
- chore: bump pytest from 8.3.3 to 8.3.4 `#162 <https://github.com/ansys/pyworkbench/pull/162>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.2.2 to 1.2.3 `#164 <https://github.com/ansys/pyworkbench/pull/164>`_
- chore: bump safety from 3.2.11 to 3.2.13 `#166 <https://github.com/ansys/pyworkbench/pull/166>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.2.3 to 1.2.4 `#173 <https://github.com/ansys/pyworkbench/pull/173>`_
- chore: bump safety from 3.2.13 to 3.2.14 `#174 <https://github.com/ansys/pyworkbench/pull/174>`_
- chore: bump sphinx-autodoc-typehints from 2.5.0 to 3.0.0 `#177 <https://github.com/ansys/pyworkbench/pull/177>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.2.4 to 1.2.6 `#180 <https://github.com/ansys/pyworkbench/pull/180>`_
- chore: bump bandit from 1.8.0 to 1.8.2 `#181 <https://github.com/ansys/pyworkbench/pull/181>`_
- chore: bump sphinx-autodoc-typehints from 3.0.0 to 3.0.1 `#183 <https://github.com/ansys/pyworkbench/pull/183>`_
- chore: bump ansys-sphinx-theme[autoapi] from 1.2.6 to 1.2.7 `#186 <https://github.com/ansys/pyworkbench/pull/186>`_
- chore: bump safety from 3.2.14 to 3.3.0 `#189 <https://github.com/ansys/pyworkbench/pull/189>`_


Miscellaneous
^^^^^^^^^^^^^

- close the current project on exit `#159 <https://github.com/ansys/pyworkbench/pull/159>`_


Documentation
^^^^^^^^^^^^^

- chore: update CHANGELOG for v0.7.0 `#147 <https://github.com/ansys/pyworkbench/pull/147>`_
- bump version to 0.8 `#148 <https://github.com/ansys/pyworkbench/pull/148>`_
- DOC: Update docs with new pymechanical api `#165 <https://github.com/ansys/pyworkbench/pull/165>`_
- Fli/improve archive download `#170 <https://github.com/ansys/pyworkbench/pull/170>`_
- doc: include library artifacts `#179 <https://github.com/ansys/pyworkbench/pull/179>`_

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
