betahaus.pyracont README
========================

.. image:: https://travis-ci.org/robinharms/betahaus.pyracont.png?branch=master
  :target: https://travis-ci.org/robinharms/betahaus.pyracont

This packages main goal is to provide:

* Basic ZODB-based content type skeleton for `Pyramid <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_.
* Dynamic content types that can be adapted to pretty much suit most purposes.
* Ability to make highly pluggable components sutable for frameworks.
* Easy integration with `colander <http://docs.pylonsproject.org/projects/colander/en/latest/>`_.

This package currently lacks proper documentation, but should be pretty stable regarding API changes since it's used
in production in other open source projects.


Possible TODOs:
---------------
* Custom field adapters instead of custom field types. No point in storing persistent content types unless needed.
* With field adapters content types don't need special settings.
* This might require an introspection tool, otherwise it might appear to "magical".
* A way to transform input before it's saved.
