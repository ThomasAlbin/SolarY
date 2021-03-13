Changelog
=========

0.6 / 2021-03-DD
----------------

This is the first release with strict coding guidelines being enforced.

New Features
------------

* Added `tox.ini` to help automated CI.

* Added automated coding guidelines enforcement using:

  - black
  - blackdoc
  - isort

* Added tools to enforce strict coding standards:

  - flake8
  - mypy
  - pydocstyle
  - doc8
  - pylint
  - bandit

Changes
-------

* Refactored `ReflectorCCD` to not use multiple inheritance but
  ``CCD`` and ``Reflector`` aggregation.

* Restructured the directory structure to adhere to Python project
  standards.

Fixes
-----

* none
