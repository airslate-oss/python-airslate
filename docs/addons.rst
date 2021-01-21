===============
Addons resource
===============


Methods
=======

Get access token for an installed addon
---------------------------------------

.. code-block:: python

   import json
   from airslate.client import Client

   client = Client()

   org_uid = '057C5000-0000-0000-0000D881'
   client_id = '32C2A810-0000-0000-000044D8'
   client_secret = 'b21877f468f839821b9c6744ee2b6941'

   identity = client.addons.access_token(org_uid, client_id, client_secret)

   print(json.dumps(identity, indent=2))


**Output:**

.. code-block:: json

   {
     "meta": {
       "token_type": "Bearer",
       "expires": "1800",
       "access_token": "6yWAkqNQaebbJUN14sen7e43ABiDpt1LlqHDkXekZjTH23ubYl8o9ae6osKynsgo",
       "refresh_token": "",
       "domain": "serghei"
     }
   }
