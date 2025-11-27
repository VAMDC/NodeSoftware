from django.core.management.base import BaseCommand
from valdimport import import_transitions


class Command(BaseCommand):
    help = 'Import transitions from VALD format (Pass 2)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Input file (or use stdin)')
        parser.add_argument('--batch-size', type=int, default=10000)
        parser.add_argument('--skip-header', type=int, default=2)
        parser.add_argument('--skip-calc', action='store_true',
                          help='Skip Einstein A calculation')

    def handle(self, *args, **options):
        processed = import_transitions(
            input_file=options['file'],
            batch_size=options['batch_size'],
            skip_header=options['skip_header'],
            skip_calc=options['skip_calc'],
            verbose=True
        )
        self.stdout.write(
            self.style.SUCCESS(f'Done! Imported {processed} transitions')
        )
