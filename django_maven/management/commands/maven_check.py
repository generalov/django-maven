from optparse import make_option

from django.core.management.base import BaseCommand


class MavenCheckException(Exception):
    pass


class Command(BaseCommand):
    help = 'Run `manage.py maven maven_check` and look for MavenCheckException in the Sentry issues list.'

    option_list = BaseCommand.option_list + (
        make_option('--ok',
                    action='store_true',
                    dest='ok',
                    default=False,
                    help='just print "OK" message'),
    )

    def handle(self, *args, **options):
        if options['ok']:
            print ('OK')
        else:
            raise MavenCheckException("Errors should never pass silently.")


