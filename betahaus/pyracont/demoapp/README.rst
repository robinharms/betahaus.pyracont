
Demo app for transformations and content types
==============================================

While unit tests are nice, the real thing is important too...


Installing
----------

Run buildout with the file demo.cfg - it will install other
dependencies for this package.
Start the server with the demo.ini to test it. The database
will be created in memory with no persistance at all.


Functions
---------

There are 2 transformations registered for the demo. One that
creates links from hashtags on view, and one that adds any
hashtags to the tags-list if they're not already present there.
