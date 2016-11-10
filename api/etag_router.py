__author__ = 'mstacy'
class EtagRouter(object):
    """
    A router to control all database operations on models in the
    purple_martin application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read purple_martin models go to purple db.
        """
        if model._meta.app_label == 'etag':
            return 'etag'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write purple_martin models go to purple db.
        """
        if model._meta.app_label == 'etag':
            return 'etag'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the purple martin app is involved.
        """
        if obj1._meta.app_label == 'etag' or \
           obj2._meta.app_label == 'etag':
           return True
        return None

     #def allow_migrate(self, db, model):
     #   """
     #   Make sure the auth app only appears in the 'auth_db'
     #   database.
     #   """
     #   if db == 'etag':
     #       return model._meta.app_label == 'etag'
     #   elif model._meta.app_label == 'purple_martin':
     #       return False
     #   return None
