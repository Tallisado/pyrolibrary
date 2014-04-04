from setuptools import setup, find_packages
import sys, os

version = '1.1'

setup(name='PyroLibrary',
      version=version,
      description="Robot Framework Selenium2Library wrapper that integrates both Sauce and Sencha custom ui commands",
      long_description="""\
Robot Framework Selenium2Library wrapper that integrates both Sauce and Sencha custom ui commands""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='selenium python pybot factory sauce teamcity',
      author='Tallis Vanek',
      author_email='talliskane@gmail.com',
      url='https://github.com/Tallisado/pyrofactory',
      license='',
      packages=['PyroLibrary'],
      package_dir={'pyro_library': 'src/pyro_library'},
      install_requires=[
          "robotframework-selenium2library",
      ],
      )