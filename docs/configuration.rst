=============
Configuration
=============

Client Options
==============

Various options can be set globally on the ``Client.DEFAULT_OPTIONS`` object,
per-client on ``client.options``, or per-request as additional named arguments.
For example:

.. code-block:: python

   # global
   airslate.Client.DEFAULT_OPTIONS['max_retries'] = 2

   # per-client
   client.options['max_retries'] = 2

Available options
-----------------

- ``base_url`` (default: "https://api.airslate.com"): API endpoint base URL to connect to
