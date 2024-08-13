class YourAuthRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'auth_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'auth_db'
        return 'default'
