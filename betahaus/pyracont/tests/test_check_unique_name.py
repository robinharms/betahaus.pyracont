from unittest import TestCase

from pyramid import testing


def _dummy_func(*args):
    pass


class DecoratorFieldFactoryTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from betahaus.pyracont import check_unique_name
        return check_unique_name

    def test_not_existing(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.assertEqual(self._fut(context, request, 'i_dont_exist'), True)

    def test_existing_in_context(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        context['hello'] = testing.DummyResource()
        context['hello-1'] = testing.DummyResource()
        self.assertEqual(self._fut(context, request, 'hello'), False)
        self.assertEqual(self._fut(context, request, 'hello-1'), False)
        self.assertEqual(self._fut(context, request, 'hello-2'), True)

    def test_existing_view(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.config.add_view(_dummy_func, name = "this_name")
        self.assertEqual(self._fut(context, request, 'this_name'), False)
        self.assertEqual(self._fut(context, request, 'this_name-1'), True)

    def test_existing_view_request_method(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.config.add_view(_dummy_func, name = "this_name", request_method = 'POST')
        self.assertEqual(self._fut(context, request, 'this_name'), False)
        self.assertEqual(self._fut(context, request, 'this_name-1'), True)

    def test_existing_view_specific_context(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.config.add_view(_dummy_func, name = "this_name", context = testing.DummyResource)
        self.assertEqual(self._fut(context, request, 'this_name'), False)
        self.assertEqual(self._fut(context, request, 'this_name-1'), True)

    def test_existing_but_other_context(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.config.add_view(_dummy_func, name = "this_name", context = object)
        self.assertEqual(self._fut(context, request, 'this_name'), True)

    def test_existing_view_with_permission(self):
        self.config.testing_securitypolicy(userid = 'dummy', permissive = False)
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.config.add_view(_dummy_func, name = "this_name", permission = 'some_perm')
        self.assertEqual(self._fut(context, request, 'this_name'), False)
        self.assertEqual(self._fut(context, request, 'this_name-1'), True)

