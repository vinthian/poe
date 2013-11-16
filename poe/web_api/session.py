import json
import logging

import mechanize


logger = logging.getLogger(__name__)


class InvalidLoginException(Exception):
    def __init__(self, msg):
        super(InvalidLoginException, self).__init__(self, msg)
        logger.debug("Invalid login exception")


class DataNotFoundException(Exception):
    def __init__(self, msg):
        super(DataNotFoundException, self).__init__(self, msg)
        logger.debug("Data not found exception")


class PathSession(object):
    URLS = {
        "login": "https://www.pathofexile.com/login",
        "account": "https://www.pathofexile.com/my-account",
        "stash": "http://www.pathofexile.com/character-window/get-stash-items",
    }

    def __init__(self, username, password):
        self.username = username
        self.br = mechanize.Browser()
        self.br.open(self.URLS["login"])
        self.br.select_form(nr=0)
        self.br.form["login_email"] = username
        self.br.form["login_password"] = password
        logger.debug("Logging in as %s" % username)
        self.br.submit()

        self.br.open(self.URLS["account"])
        if self.br.geturl() != self.URLS["account"]:
            raise InvalidLoginException("Could not log in")

    def get_stash(self, league="standard"):
        url = self.URLS["stash"] + ("?league=%s" % league)
        logger.debug("Grabbing stash for %s: %s" % (self.username, url))
        response = self.br.open(url)
        content = response.read()

        try:
            data = json.loads(content)
            if data is False:
                raise DataNotFoundException("No data returned")
        # I don't think this ever happens
        except ValueError:
            raise DataNotFoundException("Invalid data returned")

        logger.debug("response: %s" % data)