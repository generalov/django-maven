django-maven
============

Capture exceptions in django management commands into Sentry by Raven.

Problem And Solution
--------------------

Many management commands running in cron and by default errors and exceptions not wrote in logs.
Or some people redirect all stdout in file (`command >> file.txt`) with log rotation or not.

This package make possible **capture exceptions** (not all stdout/stderr) in your Sentry project.

Installation
------------

1. Install package:

    $ pip install django-maven

2. Add `django_maven` in `INSTALLED_APPS`.

3. Use it! ;)

Example Of Usage
----------------

It's simple!

Add `maven` command by first argument for manage.py in your management command string.

For example, this is command without `django-maven`:

    $ python manage.py rebuild_index --noinput

And command with `django-maven`:

    $ python manage.py maven rebuild_index --noinput

If `rebuild_index` command raising exception (server die or error creating index) you see their in your Sentry.

Tests
-----

Tests should run with tox >=1.8. Running `tox` will run all tests for all environments.
Use tox -e <env> to run a certain environment, a list of all environments can be found with tox -l.

Hint: it is possible to run all environments in parallel with `detox`.

The name
--------

**django-maven** is django Management rAVEN.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/saippuakauppias/django-maven/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

