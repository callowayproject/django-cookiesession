from django.core.management.base import BaseCommand
from middleware.cookie import SessionStore

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if args:
            session = SessionStore(args[0])
            session_key = session.load()
            for item in session_key.items():
                print '%s : %s' % item
            return
        else:
            print "Please include a cookie string."
            return
        