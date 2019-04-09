class DatradebotRouter(object):
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to datradebot_db.
        """
        if model._meta.app_label == 'datradebot':
            return 'datradebot_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to datradebot_db.
        """
        if model._meta.app_label == 'datradebot':
            return 'datradebot_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the datradebot app is involved.
        """
        if obj1._meta.app_label == 'datradebot' or obj2._meta.app_label == 'datradebot':
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'datradebot_db'
        database.
        """
        if app_label == 'datradebot':
            return db == 'datradebot_db'
        return None
