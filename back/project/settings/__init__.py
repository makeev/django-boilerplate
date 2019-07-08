# coding: utf-8
#
from .settings import *
from .constance import *
from .logging import *
from .admin_reorder import *

try:
    from .settings_local import *
except ImportError:
    try:
        from .settings_develop import *
    except ImportError:
        pass
    pass

import project.monkey_patch
