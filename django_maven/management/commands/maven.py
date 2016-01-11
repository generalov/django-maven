import sys

from django.conf import settings
from django.core.management import get_commands, load_command_class
from django.core.management.base import CommandError, handle_default_options
from django_maven.compat import MavenBaseCommand, OutputWrapper
from raven import Client

VERBOSE_OUTPUT = 2


class Command(MavenBaseCommand):
    help = 'Capture exceptions and send in Sentry'

    def __init__(self, *args, **kw):
        super(MavenBaseCommand, self).__init__(*args, **kw)
        self._argv = None

    def run_from_argv(self, argv):
        self._argv = argv
        return super(Command, self).run_from_argv(argv)

    def execute(self, *args, **options):
        if not args:
            self.print_help(self._argv[0], self._argv[1])
            return

        try:
            subcommand = self._get_subcommand_class(args[0])
            subcommand_argv = [self._argv[0]] + list(args)

            # this is a lightweight version of the BaseCommand.run_from_argv
            # it should be compatible with Django-1.5..1.9
            subcommand_args, subcommand_options = self._handle_argv(
            subcommand, subcommand_argv)
            subcommand.execute(*subcommand_args, **subcommand_options)
        except Exception as e:
            if not isinstance(e, CommandError):
                if int(options['verbosity']) >= VERBOSE_OUTPUT:
                    # self.stderr is not guaranteed to be set here
                    stderr = getattr(self, 'stderr', OutputWrapper(
                        sys.stderr, self.style.ERROR))
                    stderr.write('Maven: got %s.' % (e.__class__.__name__))

                sentry = self._get_sentry()
                if sentry:
                    sentry.captureException()
            # use default 'maven' options to deal with traceback
            raise

    def _get_sentry(self):
        if hasattr(settings, 'SENTRY_DSN'):
            dsn = settings.SENTRY_DSN
        elif hasattr(settings, 'RAVEN_CONFIG'):
            dsn = settings.RAVEN_CONFIG.get('dsn')
        else:
            return None

        sentry = Client(dsn)
        if not sentry.is_enabled():
            return None
        return sentry

    def _get_subcommand_class(self, command):
        commands = get_commands()
        app_name = commands[command]
        return load_command_class(app_name, command)

    def _handle_argv(self, subcommand, argv):
        """The universal Django command arguments parser."""
        parser = subcommand.create_parser(argv[0], argv[1])

        if hasattr(subcommand, 'use_argparse') and subcommand.use_argparse:
            options = parser.parse_args(argv[2:])
            cmd_options = vars(options)
            # Move positional args out of options to mimic legacy optparse
            args = cmd_options.pop('args', ())
        else:
            options, args = parser.parse_args(argv[2:])
            cmd_options = vars(options)
        handle_default_options(options)
        return args, cmd_options
