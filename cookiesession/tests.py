import sys
from StringIO import StringIO
from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User

from cookiesession.middleware import SessionStore
from cookiesession.management.commands.decode_session_cookie import Command as DecodeCommand
from cookiesession.management.commands.encode_session_cookie import Command as EncodeCommand

def decode_cookie(cookie):
    return SessionStore(cookie).load()
    

class TestCookieSessions(TestCase):
    """Unit tests for cookiesessions"""
    
    def setUp(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user('testuser', 'test@example.com', 'secret')
        user.is_staff = True
        user.save()
    
    def testLogin(self):
        c = Client()
        # The first request gets the "testcookie"
        r = c.get('/login/')
        r = c.post('/login/', {'username': 'testuser', 'password': 'secret'})
        session = decode_cookie(r.cookies.get('sessionid').value)
        
        # Should redirect you somewhere if successful
        self.assertEquals(r.status_code, 302)
        self.assertTrue(session.has_key('_auth_user_id'))
        self.assertTrue(session.has_key('_auth_user_backend'))
        user = User.objects.get(pk=session['_auth_user_id'])
        self.assertTrue(user.username, 'testuser')
        
    def test_encode_decode(self):
        testdata = {'foo': 'bar'}
        self.assertEqual(decode_cookie(SessionStore('').encode(testdata)), testdata)
        
        
    def test_management(self):
        out = sys.stdout
        sys.stdout = StringIO()
        
        EncodeCommand().handle('foo=bar')
        self.assertEqual(sys.stdout.getvalue(), 'eJyrVkrLz1eyUlBKSixSqjUzTDM3TzFNNE1LSbM0NEg1TrGwNDczNjdMTE01SU0ytUwzMk40sUgBALJ3D40=\n')

        DecodeCommand().handle(sys.stdout.getvalue())
        self.assertEqual(sys.stdout.getvalue().replace("u'","'"), "eJyrVkrLz1eyUlBKSixSqjUzTDM3TzFNNE1LSbM0NEg1TrGwNDczNjdMTE01SU0ytUwzMk40sUgBALJ3D40=\n{'foo': 'bar'}\n")

        sys.stdout = out
