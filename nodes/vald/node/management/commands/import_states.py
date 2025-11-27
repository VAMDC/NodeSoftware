from django.core.management.base import BaseCommand
from valdimport import import_states


class Command(BaseCommand):
    help = 'Import states from VALD format (Pass 1)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Input file (or use stdin)')
        parser.add_argument('--batch-size', type=int, default=10000)
        parser.add_argument('--skip-header', type=int, default=2)

    def handle(self, *args, **options):
        processed, inserted = import_states(
            input_file=options['file'],
            batch_size=options['batch_size'],
            skip_header=options['skip_header'],
            verbose=True
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Processed {processed} lines, inserted {inserted} unique states'
            )
        )
