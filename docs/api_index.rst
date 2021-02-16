=========
API Index
=========


Resources API
=============


Addons API
----------

* ``client.addons.auth()`` - get access token for an Addon installed in an Organization
* ``client.addons.files.get()`` - get the requested Slate Addon File
* ``client.addons.files.download()`` - download contents of the requested Slate Addon File


Documents API
-------------

* ``client.documents.fields()`` - get Fields for a given Document
* ``client.documents.update_fields()`` - update Fields for a given Document


Flows API
---------

* ``client.flows.documents.collection()`` - get supported documents for a given Flow


Slates API
----------

* ``client.slates.tags.assign()`` - assign tags to a given Slate
* ``client.slates.tags.collection()`` - get all Slate tags for a given Flow
