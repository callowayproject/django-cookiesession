"""
This is great for testing. It allows you to set the cookie up by passing it 
keywords and arguments
"""
from django.core.management.base import LabelCommand
from django.utils import simplejson
from cookiesession.middleware import SessionStore


class Command(LabelCommand):
    help = """Encodes key=val arguments into a cookie for manual insertion 
    into your browser for testing purposes. You must call the command:
    
    ./manage.py encode_cookie key1=value key2=value"""
    _cookie_dict = {}
    
    def handle(self, *labels, **options):
        super(Command, self).handle(*labels, **options)
        print SessionStore('').encode(self._cookie_dict)
    
    def handle_label(self, label, **options):
        key, val = label.split('=')
        self._cookie_dict[key] = val