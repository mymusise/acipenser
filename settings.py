from django.conf import settings


class AcipenserRouter(object):
    """
    A router to control all database operations on models in the
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read question models go to question.
        """
        if model._meta.app_label == 'test_db':
            return 'test_db'

        # return "default"

    def db_for_write(self, model, **hints):
        """
        Attempts to write question models go to question.
        """
        if model._meta.app_label == 'test_db':
            return 'test_db'

        # return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the question app is involved.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the question app only appears in the 'question'
        database.
        """
        if db == 'test_db':
            return True
        return None


USER_SETTINGS = getattr(settings, 'ACIPENSER_TEST', {})

DEFAULT_SETTINGS = {
    "HOG_LIST" : [],
    "CUSTOM_LIST": [],
}

ACIPENSER_SETTINGS = {}

for key, value in DEFAULT_SETTINGS.items():
    user_value = USER_SETTINGS.get(key, None)
    if user_value:
        ACIPENSER_SETTINGS[key] = user_value
    else:
        ACIPENSER_SETTINGS[key] = DEFAULT_SETTINGS[key]