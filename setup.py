from setuptools import setup, find_packages

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

packages = find_packages()
packages.remove('example')

setup(name='django-cookiesession',
      version='0.1.1',
      description='A secure way to hold Django session data in cookies',
      long_description=long_description,
      author='Justin Quick, The Washington Times',
      author_email='jquick@washingtontimes.com',
      url='http://github.com/washingtontimes/django-cookiesession',
      packages=packages,
      classifiers=['Development Status :: 4 - Beta',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          ],
      )