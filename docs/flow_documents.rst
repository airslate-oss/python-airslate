==============
Flow documents
==============


Get supported documents for given flow
--------------------------------------

.. note::

   To obtain ``token`` refer to ``airslate.addons.access_token()`` function.

.. code-block:: python

   import os
   from airslate.client import Client

   org_id = '057C5000-0000-0000-0000D981'
   flow_id = '04415300-0000-0000-0000BA29'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   documents = client.flow_documents.collection(flow_id, include='fields')

   for document in documents:
       print(document)

       print({
           'id': document['id'],
           'name': document['name'],
           'status': document['status'],
           'version': document['version'],
       })

       for field in document.fields:
           print(field)

.. raw:: html

   <details><summary>Output</summary>

.. code-block::

    <Document (documents): 5ED5E800-0000-0000-000021F6>
    {'id': '5ED5E800-0000-0000-000021F6', 'name': 'Untitled Form', 'status': 'DRAFT', 'version': 8}
    <Field (dictionary): 5ED5E800-0000-0000-000021F6-0001>
    <Field (dictionary): 5ED5E800-0000-0000-000021F6-0002>
    <Field (dictionary): 5ED5E800-0000-0000-000021F6-0003>
