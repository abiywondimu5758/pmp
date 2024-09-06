class PublicSchemaRouter:
    """
    A router to control all database operations on models in the
    public schema applications.
    """

    def db_for_read(self, model, **hints):
        # Route read operations for token_blacklist to the public schema
        if model._meta.app_label == 'token_blacklist':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        # Route write operations for token_blacklist to the public schema
        if model._meta.app_label == 'token_blacklist':
            return 'default'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'token_blacklist':
            # Ensures migration happens in the 'default' database, which uses the public schema
            return db == 'default'
        return None
