=========
Flow Tags
=========

.. note::

   To obtain ``token`` refer to ``airslate.addons.auth()`` method.


Get all Slate tags for a given Flow
-----------------------------------

.. code-block:: python

   import os
   from airslate.client import Client

   org_id = '057C5000-0000-0000-0000D981'
   flow_id = '04415300-0000-0000-0000BA29'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   tags = client.slates.tags.collection(flow_id)
   print(tags)

Output

.. code-block::

    [<Tag: id=0A231100-0000-0000-0000943B, type=flow_tags>,
     <Tag: id=FFD92100-0000-0000-0000943B, type=flow_tags>,
     <Tag: id=D1533100-0000-0000-0000943B, type=flow_tags>]


Assign tags to a given Slate
----------------------------

.. code-block:: python

   import os
   from airslate.client import Client
   from airslate.models.tags import Assign

   org_id = '057C5000-0000-0000-0000D981'
   flow_id = '04415300-0000-0000-0000BA29'
   slate_id = 'D38EA300-0000-0000-0000C9C1'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   request_data = Assign(names=['bookkeeping', 'contacts', 'internal'])
   tags = client.slates.tags.assign(
       flow_id,
       slate_id,
       request_data,
   )

   for tag in tags:
       print({
           'id': tag.id,
           'name': tag.name,
           'created_at': tag.created_at,
           'org_id': tag.relationships['organization']['data']['id'],
       })


.. raw:: html

   <details><summary>Output</summary>

.. code-block::

    {'id': '0A231100-0000-0000-0000943B',
     'name': 'bookkeeping','
     'created_at': '2021-02-13 14:08:49',
     'org_id': '057C5000-0000-0000-0000D981'}

    {'id': 'FFD92100-0000-0000-0000943B',
     'name': 'contacts',
     'created_at': '2021-02-13 14:08:49',
     'org_id': '057C5000-0000-0000-0000D981'}

    {'id': 'D1533100-0000-0000-0000943B',
     'name': 'internal',
     'created_at': '2021-02-13 14:08:49',
     'org_id': '057C5000-0000-0000-0000D981'}
