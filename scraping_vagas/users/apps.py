from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "scraping_vagas.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import scraping_vagas.users.signals  # noqa F401
        except ImportError:
            pass
