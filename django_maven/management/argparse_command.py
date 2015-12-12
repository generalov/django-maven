import argparse

from django.core.management.base import BaseCommand


class MavenBaseCommand(BaseCommand):
    """The *argparse* compatible command"""

    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument('args', nargs=argparse.REMAINDER)
