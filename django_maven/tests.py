try:
    from unittest.case import skipIf
except ImportError:
    from unittest2.case import skipIf

from django.core.management.base import BaseCommand, handle_default_options
from django.test import TestCase
from django_maven.management.argparse_command import \
    MavenBaseCommand as ArgparseMavenBaseCommand
from django_maven.management.optparse_command import \
    MavenBaseCommand as OptparseMavenBaseCommand


class TestCommandParserMixin(object):

    def test_parse_maven_default_options(self):
        args, options = self._handle_argv(['--verbosity', '2'])
        self.assertEqual(args, [])
        self.assertEqual(int(options['verbosity']), 2)

    def test_parse_subcommand(self):
        args, options = self._handle_argv(['subcommand'])
        self.assertEqual(args, ['subcommand'])

    def test_should_keep_subcommand_default_options(self):
        args, options = self._handle_argv(['subcommand', '--help'])
        self.assertEqual(args, ['subcommand', '--help'])

    def test_should_keep_subcommand_custom_options(self):
        args, options = self._handle_argv(['subcommand', '--foo'])
        self.assertEqual(args, ['subcommand', '--foo'])

    def test_mavens_and_subcommands_default_options_should_not_conflict(self):
        args, options = self._handle_argv(
            ['--verbosity', '2', 'subcommand', '--verbosity', '3'])
        self.assertEqual(int(options['verbosity']), 2)
        self.assertEqual(args, ['subcommand', '--verbosity', '3'])

    def _handle_argv(self, argv):
        raise NotImplementedError()


@skipIf(not hasattr(BaseCommand, 'use_argparse'),
        'This Django doesn\'t use argparse')
class ArgparseCommandParserTest(TestCommandParserMixin, TestCase):
    """
    :type parser: django.core.management.base.CommandParser"""

    def setUp(self):
        self.cmd = ArgparseMavenBaseCommand()
        self.parser = self.cmd.create_parser('manage.py', 'maven')

    def _handle_argv(self, argv):
        options = self.parser.parse_args(argv)
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        handle_default_options(options)
        return args, cmd_options


class OptparseCommandParserTest(TestCommandParserMixin, TestCase):
    """:type parser: django.core.management.base.OptionParser"""

    def setUp(self):
        self.cmd = OptparseMavenBaseCommand()
        self.parser = self.cmd.create_parser('manage.py', 'maven')

    def _handle_argv(self, argv):
        options, args = self.parser.parse_args(argv)
        cmd_options = vars(options)
        handle_default_options(options)
        return args, cmd_options
