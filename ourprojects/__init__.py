"""Manage projects & teams [`source <https://github.com/laminlabs/ourprojects/blob/main/ourprojects/models.py>`__].

Install the package::

   pip install ourprojects

Import the package::

   import ourprojects as ops

The `Reference` registry:

.. autosummary::
   :toctree: .

    Reference
"""

__version__ = "0.0.1"  # denote a pre-release for 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="ourprojects")
    return globals()[name]


if _check_instance_setup():
    del __getattr__  # delete so that imports work out
    from .models import Reference
