"""parse-rest-python - A fast and simple Python library to interact with Parse.com REST API

parse-rest-python is a fast and simple Python library to interact with Parse.com REST API.
It's a simple wrapper over the Parse.com REST API. It returns data in JSON format.

Example Usage
-------------

Contribute
----------
This library is hosted on Github, please make a pull request to contribute:
https://github.com/collegeappz/parse_requests
"""
doc = __doc__.splitlines()

from setuptools import setup
repo_url = "https://github.com/collegeappz/parse_requests"

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 2
Topic :: Software Development :: Quality Assurance
""".splitlines()

setup(
    name="parse_requests",
    version="1.0.0",
    zip_safe=False,
    author='Kien Pham',
    author_email='kien@collegeappz.com',
    url="https://github.com/collegeappz/parse_requests",
    license="MIT",
    description=doc[0],
    long_description='\n'.join(doc[2:]),
    install_requires=['requests'],
    extras_require={
        'test': [
            'nose',
            'coverage',
            'mock'
        ]
    },
    test_suite="test",
    keywords="parse.com parse api rest",
    classifiers=classifiers
)
