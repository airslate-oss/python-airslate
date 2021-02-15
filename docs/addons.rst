===============
Addons resource
===============


Get access token for an installed Addon
---------------------------------------

.. code-block:: python

   import json
   from airslate.client import Client

   client = Client()

   identity = client.addons.auth(
       org_id='057C5000-0000-0000-0000D981',
       client_id='32C2A810-0000-0000-000044D8',
       client_secret='b21877f468f839821b9c6744ee2b6941',
   )

   print(json.dumps(identity, indent=2))

.. raw:: html

   <details><summary>Output</summary>

.. code-block:: json

   {
     "meta": {
       "token_type": "Bearer",
       "expires": 1800,
       "access_token": "6yWAkqNQaebbJUN14sen7e43ABiDpt1LlqHDkXekZjTH23ubYl8o9ae6osKynsgo",
       "refresh_token": "",
       "domain": "testorg"
     }
   }
