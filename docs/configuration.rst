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

   # per-request
   client.post(
       '/v1/addon-token',
       {},
       max_retries=2,
   )

Available options
-----------------

- ``base_url`` (default: "https://api.airslate.com"): API endpoint base URL to connect to.
- ``timeout`` (default: 5.0): stop waiting for a response after a given number of seconds
  with the ``timeout`` option. It is not a time limit on the entire response download; rather,
  an exception is raised if the server has not issued a response for ``timeout`` seconds
  (more precisely, if no bytes have been received on the underlying socket for ``timeout`` seconds).
- ``max_retries`` (default: 5): number to times to retry if API rate limit is reached or a
  server error occurs. Rate limit retries delay until the rate limit expires, server errors
  exponentially backoff starting with a 1 second delay.
