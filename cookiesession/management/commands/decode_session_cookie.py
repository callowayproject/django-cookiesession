from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from cookiesession.middleware import SessionStore


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not args:
            raise CommandError('Please include a cookie string to decode')
        pprint(SessionStore(args[0]).load())
    