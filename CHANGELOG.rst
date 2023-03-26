Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

1.0.0 (2023-XX-XX)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Refocused project from working solely on Bots API to working with the broader
  airSlate API. The project has shifted its focus from working exclusively on
  the Bots API to encompass the full range of functionality available through
  the airSlate API. This change will enable us to better support the needs of
  our users and provide a more comprehensive solution for their workflow
  automation needs. We will continue to maintain and update our Bots API
  functionality, but with a renewed emphasis on integration with the wider
  airSlate ecosystem.
* Dropped support for Python 3.7 due to end-of-life status.
  Python 3.7 reached its end-of-life date in June 2023, which means it will no
  longer receive bug fixes or security updates from the Python development team.
  As a result, we have removed support for Python 3.7 in order to ensure the
  ongoing security and stability of our package. Users who require Python 3.7
  can continue to use older package versions that support it.


Features
^^^^^^^^

* Provided resource class to work with Organizations API.


Improvements
^^^^^^^^^^^^

* Overhauled ``setup.py`` to improve parsing of changelog and better detection
  of current package version.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Streamlined ``setup.py`` code to reduce duplication and improve maintainability.
* Revamped requirements files to ensure better reproducibility of builds.
* Updated dependency versions and added more precise version constraints where
  applicable to prevent unexpected package updates during builds.
* Change coverage collection technics and tests run thanks to ``coverage``.


----


0.4.0b1 (2023-03-25)
--------------------

Features
^^^^^^^^

* Added support for Python 3.11.


Improvements
^^^^^^^^^^^^

* Changed additional groups of dependencies declared in ``setup.py`` so that
  ``develop`` is superset now for ``testing`` and ``docs``.


Bug Fixes
^^^^^^^^^

* Don't include ``tests`` package in wheel. Previously ``pip install airslate``
  used to install a top-level package ``tests``. This was fixed.
* Fixed package description.


----


0.3.0a1 (2021-02-18)
--------------------

Features
^^^^^^^^

* Provided ability to get and assign Tags for a given Slate.
* Provided ability to get and update Fields for a given Document.
* Introduced ``airslate.exceptions.NotFoundError`` to raise from client
  when the server can not find the requested resource.
* Introduced ``airslate.facades`` facade module to provide an easy to access API resources:

  * ``client.addons.auth()`` - get access token for an Addon installed in an Organization
  * ``client.addons.files.get()`` - get the requested Slate Addon File
  * ``client.addons.files.download()`` - download contents of the requested Slate Addon File
  * ``client.documents.fields()`` - get Fields for a given Document
  * ``client.documents.update_fields()`` - update Fields for a given Document
  * ``client.flows.documents.collection()`` - get supported Documents for a given Flow
  * ``client.slates.tags.assign()`` - assign Tags to a given Slate
  * ``client.slates.tags.collection()`` - get all Slate Tags for a given Flow

* Entity attributes are now accessible via dot notation,
  i.e. ``entity['id']`` is the same as ``entity.id``.
* Implement ``airslate.entities.base.BaseEntity.to_dict()`` to convert entities
  to a dictionary.
* Implement ``airslate.entities.base.BaseEntity.__getstate__()`` as well as
  ``airslate.entities.base.BaseEntity.__setstate__()`` to provide ability to persist
  and load entities state.
* Implement ``airslate.client.Client.patch()`` to send ``PATCH`` requests.


Breaking Changes
^^^^^^^^^^^^^^^^

* Moved ``client.addons.access_token()`` to ``client.addons.auth()`` facade.
* Moved ``client.slate_addon_files`` to ``client.addons.files()`` facade.
* Moved ``client.flow_documents`` to ``client.flows.documents()`` facade.
* ``BaseEntity.set_attributes()`` from ``airslate.entities.base`` module has been
  removed. Users are recommended to use ``entity.attributes.update(dict)``.
* ``BaseEntity.original_included`` from ``airslate.entities.base`` module has been
  removed.


Bug Fixes
^^^^^^^^^

* Fixed ``included`` parsing for ``BaseEntity.from_one`` and ``BaseEntity.from_collection``
  when call ``filter_included``.


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
