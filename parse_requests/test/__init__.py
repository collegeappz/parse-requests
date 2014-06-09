import unittest
from nose.tools import assert_equal
from parse_requests.classes import set_keys
from parse_requests.classes.User import User


class BaseTestCase(unittest.TestCase):
    # TODO: add setUp(), tearDown()
    pass


class TestCase(BaseTestCase):
    def test_get_all_users(self):
        # no auth
        user = User()
        assert_equal(user.get(), {u'error': u'unauthorized'})
