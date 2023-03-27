=============
Organizations
=============

Get a list of Organizations
---------------------------

Get a list of all Organizations that the current user belongs to.

.. code-block:: python

   from pathlib import Path
   from airslate.client import Client


   client = Client.jwt_session(
       client_id='00000000-0000-0000-0000-000000000000',
       user_id='00000000-0000-0000-0000-000000000000',
       key=Path('oauth-private.key').read_bytes(),
   )

   organizations = client.organizations.collection()
   for org in organizations:
       print(org)
       print(org.to_dict(), '\n')

.. raw:: html

   <details><summary>Output</summary>

.. code-block::

    <Organization: id=5FFE553A-2200-0000-0000D981>
    {'id': '5FFE553A-2200-0000-0000D981', 'name': 'Acme', 'subdomain': 'acme', 'category': 'PROFESSIONAL_AND_BUSINESS', 'size': '0-5', 'status': 'FINISHED', 'created_at': '2022-02-09T09:44:58Z', 'updated_at': '2022-10-28T03:59:10Z'

    <Organization: id=5FFE553A-2200-0000-0000D982>
    {'id': '5FFE553A-2200-0000-0000D982', 'name': 'MyOrg', 'subdomain': 'myorg', 'category': 'WHOLESALE_TRADE', 'size': '1001-2000', 'status': 'FINISHED', 'created_at': '2019-07-31T14:36:21Z', 'updated_at': '2023-03-09T03:59:09Z'
