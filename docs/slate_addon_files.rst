=================
Slate Addon Files
=================


Get the requested slate addon file
----------------------------------


.. code-block:: python

   import os
   from airslate.client import Client

   org_id = '057C5000-0000-0000-0000D981'
   file_id = 'D77F5000-0000-0000-0000AE67'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   file = client.slate_addon_files.get(file_id)
   print(file)
   print(file['name'], file['size'])

   addon = file.slate_addon
   print(addon)

.. raw:: html

   <details><summary>Output</summary>

.. code-block::

   <SlateAddonFile: id=D77F5000-0000-0000-0000AE67, type=slate_addon_files>
   my_file.csv 733
   <SlateAddon: id=09867A00-0000-0000-000093F0, type=slate_addons>

.. note::

   To obtain ``token`` refer to ``airslate.addons.access_token()`` method.
