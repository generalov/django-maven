from __future__ import unicode_literals

import locale
import os
import subprocess

from django.test import TestCase


class MavenCommandTest(TestCase):

    def test_subcommand(self):
        result = get_output(['django-admin.py',
                             'testcmd', '--settings=test_project.settings'])
        self.assertEqual('OK', result.output.strip())
        self.assertEqual(0, result.returncode)

    def test_maven_subcommand(self):
        result = get_output(['django-admin.py',
                             'maven', '--settings=test_project.settings',
                             'testcmd'])
        self.assertEqual('OK', result.output.strip())
        self.assertEqual(0, result.returncode)

    def test_maven_should_capture_exceptions_from_subcommand(self):
        result = get_output(['django-admin.py',
                             'maven', '--settings=test_project.settings',
                             '--traceback', '--verbosity=2',
                             'testcmd', '--fail'])
        self.assertIn('Beautiful is better than IgnoramusException. '
                      'Errors should never pass silently.',
                      result.output.strip())
        self.assertIn('Traceback', result.output.strip())
        self.assertNotEqual(0, result.returncode)


def get_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a string."""

    def decode(bytes):
        return bytes.decode(locale.getpreferredencoding(False), 'ignore')

    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               env=dict(os.environ),
                               *popenargs, **kwargs)
    output, err = process.communicate()
    retcode = process.poll()
    cmd = kwargs.get('args')
    if cmd is None:
        cmd = popenargs[0]
    if retcode:
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = decode(err)
        return error
    else:
        result = CalledProcessResult(cmd, decode(output))
        return result


class CalledProcessResult(object):

    def __init__(self, cmd, output=None):
        self.cmd = cmd
        self.output = output
        self.returncode = 0

    def __str__(self):
        return "Command '%s' success" % (self.cmd)
