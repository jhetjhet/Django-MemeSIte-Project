#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
	name='Memeniac',
	version='1.0',
	packages=find_packages(),
	scripts=['manage.py'],

	install_required=[
		'Python==3.7.7',
		'Django==3.0.8',
		'channels==2.4.0==2.4.0',
		'channels-redis==2.4.2',
		'django-crispy-forms==1.9.1',
		'Pillow==7.2.0,'
	],

	author='Austin',
	author_email='villasanamallariaustin@gmail.com',
	description='',
)