
**Get access token for an installed addon:**

.. code-block:: python

   from airslate.client import Client

   client = Client()

   org_uid = '057C5000-0000-0000-0000D881'
   client_id = '32C2A810-0000-0000-000044D8'
   client_secret = 'b21877f468f839821b9c6744ee2b6941'

   identity = client.addons.access_token(org_uid, client_id, client_secret)

   print(identity)
