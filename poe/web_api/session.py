import json
import logging
import urlparse

import time
import mechanize

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from poe.config import settings
from poe.web_api.models import Base, StashTab, Item, get_or_create


logger = logging.getLogger(__name__)


class InvalidLoginException(Exception):
    def __init__(self, msg):
        super(InvalidLoginException, self).__init__(self, msg)
        logger.debug("Invalid login exception")


class NotLoggedInException(Exception):
    def __init__(self, msg):
        super(NotLoggedInException, self).__init__(self, msg)
        logger.debug("Not logged in exception")


class DataNotFoundException(Exception):
    def __init__(self, msg):
        super(DataNotFoundException, self).__init__(self, msg)
        logger.debug("Data not found exception")


class PathBrowser(mechanize.Browser, object):
    def __init__(self, *args, **kwargs):
        super(PathBrowser, self).__init__(*args, **kwargs)
        self.set_handle_robots(False)

    def open(self, *args, **kwargs):
        url = args[0]
        try:
            logger.info("%s %s" % (url.get_full_url(), url.get_method()))
            if url.has_data():
                logger.info(urlparse.parse_qs(url.get_data()))
        except AttributeError:
            logger.info(url)
        return super(PathBrowser, self).open(*args, **kwargs)


class PathSession(object):
    def __init__(self):
        self.br = PathBrowser()
        self.logged_in = False
        self.initdb()

    def login(self, username, password):
        self.br.open(settings["URL_LOGIN"])
        self.br.select_form(nr=0)
        self.br.form["login_email"] = username
        self.br.form["login_password"] = password
        self.br.submit()

        self.br.open(settings["URL_ACCOUNT"])
        if self.br.geturl() != settings["URL_ACCOUNT"]:
            self.logged_in = False
            return False
            # raise InvalidLoginException("Could not log in")

        self.logged_in = True
        return True

    def initdb(self):
        self.engine = create_engine("sqlite:///%s" % settings["DB_PATH"])
        # always reset the db on a new session
        initdb(self)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker()
        DBSession.bind = self.engine
        self.db = DBSession()

    def logged_in(func):
        from functools import wraps
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.logged_in:
                return func(self, *args, **kwargs)
            else:
                raise NotLoggedInException("Not logged in")
        return wrapper

    @logged_in
    def get_stash(self, league="standard"):
        result = True
        tab_index = 0
        # TODO: temporary override of max number of stash tabs for testing
        while result is not None and tab_index < 1:
            delay = 0 if tab_index % 5 == 0 else 0
            # TODO: Threading
            stash_tab = self.get_stash_tab(league, tab_index, delay)

            items = []

            tab = get_or_create(
                self.db,
                StashTab,
                league=stash_tab["items"][0]["league"],
                name=stash_tab["items"][0]["inventoryId"],
                tab_index=tab_index)

            for item in stash_tab["items"]:
                items.append(Item(
                    stash_tab=tab,
                    name=item["name"],
                    icon=item["icon"],
                    type_line=item["typeLine"],
                    verified=item["verified"],
                    identified=item["identified"],
                    support=item["support"],
                    frame_type=item["frameType"],
                    w=item["w"],
                    h=item["h"],
                    x=item["x"],
                    y=item["y"]))

            self.db.add(tab)
            self.db.add_all(items)
            self.db.commit()

            tab_index += 1

    @logged_in
    def get_stash_tab(self, league="standard", tab=0, delay=0):
        time.sleep(delay)
        url = settings["URL_STASH"] + ("?league=%s&tabIndex=%s" % (league, tab))
        response = self.br.open(url)
        content = response.read()

        try:
            data = json.loads(content)
            if data is False:
                return None

        # I don't think this ever happens
        except ValueError:
            raise DataNotFoundException("Invalid data returned")

        logger.info(data)

        return data


def initdb(session):
    import os

    if os.path.exists(settings["DB_PATH"]):
        os.remove(settings["DB_PATH"])
    Base.metadata.create_all(session.engine)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "initdb":
        session = PathSession()
        initdb(session)

    if sys.argv[1] == "get_stash":
        session = PathSession()
        session.get_stash(league=sys.argv[2])
