"""Manage projects & teams.

Install and mount `ourprojects` in a new instance:

>>> pip install ourprojects
>>> lamin init --storage ./test-ourprojects --schema ourprojects

Import the package:

>>> import ourprojects as ops

The `Reference` registry:

.. autosummary::
   :toctree: .

    Project
"""

__version__ = "0.0.1"  # denote a pre-release for 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="ourprojects")
    return globals()[name]


if _check_instance_setup():
    import lamindb

    del __getattr__  # delete so that imports work out
    from .models import Project
