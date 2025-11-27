from django.core.management.base import BaseCommand
from valdimport import import_bibtex


class Command(BaseCommand):
    help = 'Import references from BibTeX file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True, help='BibTeX file')
        parser.add_argument('--batch-size', type=int, default=1000)

    def handle(self, *args, **options):
        processed, inserted = import_bibtex(
            input_file=options['file'],
            batch_size=options['batch_size'],
            verbose=True
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Processed {processed} BibTeX entries, inserted {inserted} total references'
            )
        )
