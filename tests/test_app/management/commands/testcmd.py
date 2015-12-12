from optparse import make_option

from django.core.management.base import BaseCommand


class IgnoramusException(Exception):
    pass


class Command(BaseCommand):
    help = 'Test command'

    option_list = BaseCommand.option_list + (
        make_option('--fail',
                    action='store_true',
                    dest='fail',
                    default=False,
                    help='Raise exception'),
    )

    def handle(self, *args, **options):
        if options['fail']:
            raise IgnoramusException('use jQuery')
        print ('OK')
