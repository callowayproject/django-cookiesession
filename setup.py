#!/usr/bin/env python

from distutils.core import setup
try:
    f = open('README.rst', 'r')
    long_description = f.read()
    f.close()
except IOError:
    long_description = ''

setup(name='cookiesession',
      version='0.1',
      description='A secure way to hold Django session data in cookies',
      long_description=long_description,
      author='Justin Quick, The Washington Times',
      author_email='jquick@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/cookiesession/',
      packages=['cookiesession'],
      classifiers=['Development Status :: 4 - Beta',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          ],
      )