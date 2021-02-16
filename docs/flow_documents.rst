==============
Flow Documents
==============


.. note::

   To obtain ``token`` refer to ``airslate.addons.auth()`` method.


Get supported documents for a given Flow
----------------------------------------

.. code-block:: python

   import os
   from airslate.client import Client

   org_id = '057C5000-0000-0000-0000D981'
   flow_id = '04415300-0000-0000-0000BA29'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   documents = client.flows.documents.collection(flow_id, include='fields')

   for document in documents:
       print(document)

       print({
           'id': document.id,
           'name': document.name,
           'status': document.status,
           'version': document.version,
       })

       for field in document.fields:
           print(field)

.. raw:: html

   <details><summary>Output</summary>

.. code-block::

    <Document: id=5ED5E800-0000-0000-000021F6, type=documents>
    {'id': '5ED5E800-0000-0000-000021F6', 'name': 'Untitled Form', 'status': 'DRAFT', 'version': 8}
    <Field: id=5ED5E800-0000-0000-000021F6-0001, type=dictionary>
    <Field: id=5ED5E800-0000-0000-000021F6-0002, type=dictionary>
    <Field: id=5ED5E800-0000-0000-000021F6-0003, type=dictionary>
