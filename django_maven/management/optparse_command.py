import types
from optparse import AmbiguousOptionError, BadOptionError

from django.core.management.base import BaseCommand


class MavenBaseCommand(BaseCommand):
    """The *optparse* compatible command

    manage.py maven [maven options] subcommand [subcommand options]
    """

    @property
    def use_argparse(self):
        return False

    def create_parser(self, prog_name, subcommand):
        parser = super(MavenBaseCommand, self).create_parser(
            prog_name, subcommand)
        parser._process_args = types.MethodType(_process_args, parser)
        return parser


def _process_args(self, largs, rargs, values):
    max_own_positional_args = 1

    while rargs:
        try:
            arg = rargs[0]
            # XXX: e.generalov@ added condition to skip processing
            # arguments after subcommand name
            if len(largs) >= max_own_positional_args:
                return  # stop now, leave this arg in rargs
            # We handle bare "--" explicitly, and bare "-" is handled by the
            # standard arg handler since the short arg case ensures that the
            # len of the opt string is greater than 1.
            elif arg == '--':
                del rargs[0]
                return
            elif arg[0:2] == '--':
                # process a single long option (possibly with value(s))
                self._process_long_opt(rargs, values)
            elif arg[:1] == '-' and len(arg) > 1:
                # process a cluster of short options (possibly with
                # value(s) for the last one only)
                self._process_short_opts(rargs, values)
            elif self.allow_interspersed_args:
                largs.append(arg)
                del rargs[0]
            else:
                return  # stop now, leave this arg in rargs

        except (BadOptionError, AmbiguousOptionError) as e:
            largs.append(e.opt_str)
