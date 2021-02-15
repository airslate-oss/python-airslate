=============
Configuration
=============


Client Options
==============

Various options can be set globally on the ``Client.DEFAULT_OPTIONS`` object,
per-client on ``client.options``, or per-request as additional named arguments.
For example:

.. code-block:: python

   from airslate.client import Client


   # global
   Client.DEFAULT_OPTIONS['timeout'] = 10.0

   # per-client
   client = Client(timeout=10.0)
   client.options['timeout'] = 10.0

   # per-request
   client.post('/v1/addon-token', {}, timeout=10.0)


Available options
-----------------

- ``base_url`` (default: "https://api.airslate.com"): API endpoint base URL to connect to.
- ``timeout`` (default: 5.0): The time stop waiting for a response after a given number of seconds.
  It is not a time limit on the entire response download; rather, an exception is raised if the
  server has not issued a response for ``timeout`` seconds (more precisely, if no bytes have been
  received on the underlying socket for ``timeout`` seconds).
- ``full_response`` (default: False): Return the entire JSON response or just ``data`` section.
  This option should only be modified for direct calls of the client's methods
  (e.g. ``client.get()``, ``client.post()``, etc). Resource classes can depend on the default
  value of this option.

The following options can be set only globally:

- ``max_retries`` (default: 3): The number to times to retry if API rate limit is reached or a
  server error occurs. Rate limit retries delay until the rate limit expires, server errors
  exponentially backoff starting with a 1 second delay. The algorithm is as follows:

.. code-block::

  {backoff factor} * (2 ** ({number of total retries} - 1))
