import json
import pickle
from sync.language import LANGUAGES
from logging import getLogger

from sync.defaults import LOCALBOX_PREFERENCES_PATH, DEFAULT_LANGUAGE


class PreferencesController:
    def __init__(self, lazy_load=False):
        self._prefs = Preferences()

        if not lazy_load:
            self.load()

    def save(self):
        getLogger(__name__).debug('Saving preferences: %s' % self._prefs)
        pickle.dump(self._prefs, open(LOCALBOX_PREFERENCES_PATH, 'wb'))

    def load(self):
        getLogger(__name__).debug('Loading preferences: %s' % self._prefs)
        try:
            f = open(LOCALBOX_PREFERENCES_PATH, 'rb')
            self._prefs = pickle.load(f)
        except IOError:
            getLogger(__name__).warn('%s does not exist' % LOCALBOX_PREFERENCES_PATH)
            self.prefs.language = DEFAULT_LANGUAGE
            self.save() # to disable the warning on the following runs
        return self._prefs

    @property
    def prefs(self):
        return self._prefs

    def get_language_abbr(self):
        """
        Get language abreviation from preferences.
        gettext.translation receives an abbreviation
        :return:
        """
        return LANGUAGES[self._prefs.language if self._prefs.language else DEFAULT_LANGUAGE]


class Preferences:
    def __init__(self):
        self.language = None

    def __str__(self):
        return json.dumps(self.__dict__)


ctrl = PreferencesController()