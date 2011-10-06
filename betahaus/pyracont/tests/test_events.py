from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass


class EventsTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.events import ObjectUpdatedEvent
        return ObjectUpdatedEvent

    def test_verify_class(self):
        from betahaus.pyracont.interfaces import IObjectUpdatedEvent
        self.failUnless(verifyClass(IObjectUpdatedEvent, self._cut))

    def test_verify_obj(self):
        from betahaus.pyracont.interfaces import IObjectUpdatedEvent
        self.failUnless(verifyObject(IObjectUpdatedEvent, self._cut(object())))
