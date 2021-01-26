==============
Flow documents
==============


Methods
=======

Get supported documents for given flow
--------------------------------------

.. code-block:: python

   from airslate.client import Client

   client = Client(
       token='1nLgn1ZbpNpghbaFTeSaIuL5418qn7IIfrsHg1kwPUZqbFxW9DJrOjVJwkHYBnU8',
   )

   flow_id = '04415300-0000-0000-0000BA29'
   org_id = '057C5000-0000-0000-0000D981'

   query = {'include': 'fields'}
   headers = {
       'Organization-Id': org_id,
   }

   documents = client.flow_documents.collection(
       flow_id,
       query=query,
       headers=headers,
   )

   print(len(documents['data'][0]['relationships']))  # 17
   print(documents['data'][0]['attributes']['type'])  # HTML_FORM_NEW
