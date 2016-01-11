"""This module is about the case of invalid import in the django management command
or absend requirement.

The command::

    manage.py maven test_maven_import_error

should send traceback
"""

import not_installed_module
