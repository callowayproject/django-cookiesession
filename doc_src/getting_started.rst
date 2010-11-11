.. _getting_started:

===================================
Getting Started with Cookie Session
===================================

Installation
============

1. Install it from the `Python Package Index <http://pypi.python.org/>`_ :: 

	easy_install cookiesession

2. Comment out, or delete ``django.contrib.sessions.middleware.SessionMiddleware`` from settings.py's ``MIDDLEWARE_CLASSES`` setting.

3. Add cookiesession's middleware to your settings.py ``MIDDLEWARE_CLASSES`` ::

	MIDDLEWARE_CLASSES = (
	    'django.middleware.common.CommonMiddleware',
	    #'django.contrib.sessions.middleware.SessionMiddleware',
	    'cookiesessions.middleware.CookieSessionMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	)

4. *Optional.* In order to use the management commands you need to add ``cookiesession`` to settings.py's ``INSTALLED_APPS``

5. In settings.py (or local_settings.py) set ``SESSION_COOKIE_DOMAIN``, ``SESSION_COOKIE_NAME``, or ``SESSION_COOKIE_PATH`` as necessary (see `the Django session docs <http://docs.djangoproject.com/en/dev/topics/http/sessions/#session-cookie-domain>`_ for more info). 
   
   Developers will want to override the ``SESSION_COOKIE_DOMAIN`` with ``127.0.0.1`` and access their local development server as ``http://127.0.0.1:8000/``


How Cookie Session Works
========================

Cookies are inherently insecure and can't be trusted. Users have access to the values and can do what ever they want with them. So how could you ever put important data in a cookie?

There's a difference between "important" and "secret". Django only stores two pieces of data about the user in the session cookie: the user's id and the authentication backend used for authentication. Neither of these bits of information are "secret" in that knowing them can lead to security breaches. They are "important" in that we need them to retrieve the user's information.

However with cookies, a user could easily modify the user id stored in the cookie and suddenly be a different user. That means we need a way to detect a modification to the cookie.

The process is pretty straight forward:

1. The session dictionary is converted into a `JSON <http://json.org/>`_ string

2. A `SHA1 hash <http://en.wikipedia.org/wiki/SHA_hash_functions>`_ is made using the concatenation of the JSON string and the site's ``SECRET_KEY``. This creates a secure "fingerprint" of something unique: the session and your site's ``SECRET_KEY``. 

3. The JSON string and the SHA1 hash are concatenated, compressed and base64 encoded. Now the cookie contains the data, and a "fingerprint" that your site can use to ensure everything is as it should be.

When the user has logged in and makes a new request, we reverse the steps to verify the cookie hasn't been tampered with:

1. The cookie is decoded and decompressed

2. The data is split into the SHA1 hash and the JSON string

3. A new SHA1 hash is generated from the received JSON string and the site's ``SECRET_KEY``

4. If the hash received in the cookie doesn't match the newly generated hash, a ``SuspiciousOperation`` exception is raised. If the hashes match, the JSON string is converted into a python object and used.


