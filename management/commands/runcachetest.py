from django.core.management.base import BaseCommand, CommandError
from acipenser.runner import TestRunner


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments

        # Named (optional) arguments
        parser.add_argument(
            '-s',
            '--safe',
            type=bool,
            default=False,
            # help='run test if request not update db',
        )

    def handle(self, *args, **options):
        is_safe = options.get('safe', True)
        runner = TestRunner(is_safe=is_safe)
        runner.run()
