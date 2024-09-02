from django.apps import AppConfig

class AdminManagementConfig(AppConfig):
    name = 'Admin_Management'

    def ready(self):
        import Admin_Management.signals  # Adjust the import path according to your project structure
