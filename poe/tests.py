from unittest import TestCase

from poe.config import settings
from poe.web_api.session import (
    PathSession, InvalidLoginException, DataNotFoundException
)


class PathSessionTestCase(TestCase):
    def setUp(self):
        self.username = settings["USERNAME"]
        self.password = settings["PASSWORD"]

    def test_good_login(self):
        session = PathSession(self.username, self.password)
        del session

    def test_bad_login(self):
        session = PathSession
        self.assertRaises(InvalidLoginException, PathSession,
                          username="bad", password="login")
        del session

    def test_get_stash(self):
        session = PathSession(self.username, self.password)
        # good
        session.get_stash(league="nemesis")
        # bad
        self.assertRaises(DataNotFoundException, session.get_stash,
                          league="bad_league")
        del session
