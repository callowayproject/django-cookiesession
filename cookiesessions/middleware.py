from base64 import b64decode, b64encode
from time import time

from django.contrib.sessions.backends.base import SessionBase
from django.core.exceptions import SuspiciousOperation
from django.utils import simplejson
from django.utils.http import cookie_date
from django.utils.hashcompat import sha_constructor
from django.contrib.auth.models import AnonymousUser

from settings import MAX_COOKIE_SIZE, USERNAME_COOKIE_NAME
from django.conf import settings

SESSION_COOKIE_DOMAIN = settings.SESSION_COOKIE_DOMAIN
SESSION_COOKIE_NAME = settings.SESSION_COOKIE_NAME
SESSION_COOKIE_PATH = settings.SESSION_COOKIE_PATH

class UsernameInCookieMiddleware(object):
    def process_response(self, request, response):
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            response.set_cookie(USERNAME_COOKIE_NAME, request.user.username, domain=SESSION_COOKIE_DOMAIN)
        elif hasattr(request, 'user')  and isinstance(request.user, AnonymousUser) and USERNAME_COOKIE_NAME in request.COOKIES:
            response.delete_cookie(USERNAME_COOKIE_NAME, domain=SESSION_COOKIE_DOMAIN)
        return response


class CookieSessionMiddleware(object):
    """
    Store the session information in a cookie that is secured against tampering
    """
    def process_request(self, request):
        cookie = request.COOKIES.get(SESSION_COOKIE_NAME)
        request.session = SessionStore(cookie)
    
    def process_response(self, request, response):
        try:
            session = request.session
        except AttributeError:
            return response
        if session.deleted:
            response.delete_cookie(SESSION_COOKIE_NAME,
                domain = SESSION_COOKIE_DOMAIN,
                path = SESSION_COOKIE_PATH
            )
        else:
            if session.modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = session.get_expiry_age()
                    expires = cookie_date(time() + max_age)
                cookie = session.encode(session._session)
                if len(cookie) <= MAX_COOKIE_SIZE:
                    response.set_cookie(SESSION_COOKIE_NAME, cookie,
                        max_age = max_age, expires=expires,
                        domain = SESSION_COOKIE_DOMAIN,
                        path = SESSION_COOKIE_PATH,
                        secure = settings.SESSION_COOKIE_SECURE or None
                    )
                else:
                    # The data doesn't fit into a cookie, not sure what's the
                    # best thing to do in this case. Right now, we just leave
                    # the old cookie intact if there was one. If Django had
                    # some kind of standard logging interface, we could also
                    # log a warning here.
                    pass
        return response


class SessionStore(SessionBase):
    def __init__(self, cookie):
        SessionBase.__init__(self, 'cookie')
        self.cookie = cookie
        self.deleted = False

    def exists(self, session_key):
        return self.cookie and not self.deleted

    def create(self):
        pass

    def save(self, must_create=False):
        pass

    def delete(self, session_key=None):
        self.deleted = True

    def load(self):
        if self.cookie:
            return self.decode(self.cookie)
        return {}

    def cycle_key(self):
        pass

    def encode(self, session_dict):
        json = simplejson.dumps(session_dict)
        json_sha = sha_constructor(json + settings.SECRET_KEY).hexdigest()
        try:
            return b64encode(str(json + json_sha).encode('zlib'))
        except Exception, e:
            return ''

    def decode(self, session_data):
        try:
            data = b64decode(session_data).decode('zlib')
        except Exception, e:
            return {}
        json, json_sha = data[:-40], data[-40:]
        if sha_constructor(json + settings.SECRET_KEY).hexdigest() != json_sha:
            raise SuspiciousOperation('User tampered with session cookie')
        return simplejson.loads(json)
