# coding: utf-8
import os
import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = "ElasticSearch ODM inspired by MongoEngine, for docs please visit the homepage."


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()

# grep toute/__init__.py since python 3.x cannot import it
file_text = read(fpath('lib/toute/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval

setup(
    name='toute',
    version="1.2.1",
    url='https://github.com/eshta/toute',
    license='MIT',
    author="Omar Shaban",
    author_email="omars@php.net",
    description='ElasticSearch ODM inspired by MongoEngine',
    long_description=long_description,
    packages=find_packages("lib"),
    package_dir={"": "lib"},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=["python-dateutil", "six>=1.12.0"],
    tests_require=[
        "pytest==2.8.3",
        "pytest-cov==2.2.0",
        "flake8==2.5.0",
        "pep8-naming==0.3.3",
        "flake8-debugger==1.4.0",
        "flake8-print==2.0.1",
        "flake8-todo==0.4",
        "radon==1.2.2"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
