==========================
Cookie Sessions for Django
==========================

This package contains a drop-in replacement middleware for ``django.contrib.sessions.middleware.SessionMiddleware`` to store all session data in a browser cookie instead of the database. The code is based on 
`a snippet from Christopher Lenz.  <http://http://scratchpad.cmlenz.net/370f3e0d58804d38c3bc14e514272fda/>`_ 

To prevent user tampering the session dictionary goes through the following encoding steps:

1. The session dictionary is converted into ``json``
2. A ``sha1`` hash is made with the ``json`` and the site's ``SECRET_KEY``
3. The ``json`` and ``sha1`` hash are concatenated, gzipped and base64 encoded.

Upon decoding:

1. The cookie is base64 decoded and ungzipped
2. The data is split into the ``sha1`` hash and the ``json`` data
3. The ``sha1`` hash is regenerated from the received ``json`` data and the site's ``SECRET_KEY``
4. If the hashes don't match, a ``SuspiciousOperation`` exception is raised. If the hashes match, the ``json`` data is converted into a python object and returned.

Management Commands
===================

Two management commands are included to make debugging things easier.

``decode_session_cookie``
   Called as ``./manage.py decode_session_cookie <session_cookie_string>`` and prints the keys and values of the session dictionary.


``encode_session_cookie``
   Encodes key=val arguments into a cookie for manual insertion into your browser for testing purposes. You must call the command as ``./manage.py encode_cookie key1=value key2=value``
