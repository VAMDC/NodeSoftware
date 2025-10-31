from django.core.management.base import BaseCommand
from valdimport import import_states_transitions


class Command(BaseCommand):
    help = 'Combined single-pass import of states and transitions from VALD format'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Input file (or use stdin)')
        parser.add_argument('--batch-size', type=int, default=10000)
        parser.add_argument('--skip-header', type=int, default=2)
        parser.add_argument('--skip-calc', action='store_true',
                          help='Skip Einstein A calculation')
        parser.add_argument('--no-read-ahead', action='store_true',
                          help='Disable read-ahead thread (enabled by default)')

    def handle(self, *args, **options):
        processed, states_inserted, trans_inserted = import_states_transitions(
            input_file=options['file'],
            batch_size=options['batch_size'],
            skip_header=options['skip_header'],
            skip_calc=options['skip_calc'],
            read_ahead=not options['no_read_ahead'],
            verbose=True
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Processed {processed} lines, '
                f'inserted {states_inserted} unique states, '
                f'{trans_inserted} transitions'
            )
        )
