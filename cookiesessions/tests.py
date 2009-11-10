import unittest
from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from django.contrib.auth.models import User

def decode_cookie(cookie):
    from cookiesessions.middleware import SessionStore
    session = SessionStore(cookie)
    return session.load()
    

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
        