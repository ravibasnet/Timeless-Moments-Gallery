from django.contrib import admin
from django.apps import apps

class CustomAdminSite(admin.AdminSite):
    site_header = 'Timeless Moments Administration'
    site_title = 'Timeless Moments Admin Portal'
    index_title = 'Dashboard'

    def __init__(self, name='admin'):
        super().__init__(name)
        # Auto-register all models
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                try:
                    self.register(model)
                except admin.sites.AlreadyRegistered:
                    pass

# Create default admin site instance
admin_site = CustomAdminSite(name='admin')
