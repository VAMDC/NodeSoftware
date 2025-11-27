from django.apps import AppConfig
import decimal


class NodeConfig(AppConfig):
    name = 'node'

    def ready(self):
        # Fix DecimalField quantization errors in Django's SQLite backend
        # Django creates decimal contexts with prec=max_digits, but quantization
        # operations need extra precision headroom to work correctly
        from .models import State, Transition, Species

        for model in [State, Transition, Species]:
            for field in model._meta.get_fields():
                if hasattr(field, 'context') and isinstance(field.context, decimal.Context):
                    min_prec = field.max_digits + field.decimal_places + 10
                    if field.context.prec < min_prec:
                        field.context = decimal.Context(prec=min_prec)
