# coding: utf-8
from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name = 'mworkflow',
    version = version,
    description = 'A Worflow API'
    author = 'Mauricio Lima',
    author_email = 'arkanjuca@gmail.com',
    url='http://github.com/mworkflow',
    packages = find_packages(),
    zip_safe = False,
    include_package_data = True,
)
