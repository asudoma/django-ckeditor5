#!/usr/bin/env python

from setuptools import setup, find_packages

version = __import__('ckeditor5').__version__

setup(
    name='django-ckeditor5',
    version=version,
    description='Django admin CKEditor5 integration.',
    author='Artem Sudoma',
    author_email='artem.sudoma@gmail.com',
    url='https://github.com/asudoma/django-ckeditor5',
    packages=find_packages(exclude=["*.demo"]),
    include_package_data=True
)
