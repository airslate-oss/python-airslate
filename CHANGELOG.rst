Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

Versions follow `Semantic Versioning`_ (``<major>.<minor>.<patch>``).

.. note::

   Backward incompatible (breaking) changes will only be introduced in major
   versions.

0.2.1 (2021-02-08)
------------------

Features
^^^^^^^^


* Provided ability to get slate addon file.

* Added new resources:

  * ``airslate.resources.slate_addon.SlateAddonFiles`` - represent slate addon files resource

* Added new entities:

  * ``airslate.entities.addons.SlateAddon`` - represent slate addon entity
  * ``airslate.entities.addons.SlateAddonFile`` - represent slate addon file entity


* The base entity class as well as all derived classes now provide the following methods:

  * ``has_one()`` - create an instance of the related entity
  * ``from_one()`` - create an instance of the current class from the provided data



Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Change default string representation of entities. Now it has the
  following form ``<EntityName: id=ID, type=TYPE>``.


----


0.1.0 (2021-02-07)
------------------

* Initial release.

.. _Semantic Versioning: https://semver.org/
