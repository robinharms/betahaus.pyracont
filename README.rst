betahaus.pyracont
=================

.. image:: https://travis-ci.org/robinharms/betahaus.pyracont.png?branch=master
  :target: https://travis-ci.org/robinharms/betahaus.pyracont

Basic ZODB-based content type skeleton for Pyramid.

Essentially, we noticed that most projects we did ended up having the same
skeleton. This is to make them more reusable. While testing coverage is 100%,
we seriously lack documentation and more field-testing, hence this is released
as alpha.


TODO:
Custom field adapters instead of custom field types. No point in storing persistent content types unless needed.
With field adapters content types don't need special settings.
This might require an introspection tool, otherwise it might appear to "magical".
