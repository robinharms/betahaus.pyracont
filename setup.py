import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = ('pyramid',
            'repoze.folder',
            'slugify',
            'pytz',
            'ZODB3',
            'colander',
            'zope.interface',
            'zope.component',
            )

setup(name='betahaus.pyracont',
      version='0.2b',
      description='betahaus.pyracont',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        ],
      author='Robin Harms Oredsson and contributors',
      author_email='robin@betahaus.net',
      url='https://github.com/robinharms/betahaus.pyracont',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="betahaus.pyracont",
      entry_points = """\
      """,
      )
