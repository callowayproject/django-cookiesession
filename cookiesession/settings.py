from django.conf import settings

USERNAME_COOKIE_NAME = getattr(settings, 'USERNAME_COOKIE_NAME', 'username')

MAX_COOKIE_SIZE = getattr(settings, 'MAX_COOKIE_SIZE', 4096)
