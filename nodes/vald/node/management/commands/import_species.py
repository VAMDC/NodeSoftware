from django.core.management.base import BaseCommand
from valdimport import import_species


class Command(BaseCommand):
    help = 'Import species from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True, help='Species CSV file')
        parser.add_argument('--batch-size', type=int, default=10000)

    def handle(self, *args, **options):
        processed, inserted = import_species(
            input_file=options['file'],
            batch_size=options['batch_size'],
            verbose=True
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Processed {processed} lines, inserted {inserted} total species'
            )
        )
