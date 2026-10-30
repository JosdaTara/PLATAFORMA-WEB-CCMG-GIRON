from django.apps import AppConfig

class NucleoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nucleo'
    label = 'nucleo'
    verbose_name = 'Núcleo (auditoría, permisos, utilidades)'
