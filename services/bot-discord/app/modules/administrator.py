import logging
import discord
from typing import List, Optional
from . import *
from .orchestrator import *
from .shared import *

# NOTE: main.py's /report (or equivalent) admin-mode branch constructs
# `EnhancedAdministratorView()`, but no such class is defined anywhere in this
# module (or the rest of the codebase) -- that code path raises a NameError at
# runtime. This is a separate, pre-existing bug, not addressed here; the
# now-removed `PersistentAdministratorView` stub that used to live in this file
# was an empty placeholder (no buttons, not correctly configured for
# persistence either) and registering it achieved nothing, so it was deleted
# rather than patched.
