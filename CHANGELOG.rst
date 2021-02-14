Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

0.3.0a1 (2021-XX-XX)
--------------------

Features
^^^^^^^^

* Provided ability to assign tags to a given Flow.
* Introduced ``airslate.exceptions.NotFoundError`` to raise from client
  when the server can not find the requested resource.
* Introduced ``airslate.flow`` module to better organize Flow API:

  * ``client.flow.documents.collection()`` - get supported documents for a given Flow
  * ``client.flow.tags.assign()`` - assign tags to a given Flow
  * ``client.flow.tags.collection()`` - get tags for a given Flow

* Entity attributes are now accessible via dot notation,
  i.e. ``entity['id']`` is the same as ``entity.id``.
* Implement ``airslate.entities.base.BaseEntity.to_dict()`` to convert entities
  to a dictionary.


Breaking Changes
^^^^^^^^^^^^^^^^

* Moved ``client.flow_documents`` to ``client.flow.documents``
* ``BaseEntity.set_attributes()`` from ``airslate.entities.base`` module has been
  removed. Users are recommended to use ``entity.attributes.update(dict)``.
* ``BaseEntity.original_included`` from ``airslate.entities.base`` module has been
  removed.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Provided ``utils`` utility module for be use within ``airslate`` package:

  * ``airslate.client.Client.DEFAULT_HEADERS`` was moved to ``airslate.utils.default_headers()``
  * ``airslate.session.USER_AGENT`` was moved to ``airslate.utils.default_user_agent()``


----


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
  following form: ``<EntityName: id=ID, type=TYPE>``.


----


0.1.0 (2021-02-07)
------------------

* Initial release.
