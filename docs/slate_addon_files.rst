=================
Slate Addon Files
=================


.. note::

   To obtain ``token`` refer to ``airslate.addons.auth()`` method.


Download contents of the requested file
---------------------------------------

.. code-block:: python

   import os
   from airslate.client import Client

   org_id = '057C5000-0000-0000-0000D981'
   file_id = 'D77F5000-0000-0000-0000AE67'

   client = Client(
       token=os.getenv('API_TOKEN'),
       headers={'Organization-Id': org_id}
   )

   local_filename = 'example.json'
   stream = client.addons.files.download(file_id)

   # With the following streaming code, the Python memory usage is
   # restricted regardless of the size of the downloaded file:
   with stream as r:
       with open(local_filename, 'wb') as f:
           for chunk in r.iter_content(chunk_size=512):
               f.write(chunk)


Get the requested Slate Addon file
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

   file = client.addons.files.get(file_id)
   print(file)
   print(file.name, file.size)
   print(file.object_meta['download_url'])

   addon = file.slate_addon
   print(addon)

.. raw:: html

   <details><summary>Output</summary>

.. code-block::

   <SlateAddonFile: id=D77F5000-0000-0000-0000AE67, type=slate_addon_files>
   my_file.csv 733
   https://api.airslate.com/v1/slate-addon-files/C41CDE20-0000-0000-000045B9/download
   <SlateAddon: id=09867A00-0000-0000-000093F0, type=slate_addons>
