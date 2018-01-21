from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-odczdataset',
    version=version,
    description="Extenstion to support OpenData.cz methodology",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Jakub Kl\xc3\xadmek',
    author_email='klimek@opendata.cz',
    url='http://opendata.cz',
    license='pddl',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.odczdataset'],
    # include files form MANIFEST.in
    include_package_data=True,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        odczdataset=ckanext.odczdataset.plugin:ODCZDatasetFormPlugin
        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    ''',

    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
