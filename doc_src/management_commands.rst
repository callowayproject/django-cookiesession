.. _management_commands:

===================
Management Commands
===================

If you have added ``cookiesession`` to your ``INSTALLED_APPS``, you will have access to the following commands:

.. _decode_session_cookie:

``decode_session_cookie``
=========================

Decodes a cookie string into the python object and prints out the keys and their values, for example::

	$ ./manage.py decode_session_cookie eJwFwVsKgCAQBdCtxKxAM8Zru5F5gPgxUEIf0d4756V...
	
	_auth_user_id: 1
	_auth_user_backend: django.contrib.auth.backends.ModelBackend

``encode_session_cookie``
=========================

Encodes key-value pairs into a valid session cookie::

	$ ./manage.py encode_session_cookie _auth_user_id=1 \
	  _auth_user_backend=django.contrib.auth.backends.ModelBackend
	
	eJwFwVsKgCAQBdCtxKxAM8Zru5F5gPgxUEIf0d4756V...
