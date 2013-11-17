from unittest import TestCase

from poe.config import settings
from poe.web_api.session import (
    PathSession, InvalidLoginException
)


class PathSessionTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = PathSession(settings["USERNAME"], settings["PASSWORD"])

    def test_good_login(self):
        pass

    def test_bad_login(self):
        self.assertRaises(InvalidLoginException, PathSession,
                          username="bad", password="login")

    def test_get_stash_good(self):
        self.session.get_stash(league="nemesis")

    def test_get_stash_bad(self):
        self.assertEquals(self.session.get_stash_tab(league="bad_league"), None)
