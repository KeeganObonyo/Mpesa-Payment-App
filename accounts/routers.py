from django.conf import settings


def decide_on_model(model):
    """Small helper function to pipe all DB operations of a worlddata model to the world_data DB"""
    return 'default' if model._meta.app_label == 'accounts' else None


class AuthRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return decide_on_model(model)

    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are part of the accounts app
        if obj1._meta.app_label == 'accounts' and obj2._meta.app_label == 'accounts':
            return True
        # Allow if neither is part of worlddata app
        elif 'accounts' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        # by default return None - "undecided"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # allow migrations on the "default" (django related data) DB
        if db == 'personnel_data' and app_label != 'accounts':
            return True

        # allow migrations on the legacy database too:
        # this will enable to actually alter the database schema of the legacy
        # DB!
        if db == 'default' and app_label == "accounts":
            return True

        return False
