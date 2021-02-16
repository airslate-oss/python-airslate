===============
Document Fields
===============

.. note::

   To obtain ``token`` refer to ``airslate.addons.auth()`` method.


Update Fields for a given Document
----------------------------------

.. code-block:: python

   import os
   from airslate.client import Client

   org_id = '057C5000-0000-0000-0000D981'
   document_id = 'C484F800-0000-0000-000021F6'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   field = Field.from_one({
       'data': {
           'id': 'C484F800-0000-0000-000021F6-0001',
           'type': 'dictionary',
           'attributes': {
               'name': 'heading1.title',
               'value': 'My Awesome Form',
               'field_type': 'text',
               'editors_config_enabled': False
           }
       }
   })

   document = client.documents.update_fields(
       document_id=document_id,
       fields=UpdateFields(data=[field])
   )

   print(document)

   print({
       'id': document.id,
       'name': document.name,
       'status': document.status,
       'updated_at': document.updated_at,
   })


.. code-block::

   <Document: id=C484F800-0000-0000-000021F6-0001, type=documents>

   {
       'id': 'C484F800-0000-0000-000021F6',
       'name': 'Contact Form',
       'status': 'DRAFT',
       'updated_at': '2021-02-16 00:13:13'
   }


Get Fields for a given Document
-------------------------------

.. code-block:: python

   import os
   from airslate.client import Client

   org_id = '057C5000-0000-0000-0000D981'
   document_id = 'C484F800-0000-0000-000021F6'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   fields = client.documents.fields(document_id)

   for field in fields:
       print(field)

       print({
           'id': field.id,
           'name': field.name,
           'type': field.field_type,
           'value': field.value,
       }, '\n')


.. raw:: html

   <details><summary>Output</summary>

.. code-block::

   <Field: id=C484F800-0000-0000-000021F6-0001, type=dictionary>
   {'id': 'C484F800-0000-0000-000021F6-0001', 'name': 'heading1.title', 'type': 'text', 'value': 'My Awesome Form'}

   <Field: id=C484F800-0000-0000-000021F6-0002, type=dictionary>
   {'id': 'C484F800-0000-0000-000021F6-0002', 'name': 'heading1.description', 'type': 'text', 'value': 'Awesome description'}

   <Field: id=C484F800-0000-0000-000021F6-0003, type=dictionary>
   {'id': 'C484F800-0000-0000-000021F6-0003', 'name': 'name', 'type': 'text', 'value': ''}

   <Field: id=C484F800-0000-0000-000021F6-0004, type=dictionary>
   {'id': 'C484F800-0000-0000-000021F6-0004', 'name': 'email', 'type': 'text', 'value': ''}
