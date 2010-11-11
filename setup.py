import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('cookiesession').__doc__.splitlines()).strip()

setup(
    name = 'django-cookiesession',
    version = __import__('cookiesession').get_version().replace(' ', '-'),
    url = 'http://github.com/washingtontimes/django-cookiesession',
    author = 'Justin Quick, Corey Oordt, The Washington Times',
    author_email = 'webdev@washingtontimes.com',
    description = DESC,
    long_description = read_file('README'),
    packages=find_packages(),
    include_package_data = True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
    ],
)