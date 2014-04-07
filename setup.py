from distutils.core import setup

version = '1.1'

setup(name='pyrolibrary',
      version=version,
      description="Robot Framework Selenium2Library wrapper that integrates both Sauce and Sencha custom ui commands",
      long_description="""\
Robot Framework Selenium2Library wrapper that integrates both Sauce and Sencha custom ui commands""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='selenium python pybot factory sauce teamcity',
      author='Tallis Vanek',
      author_email='talliskane@gmail.com',
      url='https://github.com/Tallisado/pyrolibrary',
      license='',
      packages = ['PyroLibrary','PyroLibrary.keywords','PyroLibrary.utils'],
      package_dir  = {'' : 'src'},
      install_requires=[
          'robotframework >= 2.6.0',
          "robotframework-selenium2library",
      ],
      include_package_data = True,
)