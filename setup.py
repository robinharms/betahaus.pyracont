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
            )

setup(name='betahaus.pyracont',
      version='0.1a1',
      description='betahaus.pyracont',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        ],
      author='Robin Harms Oredsson',
      author_email='robin@betahaus.net',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="betahaus.pyracont",
      entry_points = """\
      """,
      paster_plugins=['pyramid'],
      )

